#!/usr/bin/env python3
"""Tests for scripts/detect_hot_topics.py.

Run: python3 -m unittest tests.test_detect_hot_topics

Titles come from the 2026-10-20..23 PHP and Node.js Brotli stories this detector exists to catch
earlier. Feed text is untrusted and lands in a GitHub issue, so clean()/render() are pinned too.
"""

import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from detect_hot_topics import (candidate, clean, from_feed, from_ghsa, from_kev, issue_candidates, patch_tuesday, render,
                               select_and_mark)

ROOT = Path(__file__).resolve().parent.parent
WATCH = {k: [t.lower() for t in v] if isinstance(v, list) else v
         for k, v in json.loads((ROOT / 'data' / 'hot-topic-watchlist.json').read_text()).items()}
NOW = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)
CUTOFF = NOW - timedelta(hours=72)


def item(title, hours_ago=5, link='https://example.com/a'):
    return {'title': title, 'link': link, 'summary': '', 'published': '', 'published_dt': NOW - timedelta(hours=hours_ago)}


class TestFeeds(unittest.TestCase):
    def test_php_preannouncement_is_priority_three_and_plain_release_only_one(self):
        got = from_feed('php.net', [item('Upcoming Critical PHP Security Release'), item('PHP 8.5.12 Released!'),
                                    item('PHP Conference 2026 call for papers')], CUTOFF)
        self.assertEqual([(c['title'], c['score']) for c in got],
                         [('Upcoming Critical PHP Security Release', 3), ('PHP 8.5.12 Released!', 1)])

    def test_php_patch_release_is_priority_one(self):
        got = from_feed('php.net', [item('PHP 8.5.12 Released!')], CUTOFF)
        self.assertEqual([c['score'] for c in got], [1])

    def test_every_node_vulnerability_report_is_flagged(self):
        self.assertEqual(len(from_feed('node', [item('Wednesday, October 21, 2026 Security Releases')], CUTOFF)), 1)

    def test_old_items_are_ignored(self):
        self.assertEqual(from_feed('node', [item('old', hours_ago=100)], CUTOFF), [])

    def test_willison_security_post_flagged_and_off_topic_not(self):
        got = from_feed('willison', [item('eMudhra Intermediate CA Compromise'), item('My obituary for programming')], CUTOFF)
        self.assertEqual([c['title'] for c in got], ['eMudhra Intermediate CA Compromise'])


class TestGhsa(unittest.TestCase):
    def adv(self, summary, pkg, hours_ago=5):
        return {'ghsa_id': 'GHSA-x', 'summary': summary, 'html_url': 'https://github.com/advisories/GHSA-x',
                'published_at': (NOW - timedelta(hours=hours_ago)).isoformat(),
                'vulnerabilities': [{'package': {'name': pkg}}]}

    def score(self, summary, pkg):
        got = from_ghsa([self.adv(summary, pkg)], CUTOFF, WATCH)
        return [c['score'] for c in got]

    def test_watched_package_opens_an_issue_tier(self):
        self.assertEqual(self.score('Next.js: Unauthenticated Remote Code Execution in `use cache`', 'next'), [2])
        self.assertEqual(self.score('Brotli: Out-of-bounds write in the Brotli decoder', 'brotli'), [2])

    def test_package_match_uses_last_segment_of_maven_and_go_names(self):
        self.assertEqual(self.score('Struts: x', 'org.apache.struts:struts2-core'), [2])
        self.assertEqual(self.score('Symfony: x', 'symfony/symfony'), [2])

    def test_strong_keyword_alone_opens_an_issue_tier(self):
        self.assertEqual(self.score('left-pad-ng: supply chain compromise via malicious release', 'left-pad-ng'), [2])

    def test_bare_malicious_is_not_strong(self):
        # Storybook 'allows code from a malicious origin' scored 2 on the bare word in live data
        self.assertEqual(self.score('Storybook: preview allows code from a malicious origin', 'storybook'), [])

    def test_weak_rce_keyword_alone_is_priority_one(self):
        self.assertEqual(self.score('obscure-lib: Unauthenticated Remote Code Execution', 'obscure-lib'), [1])

    def test_noisy_critical_without_signal_is_dropped(self):
        self.assertEqual(self.score('Pillow: Heap buffer overflow in ImagingJpegDecode', 'Pillow'), [])


class TestKev(unittest.TestCase):
    def kev(self, vendor, product, date='2026-10-24', due='2026-11-14', cve='CVE-2026-1000', ransomware='Unknown'):
        return {'vulnerabilities': [{'cveID': cve, 'vendorProject': vendor, 'product': product,
                                     'vulnerabilityName': 'x', 'dateAdded': date, 'dueDate': due,
                                     'knownRansomwareCampaignUse': ransomware}]}

    def scores(self, kev):
        return [c['score'] for c in from_kev(kev, CUTOFF, WATCH, today=NOW)]

    def test_watched_vendor_recent_cve_is_priority_three(self):
        self.assertEqual(self.scores(self.kev('Apache', 'HTTP Server')), [3])

    def test_watched_vendor_old_cve_is_priority_one(self):
        self.assertEqual(self.scores(self.kev('Microsoft', 'Office', cve='CVE-2018-0802')), [1])

    def test_emergency_one_day_due_date_is_priority_three_for_any_vendor(self):
        self.assertEqual(self.scores(self.kev('Obscure', 'Thing', due='2026-10-25')), [3])

    def test_three_day_due_date_is_the_norm_not_urgent(self):
        # 62 of 80 KEV entries in the 2026-10 sample had a 3-day window: it must not mean 'urgent'.
        self.assertEqual(self.scores(self.kev('Obscure', 'Thing', due='2026-10-27')), [])

    def test_ransomware_only_counts_for_a_recent_cve(self):
        self.assertEqual(self.scores(self.kev('Obscure', 'Thing', ransomware='Known')), [3])
        self.assertEqual(self.scores(self.kev('Obscure', 'Thing', ransomware='Known', cve='CVE-2015-1000')), [])

    def test_unwatched_standard_entry_is_ignored(self):
        self.assertEqual(self.scores(self.kev('Obscure', 'Thing')), [])

    def test_vendor_match_is_whole_word(self):
        self.assertEqual(self.scores(self.kev('GitLab', 'GitLab')), [3])  # 'gitlab' is watched
        self.assertEqual(self.scores(self.kev('Gitless', 'Gitless Tool')), [])  # 'git' must not match 'Gitless'

    def test_old_kev_entry_ignored(self):
        self.assertEqual(self.scores(self.kev('Apache', 'HTTP Server', date='2026-09-01')), [])


class TestCalendar(unittest.TestCase):
    def test_each_month_gets_its_own_id(self):
        oct_ = patch_tuesday(datetime(2026, 10, 13, 19, tzinfo=timezone.utc))[0]
        nov = patch_tuesday(datetime(2026, 11, 10, 19, tzinfo=timezone.utc))[0]
        self.assertNotEqual(oct_['id'], nov['id'])  # a constant id would be suppressed as 'seen' after October

    def test_second_tuesday_only(self):
        self.assertEqual(len(patch_tuesday(datetime(2026, 10, 13, 19, tzinfo=timezone.utc))), 1)
        self.assertEqual(patch_tuesday(datetime(2026, 10, 13, 7, tzinfo=timezone.utc)), [])  # before MSRC publishes
        self.assertEqual(patch_tuesday(datetime(2026, 10, 20, 12, tzinfo=timezone.utc)), [])  # third Tuesday
        self.assertEqual(patch_tuesday(datetime(2026, 10, 14, 12, tzinfo=timezone.utc)), [])  # Wednesday


class TestIssueOutput(unittest.TestCase):
    def test_priority_one_alone_does_not_open_an_issue(self):
        low = [candidate('Simon Willison', 't', 'https://x', 'd', 1, 'w')]
        self.assertEqual(issue_candidates(low), [])
        high = low + [candidate('php.net', 't2', 'https://y', 'd', 3, 'w')]
        self.assertEqual(len(issue_candidates(high)), 2)

    def test_hostile_text_cannot_mention_link_or_break_the_table(self):
        evil = 'Hi @octocat see #123 | <script>alert(1)</script> [x](https://evil) `code`'
        body = render([candidate('php.net', evil, 'javascript:alert(1)', '2026-10-25T00:00', 3, evil)])
        self.assertNotIn('@octocat', body)
        self.assertNotIn('#123', body)
        self.assertNotIn('<script', body)
        self.assertNotIn('](', body)
        self.assertNotIn('javascript:', body)
        row = [l for l in body.splitlines() if l.startswith('| 3 ')][0]
        self.assertEqual(row.count('|'), 5)  # pipes in feed text must not add columns


class TestHardening(unittest.TestCase):
    def test_hostile_link_cannot_inject_markdown_or_mentions(self):
        for link in ('https://x.example/a\n\n@victim see #1', 'https://x.example/a b', 'https://x.example/a|b',
                     'https://x.example/a)(https://evil', 'https://x.example/@x'):
            body = render([candidate('GitHub advisory', 'T', link, '2026-10-25T00:00', 2, 'w')])
            self.assertNotIn('victim', body)
            self.assertNotIn('evil', body)
            row = [l for l in body.splitlines() if l.startswith('| 2 ')]
            self.assertEqual(len(row), 1, link)
            self.assertEqual(row[0].count('|'), 5, link)
            self.assertNotIn('x.example', row[0], link)  # unsafe links are dropped, not repaired

    def test_source_errors_are_shown_in_the_issue(self):
        body = render([candidate('php.net', 't', 'https://x', 'd', 3, 'w')], errors=['CISA KEV (ValueError)'])
        self.assertIn('detector blind to these', body)
        self.assertIn('CISA KEV', body)

    def test_good_link_is_kept(self):
        body = render([candidate('Node.js', 'T', 'https://nodejs.org/en/blog/vulnerability/october-2026-security-releases',
                                 '2026-10-25T00:00', 3, 'w')])
        self.assertIn('https://nodejs.org/en/blog/vulnerability/october-2026-security-releases', body)

    def test_bare_urls_in_titles_are_removed(self):
        self.assertNotIn('evil', clean('Free update at https://evil.example/x and www.evil.example'))

    def test_kev_entry_with_malformed_cve_id_is_skipped(self):
        kev = {'vulnerabilities': [{'cveID': 'CVE-2026-1\n@x', 'vendorProject': 'Apache', 'product': 'HTTP Server',
                                    'vulnerabilityName': 'x', 'dateAdded': '2026-10-24', 'dueDate': '2026-10-26'}]}
        self.assertEqual(from_kev(kev, CUTOFF, WATCH, today=NOW), [])

    def test_priority_one_only_run_leaves_state_unchanged(self):
        seen = {}
        low = [candidate('Simon Willison', 't', 'https://x', 'd', 1, 'w')]
        self.assertEqual(select_and_mark(low, seen, NOW), [])
        self.assertEqual(seen, {})

    def test_duplicates_are_collapsed_and_old_state_pruned(self):
        c = candidate('php.net', 't', 'https://x', 'd', 3, 'w')
        seen = {'old': {'source': 's', 'first_seen': (NOW - timedelta(days=120)).isoformat()}}
        issued = select_and_mark([c, c], seen, NOW)
        self.assertEqual(len(issued), 1)
        self.assertIn(c['id'], seen)
        self.assertNotIn('old', seen)


if __name__ == '__main__':
    unittest.main()
