/**
 * QuizEngine — Shared quiz logic for FixTheVuln certification practice tests.
 * Each quiz page calls QuizEngine.init(config) with cert-specific settings.
 */
const QuizEngine = (() => {
    let questions = [];
    let fallbackQuestions = [];
    let DOMAIN_INFO = {};
    let currentQuiz = [];
    let currentQuestion = 0;
    let quizSize = 10;
    let score = 0;
    let answered = 0;
    let selectedDomain = 'all';
    let selectedDifficulty = 'mixed';
    let selectedCount = 10;
    let startTime = null;
    let timerInterval = null;
    let config = {};

    function shuffleArray(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    async function loadQuestions() {
        try {
            const resp = await fetch(config.jsonPath);
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            const data = await resp.json();
            if (data.questions && data.questions.length > 0) {
                questions = data.questions;
                document.getElementById('question-pool-info').textContent =
                    questions.length + ' questions loaded — ' + config.examCode + ' mapped';
            }
        } catch (e) {
            console.warn('Using fallback questions:', e.message);
            questions = fallbackQuestions;
            document.getElementById('question-pool-info').textContent =
                fallbackQuestions.length + ' questions available (fallback)';
        }
    }

    function bindButtons() {
        document.querySelectorAll('.category-select .category-btn[data-domain]').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.closest('.category-select').querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedDomain = btn.dataset.domain;
            });
        });
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedDifficulty = btn.dataset.difficulty;
            });
        });
        document.querySelectorAll('#count-select .category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('#count-select .category-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedCount = parseInt(btn.dataset.count, 10);
            });
        });
    }

    function weightedRandomSelect(pool, count) {
        if (selectedDomain !== 'all') return shuffleArray(pool).slice(0, count);
        const byDomain = {};
        pool.forEach(q => { const d = q.domain || 1; if (!byDomain[d]) byDomain[d] = []; byDomain[d].push(q); });
        const result = [];
        const totalWeight = Object.values(DOMAIN_INFO).reduce((s, d) => s + d.weight, 0);
        for (const [dom, info] of Object.entries(DOMAIN_INFO)) {
            const domQuestions = shuffleArray(byDomain[dom] || []);
            const allocation = Math.round(count * info.weight / totalWeight);
            result.push(...domQuestions.slice(0, allocation));
        }
        const picked = new Set(result.map(q => q.id));
        if (result.length < count) {
            const remaining = shuffleArray(pool.filter(q => !picked.has(q.id)));
            result.push(...remaining.slice(0, count - result.length));
        }
        return shuffleArray(result).slice(0, count);
    }

    function startQuiz() {
        let filtered = questions.filter(q => {
            const domainMatch = selectedDomain === 'all' || String(q.domain) === selectedDomain;
            const difficultyMatch = selectedDifficulty === 'mixed' || q.difficulty === selectedDifficulty;
            return domainMatch && difficultyMatch;
        });
        quizSize = Math.min(selectedCount, filtered.length);
        if (quizSize === 0) { quizSize = Math.min(selectedCount, questions.length); filtered = questions; }
        currentQuiz = weightedRandomSelect(filtered, quizSize);
        currentQuestion = 0; score = 0; answered = 0; startTime = Date.now();
        document.getElementById('total-questions').textContent = quizSize;
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('quiz-screen').style.display = 'block';
        document.getElementById('results-screen').classList.remove('show');
        timerInterval = setInterval(updateTimer, 1000);
        displayQuestion();
    }

    function updateTimer() {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        const timerEl = document.getElementById('timer');
        timerEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        if (elapsed > 300) timerEl.classList.add('warning');
    }

    function getDomainLabel(domain) {
        const d = DOMAIN_INFO[domain];
        return d ? 'Domain ' + domain + ': ' + d.name : 'Domain ' + domain;
    }

    function displayQuestion() {
        const q = currentQuiz[currentQuestion];
        const container = document.getElementById('question-container');
        const letters = ['A', 'B', 'C', 'D'];
        const domainBadge = q.domain ? `<span class="question-category">${getDomainLabel(q.domain)}</span>` : '';
        const optionsHTML = q.options.map((opt, i) => `
            <div class="option" data-index="${i}" onclick="QuizEngine.selectOption(${i})">
                <span class="option-letter">${letters[i]}</span>
                <span>${opt}</span>
            </div>
        `).join('');
        container.innerHTML = `
            <div class="question-card">
                <span class="question-number">Question ${currentQuestion + 1}/${quizSize}</span>
                ${domainBadge}
                <p class="question-text">${q.question}</p>
                <div class="options-list">${optionsHTML}</div>
                <div class="explanation" id="explanation">
                    <h4>Explanation</h4>
                    <p>${q.explanation}</p>
                    ${q.link ? `<p><a href="${q.link}">Learn more &rarr;</a></p>` : ''}
                </div>
            </div>
        `;
        document.getElementById('current-question').textContent = currentQuestion + 1;
        document.getElementById('progress-fill').style.width = ((currentQuestion + 1) / quizSize * 100) + '%';
        document.getElementById('skip-btn').style.display = 'inline-block';
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('finish-btn').style.display = 'none';
    }

    function selectOption(index) {
        const options = document.querySelectorAll('.option');
        if (options[0].classList.contains('disabled')) return;
        const q = currentQuiz[currentQuestion];
        const correct = q.correct;
        options.forEach((opt, i) => {
            opt.classList.add('disabled');
            if (i === index) opt.classList.add('selected');
            if (i === correct) opt.classList.add('correct');
            else if (i === index && index !== correct) opt.classList.add('incorrect');
        });
        if (index === correct) score++;
        answered++;
        document.getElementById('score').textContent = score;
        document.getElementById('answered').textContent = answered;
        document.getElementById('explanation').classList.add('show');
        document.getElementById('skip-btn').style.display = 'none';
        if (currentQuestion < quizSize - 1) document.getElementById('next-btn').style.display = 'inline-block';
        else document.getElementById('finish-btn').style.display = 'inline-block';
    }

    function skipQuestion() {
        answered++;
        document.getElementById('answered').textContent = answered;
        nextQuestion();
    }

    function nextQuestion() {
        currentQuestion++;
        if (currentQuestion < quizSize) displayQuestion(); else showResults();
    }

    function showResults() {
        clearInterval(timerInterval);
        const percentage = Math.round((score / quizSize) * 100);
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        let grade, message;
        if (percentage >= 90) { grade = 'Expert!'; message = 'Outstanding! You have excellent knowledge.'; }
        else if (percentage >= 70) { grade = 'Proficient'; message = 'Great job! You have solid fundamentals.'; }
        else if (percentage >= 50) { grade = 'Learning'; message = 'Good effort! Review the topics you missed.'; }
        else { grade = 'Keep Studying'; message = 'Check out our learning path to build your knowledge.'; }
        document.getElementById('final-score').textContent = percentage + '%';
        document.getElementById('grade').textContent = grade;
        document.getElementById('grade-message').textContent = message;
        document.getElementById('correct-count').textContent = score;
        document.getElementById('incorrect-count').textContent = quizSize - score;
        document.getElementById('time-taken').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        const shareText = config.shareText.replace('{percentage}', percentage).replace('{quizSize}', quizSize);
        const shareUrl = encodeURIComponent(config.shareUrl);
        document.getElementById('share-twitter').href = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${shareUrl}`;
        document.getElementById('share-linkedin').href = `https://www.linkedin.com/sharing/share-offsite/?url=${shareUrl}`;
        document.getElementById('quiz-screen').style.display = 'none';
        document.getElementById('results-screen').classList.add('show');
        saveQuizResult(percentage, elapsed);
        displayHistory();
    }

    function restartQuiz() {
        document.getElementById('results-screen').classList.remove('show');
        document.getElementById('start-screen').style.display = 'block';
    }

    function saveQuizResult(sc, time) {
        const key = config.storageKey;
        const history = JSON.parse(localStorage.getItem(key) || '[]');
        history.unshift({ score: sc, time, domain: selectedDomain, difficulty: selectedDifficulty, count: quizSize, date: new Date().toISOString() });
        localStorage.setItem(key, JSON.stringify(history.slice(0, 10)));
    }

    function displayHistory() {
        const key = config.storageKey;
        const history = JSON.parse(localStorage.getItem(key) || '[]');
        const container = document.getElementById('quiz-history');
        if (history.length === 0) {
            container.innerHTML = '<p style="color: #666;">No quiz history yet. Take a quiz to track your progress!</p>';
            return;
        }
        const rows = history.slice(0, 5).map(h => {
            const date = new Date(h.date).toLocaleDateString();
            const minutes = Math.floor(h.time / 60);
            const seconds = h.time % 60;
            const domainLabel = h.domain === 'all' ? 'All' : ('D' + h.domain);
            return `<tr><td>${date}</td><td><strong>${h.score}%</strong></td><td>${minutes}:${seconds.toString().padStart(2, '0')}</td><td>${domainLabel}</td><td>${h.count || 10}q</td></tr>`;
        }).join('');
        container.innerHTML = `<table class="styled-table" style="margin: 0;"><thead><tr><th>Date</th><th>Score</th><th>Time</th><th>Domain</th><th>Size</th></tr></thead><tbody>${rows}</tbody></table>`;
    }

    function init(cfg) {
        config = cfg;
        DOMAIN_INFO = cfg.domains;
        fallbackQuestions = cfg.fallbackQuestions || [];
        questions = fallbackQuestions;
        loadQuestions();
        bindButtons();
        displayHistory();
    }

    return {
        init,
        startQuiz,
        selectOption,
        skipQuestion,
        nextQuestion,
        showResults,
        restartQuiz,
        displayHistory
    };
})();
