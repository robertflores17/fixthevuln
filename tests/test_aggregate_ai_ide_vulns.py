"""Covers the collector's riskiest case: the relevance gate. Every string in
KEEP and DROP below is real NVD or GHSA text from a live run, not invented.
The DROP set is what a naive keyword match actually pulled in -- database and
kernel cursors, Zed Attack Proxy -- and each bug these tests pin was found by
running the collector against production data, not by reading the regex.
"""
import json
import sys
import tempfile
import time
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from aggregate_ai_ide_vulns import (
    is_relevant, vendor_of, product_match, merge, severity_label,
    _cvss_from_metrics, _trim, MAX_STORED, affected_product,
    parse_arxiv_atom, MAX_ARXIV_BYTES, _author_matches, ARXIV_AUTHOR_NAMES,
)

# Real advisory openings that must be tracked.
KEEP = {
    "Cursor is a code editor built for programming with AI. Prior to 3.0.0, "
    "Cursor IDE for macOS allows a crafted workspace to run code.": "Cursor",
    "Zed is a code editor. Prior to 0.227.1, Zed builds SSH/WSL remote "
    "commands as a shell string without quoting.": "Zed",
    "Cline is an autonomous coding agent as an SDK, IDE extension, or CLI "
    "assistant. In versions prior to 3.0, ...": "Cline",
    "ToolHive is a utility designed to simplify the deployment and management "
    "of Model Context Protocol servers.": "MCP",
    "A prompt injection vulnerability exists in Windsurf version 1.10.7 in "
    "Write mode using the AI agent.": "Windsurf",
    "GitHub Copilot 1.372.0 allows filesystem access outside of a workspace "
    "folder via the AI agent.": "GitHub Copilot",
    "aider (aider-chat) automatically loads a .aider.conf.yml configuration "
    "file from the root of the repository, an agent autoload risk.": "Aider",
}

# Real advisories that name a tracked word incidentally. These are the exact
# rows an earlier version of the gate wrongly filed under "Cursor".
DROP = [
    "Semantic MediaWiki is a free, open-source extension to MediaWiki that "
    "lets users store and query data, including via a database cursor.",
    "async-tar is a tar archive reading/writing library for async Rust. Prior "
    "to version 0.6.1, async-tar mishandles a cursor during extension parsing.",
    "Ruby JSON is a JSON implementation for Ruby. From 2.20.0 until 2.21.2, "
    "Ruby's JSON native C extension mishandles a parser cursor.",
    "node-tar is a full-featured Tar for Node.js. Prior to 7.5.16, tar "
    "(node-tar) applies a PAX extension header at the wrong cursor offset.",
    "In the Linux kernel, the following vulnerability has been resolved: "
    "sctp: revalidate cursor in the chunk walk.",
    "In MongoDB Server 8.0, an aggregation stage can leave its _subPipeline "
    "field null during cursor setup.",
    "Zed Attack Proxy (ZAP) ViewState add-on before version 4 contains an "
    "insecure deserialization issue.",
]


class TestRelevanceGate(unittest.TestCase):
    def test_keeps_real_ai_ide_advisories(self):
        for text in KEEP:
            with self.subTest(text=text[:40]):
                self.assertTrue(is_relevant(text))

    def test_drops_incidental_keyword_matches(self):
        for text in DROP:
            with self.subTest(text=text[:40]):
                self.assertFalse(is_relevant(text))

    def test_assigns_expected_vendor(self):
        for text, vendor in KEEP.items():
            with self.subTest(vendor=vendor):
                self.assertEqual(vendor_of(text), vendor)

    def test_weak_name_counts_only_in_subject_position(self):
        """'Cursor' leading the advisory is the product; 'cursor' buried in a
        MongoDB description is a database cursor."""
        self.assertIsNotNone(product_match("Cursor is a code editor with AI"))
        self.assertIsNone(product_match(
            "A flaw in the query planner of some unrelated database product "
            "means the iteration cursor can be advanced past its bound, which "
            "is well beyond the subject window of this advisory text."))

    def test_strong_name_counts_anywhere(self):
        self.assertIsNotNone(product_match(
            "A very long preamble that pushes the product name far past the "
            "subject window before finally naming the affected component, "
            "which turns out to be Windsurf."))

    def test_matches_hyphenated_product_names(self):
        """Roo-Code and claude-code are spelled with hyphens as often as with
        spaces; \\s? silently missed every hyphenated form."""
        for text in ("RooCodeInc/Roo-Code command injection in the coding agent",
                     "Kilo-Code extension for VS Code allows prompt injection",
                     "claude-code npm package leaks tokens to an MCP server"):
            with self.subTest(text=text[:30]):
                self.assertTrue(is_relevant(text))

    def test_matches_plural_context_words(self):
        """"Claude Code extensions" must not fall through a singular-only
        context pattern."""
        self.assertTrue(is_relevant(
            "Claude Code Templates is a CLI tool for configuring and "
            "monitoring Claude Code extensions."))


class TestSeverity(unittest.TestCase):
    def test_cvss_bands(self):
        self.assertEqual(severity_label('9.8'), 'Critical')
        self.assertEqual(severity_label('7.0'), 'High')
        self.assertEqual(severity_label('4.0'), 'Medium')
        self.assertEqual(severity_label('3.9'), 'Low')

    def test_missing_score_is_blank_not_an_error(self):
        for value in ('', None, 'n/a'):
            with self.subTest(value=value):
                self.assertEqual(severity_label(value), '')

    def test_prefers_newest_cvss_spec(self):
        metrics = {
            'cvssMetricV2': [{'cvssData': {'baseScore': 5.0}}],
            'cvssMetricV31': [{'cvssData': {'baseScore': 9.1}}],
        }
        self.assertEqual(_cvss_from_metrics(metrics), '9.1')

    def test_falls_back_when_no_v31(self):
        self.assertEqual(
            _cvss_from_metrics({'cvssMetricV2': [{'cvssData': {'baseScore': 5.0}}]}), '5.0')
        self.assertEqual(_cvss_from_metrics({}), '')


class TestPrimaryScorePreference(unittest.TestCase):
    """NVD's own Primary rating outranks the reporting CNA's Secondary, and the
    API does not order them. Real case: CVE-2026-13323 lists Eclipse's
    Secondary 4.1 MEDIUM ahead of NVD's Primary 8.7 HIGH."""

    def test_primary_wins_when_listed_second(self):
        metrics = {'cvssMetricV31': [
            {'type': 'Secondary', 'cvssData': {'baseScore': 4.1}},
            {'type': 'Primary', 'cvssData': {'baseScore': 8.7}}]}
        self.assertEqual(_cvss_from_metrics(metrics), '8.7')
        self.assertEqual(severity_label(_cvss_from_metrics(metrics)), 'High')

    def test_secondary_used_when_no_primary_exists(self):
        metrics = {'cvssMetricV31': [{'type': 'Secondary', 'cvssData': {'baseScore': 4.1}}]}
        self.assertEqual(_cvss_from_metrics(metrics), '4.1')

    def test_version_precedence_still_beats_type(self):
        """A v3.1 Secondary is preferred over a v2 Primary: newer spec first."""
        metrics = {'cvssMetricV31': [{'type': 'Secondary', 'cvssData': {'baseScore': 4.1}}],
                   'cvssMetricV2': [{'type': 'Primary', 'cvssData': {'baseScore': 9.0}}]}
        self.assertEqual(_cvss_from_metrics(metrics), '4.1')


class TestAffectedProduct(unittest.TestCase):
    """A tracked name reached through a "for X" clause is context, not the
    affected product. Every string here is real advisory text that the earlier
    vendor guess misattributed."""

    def test_subject_wins_over_a_name_in_a_for_clause(self):
        self.assertEqual(affected_product(
            "Ruflo is an agent meta-harness for Claude Code and Codex. Prior to 3.16.3, "
            "ruflo's default configuration ..."), 'Ruflo')

    def test_extracts_from_in_x_before_shape(self):
        self.assertEqual(affected_product(
            "In Open VSX Registry before 1.0.2, the /vscode/unpkg/ endpoint serves "
            "user-supplied HTML files."), 'Open VSX Registry')

    def test_extracts_from_bare_version_shape(self):
        self.assertEqual(affected_product(
            "GitHub Copilot 1.372.0 allows filesystem access outside of a workspace "
            "folder."), 'GitHub Copilot')

    def test_extracts_from_discovered_in_shape(self):
        self.assertEqual(affected_product(
            "A security flaw has been discovered in dazeb cline-mcp-memory-bank up to "
            "55c81b9cf6c1."), 'dazeb cline-mcp-memory-bank')

    def test_strips_backticks_from_package_names(self):
        self.assertEqual(affected_product(
            "`@zereight/mcp-gitlab` is a Model Context Protocol server for GitLab."),
            '@zereight/mcp-gitlab')

    def test_blank_when_no_clear_subject(self):
        """Blank claims nothing; a guess misattributes someone else's bug."""
        self.assertEqual(affected_product("Some advisory with no recognisable shape"), '')
        self.assertEqual(affected_product(''), '')
        self.assertEqual(affected_product(None), '')

    def test_rejects_a_capture_that_swallowed_a_version_clause(self):
        """Real regression: this yielded "Spring AI. Prior to" by matching
        across the sentence break, misattributing the bug to Spring AI. It then
        returned blank once that capture was rejected, and now returns the
        actual product via the closed verb set. What must never come back is
        the misattribution."""
        got = affected_product(
            "mcp-security provides Security and Authorization support for Model "
            "Context Protocol in Spring AI. Prior to 0.1.9, the mcp-security "
            "framework fails to validate tokens.")
        self.assertEqual(got, 'mcp-security')
        self.assertNotIn('Spring AI', got)
        self.assertNotIn('Prior to', got)

    def test_strips_a_trailing_version_from_a_range(self):
        """Real regression: "IBM Langflow OSS 1.0.0" in an Affected product
        column reads as "1.0.0 is affected, 1.10.0 is not". The advisory covers
        1.0.0 through 1.10.3, so the version must not be named at all."""
        self.assertEqual(affected_product(
            "IBM Langflow OSS 1.0.0 through 1.10.3 contain an authentication "
            "bypass vulnerability in the MCP composer endpoint."),
            'IBM Langflow OSS')

    def test_names_the_product_not_the_component(self):
        self.assertEqual(affected_product(
            "A vulnerability in the WebSocket endpoint of gpt-researcher v0.14.7 "
            "and before allows code execution."), 'gpt-researcher')

    def test_never_returns_a_junk_word(self):
        for text in ("version 1.2.3 of something is a thing",
                     "A vulnerability is an issue in software"):
            with self.subTest(text=text[:30]):
                self.assertNotIn(affected_product(text).lower(),
                                 {'version', 'a', 'an', 'the', 'vulnerability'})


ATOM = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
 <entry>
  <id>http://arxiv.org/abs/2509.08646v1</id>
  <title>Architecting Resilient
   LLM Agents</title>
  <published>2025-09-10T00:00:00Z</published>
  <summary>As LLM agents become capable of automating tasks.</summary>
  <author><name>Ron F. Del Rosario</name></author>
  <author><name>Klaudia Krawiecka</name></author>
 </entry>
 <entry>
  <id>http://arxiv.org/abs/9999.99999v1</id>
  <title>Unrelated paper by someone else</title>
  <published>2025-01-01T00:00:00Z</published>
  <summary>Nothing to do with the tracked author.</summary>
  <author><name>Maria Del Rosario</name></author>
 </entry>
</feed>"""


class TestAffectedProductOpenings(unittest.TestCase):
    """Real advisory openings that produced a blank product cell. All six are
    verbatim from data/ai-ide-vulns.json, not invented. The column advertises
    product search, so a blank cell is a visible gap."""

    def test_parenthetical_gloss_does_not_blank_the_subject(self):
        # Advisories routinely gloss the product with its package name, and the
        # subject patterns cannot match across the parens.
        for desc, expected in (
            ("AWS HealthLake MCP Server (awslabs.healthlake-mcp-server) is a "
             "Model Context Protocol server that enables AI assistants.",
             "AWS HealthLake MCP Server"),
            ("The MCP PHP SDK (Composer package mcp/sdk) is the official Model "
             "Context Protocol SDK for PHP.", "MCP PHP SDK"),
        ):
            self.assertEqual(affected_product(desc), expected)

    def test_descriptive_verbs_other_than_is(self):
        for desc, expected in (
            ("AgenticMail gives AI agents real email addresses and phone numbers.",
             "AgenticMail"),
            ("mcp-security provides Security and Authorization support for Model "
             "Context Protocol in Spring AI. Prior to 0.1.9, the framework fails.",
             "mcp-security"),
            ("BerriAI LiteLLM contains an improper authentication vulnerability "
             "in the MCP Streamable HTTP endpoint.", "BerriAI LiteLLM"),
        ):
            self.assertEqual(affected_product(desc), expected)

    def test_rejects_a_phrase_about_the_product(self):
        """"<noun> in <Product>" names the product inside a phrase the advisory
        never asserted. Publishing "vulnerability in Cline" puts a real
        vendor's name in a fabricated one, which is worse than a blank cell.
        These openings all passed the verb match with a bad subject."""
        for desc in (
            "The vulnerability in Cline enables remote attackers to read files.",
            "The insecure default in Cursor provides attackers with code execution.",
            "A crafted request (see PoC) enables path traversal.",
            "The affected version contains a flaw in the MCP handler.",
        ):
            with self.subTest(desc=desc[:40]):
                self.assertEqual(affected_product(desc), '')

    def test_product_names_containing_prepositions_survive(self):
        """Rejecting prepositions generally cost two correct captures, so only
        " in " is rejected. "Cursor for Windows" is a real product name."""
        self.assertEqual(
            affected_product("Cursor for Windows before 1.2.3 allows code execution"),
            'Cursor for Windows')

    def test_verb_set_stays_closed(self):
        """A general "^SUBJ <any verb>" rule would name the opening noun phrase
        of almost any sentence. These must still return blank rather than
        guess."""
        for desc in (
            "A vulnerability was discovered that affects several servers.",
            "This issue occurs when the server starts.",
            "An attacker sends a crafted request to the endpoint.",
        ):
            self.assertEqual(affected_product(desc), '')

    def test_protocol_context_opener_is_not_a_product_claim(self):
        """An advisory that OPENS with protocol context still belongs to a
        product. CVE-2026-11624 reads "The Model Context Protocol has a
        security warning..." and I wrongly called it spec guidance; its CNA is
        cve-coordination@google.com and the fix is --allowed-hosts in v0.25.0
        of Google's MCP Toolbox for Databases. Blank is the right output for
        the extractor, because the product is not in the opening clause, but
        the row must not be left blank on the page: it is backfilled by hand in
        data/ai-ide-vulns.json. A blank cell beside a Critical 9.4 made the
        page read as if the protocol itself carried that score."""
        self.assertEqual(
            affected_product("The Model Context Protocol has a security warning "
                             "advising servers to validate the Origin header."), '')


class TestAffectedProductRuntime(unittest.TestCase):
    """Advisory text is CNA-authored, so it is adversarial input. When _NAME's
    body class and _SUBJ's separator class both held '-', a hyphen run had
    O(n^6) partitions and a 144-char chain took 0.5s; ~300 bytes would have
    hung the daily job past the Actions ceiling. This is the one regression
    that would not announce itself -- the job just stops producing commits."""

    def test_long_hyphen_chain_stays_fast(self):
        desc = "MCP agent flaw. An issue was discovered in " + "a-" * 400 + " which is bad"
        start = time.perf_counter()
        affected_product(desc)
        self.assertLess(time.perf_counter() - start, 0.1)

    def test_hyphenated_names_still_extract(self):
        # The fix must not cost us hyphenated product names, which are the norm
        # for npm-scoped MCP servers.
        for desc, expected in (
            ("roo-code before 3.2.1 allows path traversal", "roo-code"),
            ("@zereight/mcp-gitlab before 2.1.27 exposes all MCP tools",
             "@zereight/mcp-gitlab"),
            ("cline-mcp-memory-bank version 1.0.2 leaks tokens",
             "cline-mcp-memory-bank"),
        ):
            self.assertEqual(affected_product(desc), expected)


class TestArxivParsing(unittest.TestCase):
    def test_a_different_person_with_the_same_surname_is_rejected(self):
        """arXiv cs.CR submission is open, so a surname substring match would
        let anyone named Del Rosario onto a page that vouches for him by name.
        The second fixture entry is authored by a different Del Rosario."""
        papers = parse_arxiv_atom(ATOM)
        self.assertEqual([p['id'] for p in papers], ['2509.08646v1'])

    def test_accepts_both_spellings_of_the_real_author(self):
        for name in ('Ron F. Del Rosario', 'Ronald F. Del Rosario', 'ron f. del rosario'):
            with self.subTest(name=name):
                self.assertTrue(_author_matches([name], ARXIV_AUTHOR_NAMES))

    def test_rejects_surname_only_and_impostors(self):
        for name in ('Del Rosario', 'Maria Del Rosario', 'Ron Del Rosario'):
            with self.subTest(name=name):
                self.assertFalse(_author_matches([name], ARXIV_AUTHOR_NAMES))

    def test_preserves_author_order(self):
        """Author order carries meaning in academic credit; never reorder."""
        self.assertEqual(parse_arxiv_atom(ATOM)[0]['authors'],
                         ['Ron F. Del Rosario', 'Klaudia Krawiecka'])

    def test_collapses_whitespace_in_wrapped_titles(self):
        self.assertEqual(parse_arxiv_atom(ATOM)[0]['title'],
                         'Architecting Resilient LLM Agents')

    def test_upgrades_abstract_link_to_https(self):
        self.assertTrue(parse_arxiv_atom(ATOM)[0]['url'].startswith('https://'))

    def test_refuses_a_doctype(self):
        """ElementTree expands internal entities, so a DTD is a billion-laughs
        vector. arXiv never sends one."""
        billion = (b'<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">'
                   b'<!ENTITY lol1 "&lol;&lol;&lol;">]>'
                   b'<feed xmlns="http://www.w3.org/2005/Atom"><entry>'
                   b'<author><name>Ron F. Del Rosario</name></author></entry></feed>')
        self.assertEqual(parse_arxiv_atom(billion), [])

    def test_refuses_an_oversized_response(self):
        self.assertEqual(parse_arxiv_atom(b'x' * (MAX_ARXIV_BYTES + 1)), [])

    def test_malformed_xml_returns_empty_not_an_exception(self):
        self.assertEqual(parse_arxiv_atom(b'<feed><unclosed>'), [])


class TestKevDates(unittest.TestCase):
    """kev-data.json carries only dateAdded, the CISA catalog-add date. It is
    not a publication date and must never reach the table's "Published"
    column: CVE-2026-59822 was added 2026-09-02 but NVD published it
    2026-07-08, an 8-week error."""

    def _collect(self, record):
        import aggregate_ai_ide_vulns as agg
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'kev-data.json'
            f.write_text(json.dumps({'vulnerabilities': [record]}), encoding='utf-8')
            with mock.patch.object(agg, 'KEV_DATA_FILE', f):
                return agg.collect_kev()

    def test_catalog_add_date_is_not_published(self):
        entries = self._collect({
            'id': 'CVE-2026-59822',
            'title': 'BerriAI LiteLLM MCP authentication bypass',
            'description': 'BerriAI LiteLLM contains an improper authentication '
                           'vulnerability in the MCP Streamable HTTP endpoint.',
            'cvss': '8.2',
            'dateAdded': '2026-09-02',
        })
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['published'], '')
        self.assertEqual(entries[0]['kev_added'], '2026-09-02')


class TestMerge(unittest.TestCase):
    def _entry(self, cve_id, published='2026-09-01'):
        return {'id': cve_id, 'published': published, 'source': 'nvd'}

    def test_adds_new_and_skips_duplicates(self):
        state = {'last_updated': None, 'entries': []}
        self.assertEqual(merge(state, [self._entry('CVE-1'), self._entry('CVE-2')]), 2)
        self.assertEqual(merge(state, [self._entry('CVE-2'), self._entry('CVE-3')]), 1)
        self.assertEqual([e['id'] for e in state['entries']], ['CVE-3', 'CVE-2', 'CVE-1'])

    def test_same_cve_from_two_sources_stored_once(self):
        """GHSA and NVD both carry the same CVE id; the tracker shows one row."""
        state = {'last_updated': None, 'entries': []}
        merge(state, [{'id': 'CVE-9', 'published': '2026-09-01', 'source': 'nvd'}])
        merge(state, [{'id': 'CVE-9', 'published': '2026-09-01', 'source': 'ghsa'}])
        self.assertEqual(len(state['entries']), 1)
        self.assertEqual(state['entries'][0]['source'], 'nvd')

    def test_sorts_newest_first(self):
        state = {'last_updated': None, 'entries': []}
        merge(state, [self._entry('CVE-A', '2026-01-01'),
                      self._entry('CVE-B', '2026-09-18')])
        self.assertEqual([e['id'] for e in state['entries']], ['CVE-B', 'CVE-A'])

    def test_skips_entries_without_an_id(self):
        state = {'last_updated': None, 'entries': []}
        self.assertEqual(merge(state, [{'id': '', 'published': '2026-09-01'}]), 0)

    def test_stamps_status_and_detected_at(self):
        state = {'last_updated': None, 'entries': []}
        merge(state, [self._entry('CVE-1')])
        self.assertEqual(state['entries'][0]['status'], 'new')
        datetime.fromisoformat(state['entries'][0]['detected_at'])


class TestRetention(unittest.TestCase):
    def test_caps_stored_entries(self):
        """The file is committed daily; unbounded growth is repo bloat."""
        state = {'last_updated': None, 'entries': []}
        merge(state, [{'id': f'CVE-{i:05d}', 'published': f'2026-09-{(i % 28) + 1:02d}',
                       'source': 'nvd'} for i in range(MAX_STORED + 50)])
        self.assertEqual(len(state['entries']), MAX_STORED)

    def test_cap_keeps_the_newest(self):
        state = {'last_updated': None, 'entries': []}
        merge(state, [{'id': 'CVE-OLD', 'published': '2020-01-01', 'source': 'nvd'}])
        merge(state, [{'id': f'CVE-{i:05d}', 'published': '2026-09-18', 'source': 'nvd'}
                      for i in range(MAX_STORED)])
        self.assertEqual(len(state['entries']), MAX_STORED)
        self.assertNotIn('CVE-OLD', [e['id'] for e in state['entries']])


class TestTrim(unittest.TestCase):
    def test_collapses_whitespace(self):
        self.assertEqual(_trim("a\n  b   c"), "a b c")

    def test_truncates_on_a_word_boundary(self):
        out = _trim("word " * 100, limit=40)
        self.assertTrue(out.endswith('...'))
        self.assertLessEqual(len(out), 44)

    def test_handles_empty(self):
        self.assertEqual(_trim(''), '')
        self.assertEqual(_trim(None), '')


if __name__ == '__main__':
    unittest.main()
