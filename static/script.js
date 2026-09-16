/* ==========================================
   QUILLIFY — Frontend JavaScript
   ========================================== */

const API_BASE = window.location.origin;

// ==========================================
// Markdown to Clean HTML Converter
// ==========================================
function formatLLMOutput(text) {
    if (!text) return '';
    let html = text;

    // Remove thinking tags if present
    html = html.replace(/<think>[\s\S]*?<\/think>/gi, '');

    // Escape HTML entities first
    html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Convert markdown tables to HTML tables
    html = html.replace(/^(\|.+\|)\n(\|[-:\s|]+\|)\n((?:\|.+\|\n?)*)/gm, (match, header, sep, body) => {
        const headerCells = header.split('|').filter(c => c.trim()).map(c =>
            `<th>${c.trim()}</th>`
        ).join('');
        const rows = body.trim().split('\n').map(row => {
            const cells = row.split('|').filter(c => c.trim()).map(c =>
                `<td>${c.trim()}</td>`
            ).join('');
            return `<tr>${cells}</tr>`;
        }).join('');
        return `<table class="llm-table"><thead><tr>${headerCells}</tr></thead><tbody>${rows}</tbody></table>`;
    });

    // Headers → styled divs
    html = html.replace(/^####\s+(.+)$/gm, '<div class="llm-h4">$1</div>');
    html = html.replace(/^###\s+(.+)$/gm, '<div class="llm-h3">$1</div>');
    html = html.replace(/^##\s+(.+)$/gm, '<div class="llm-h2">$1</div>');
    html = html.replace(/^#\s+(.+)$/gm, '<div class="llm-h1">$1</div>');

    // Horizontal rules
    html = html.replace(/^---+$/gm, '<hr class="llm-hr">');

    // Bold text
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic text
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Numbered lists
    html = html.replace(/^(\d+)\.\s+(.+)$/gm, '<li class="llm-oli" value="$1">$2</li>');

    // Bullet lists (- or •)
    html = html.replace(/^[-•]\s+(.+)$/gm, '<li class="llm-uli">$1</li>');

    // Wrap consecutive <li class="llm-oli"> in <ol>
    html = html.replace(/((?:<li class="llm-oli"[^>]*>.*?<\/li>\s*)+)/g,
        '<ol class="llm-list">$1</ol>');

    // Wrap consecutive <li class="llm-uli"> in <ul>
    html = html.replace(/((?:<li class="llm-uli">.*?<\/li>\s*)+)/g,
        '<ul class="llm-list">$1</ul>');

    // Convert line breaks to <br> but not after block elements
    html = html.replace(/\n\n/g, '</p><p class="llm-para">');
    html = html.replace(/\n/g, '<br>');

    // Wrap in paragraph
    html = '<p class="llm-para">' + html + '</p>';

    // Clean up empty paragraphs
    html = html.replace(/<p class="llm-para">\s*<\/p>/g, '');
    html = html.replace(/<p class="llm-para">\s*<br>\s*<\/p>/g, '');

    return html;
}

// ==========================================
// Tab Switching
// ==========================================
function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

// ==========================================
// Word Count
// ==========================================
function updateWordCount(textareaId, countId) {
    const text = document.getElementById(textareaId).value.trim();
    const count = text ? text.split(/\s+/).length : 0;
    document.getElementById(countId).textContent = `${count} words`;
}

// ==========================================
// Button State Helpers
// ==========================================
function setLoading(button, loading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    if (loading) {
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
        button.disabled = true;
    } else {
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
        button.disabled = false;
    }
}

function showError(panelId, message) {
    document.getElementById(panelId).innerHTML = `
        <div class="error-message">
            <span>⚠️</span>
            <span>${message}</span>
        </div>
    `;
}

// ==========================================
// SEO Analyzer
// ==========================================
async function analyzeSEO() {
    const topic = document.getElementById('seo-topic').value.trim();
    const text = document.getElementById('seo-text').value.trim();
    const btn = document.querySelector('#tab-seo .submit-btn');

    if (!topic || !text) {
        showError('seo-output', 'Please fill in both the blog topic and blog content.');
        return;
    }
    if (text.split(/\s+/).length < 50) {
        showError('seo-output', 'Blog content must be at least 50 words.');
        return;
    }

    setLoading(btn, true);
    document.getElementById('seo-output').innerHTML = `
        <div class="empty-state">
            <span class="spinner" style="width:32px;height:32px;border-width:3px;"></span>
            <p style="margin-top:16px;">Analyzing your blog for SEO...</p>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/api/seo`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ blog_text: text, blog_topic: topic })
        });
        const data = await res.json();

        if (data.status === 'success') {
            renderSEOResults(data);
        } else {
            showError('seo-output', data.error || 'Analysis failed.');
        }
    } catch (err) {
        showError('seo-output', 'Failed to connect to server. Make sure the backend is running.');
    } finally {
        setLoading(btn, false);
    }
}

function renderSEOResults(data) {
    const ka = data.keyword_analysis;
    let html = `
        <div class="result-header">
            <span>🔍</span>
            <h3>SEO Analysis: ${data.blog_topic}</h3>
        </div>
        <div class="result-score">
            <span class="score-number">${data.word_count}</span>
            <span class="score-label">Words Analyzed</span>
        </div>

        <div class="result-section">
            <div class="result-section-title">📌 KeyBERT Keywords (Semantic)</div>
            <div class="keyword-grid">
                ${ka.keybert_keywords.map(kw => {
                    const score = ka.keybert_scores[kw];
                    return `<span class="result-badge">${kw} <small>(${score})</small></span>`;
                }).join('')}
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">📊 TF-IDF Keywords (Statistical)</div>
            <div class="keyword-grid">
                ${ka.tfidf_keywords.map(kw => `<span class="result-badge blue">${kw}</span>`).join('')}
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">🤖 AI SEO Analysis</div>
            <div class="llm-output">${formatLLMOutput(data.groq_seo_analysis)}</div>
        </div>
    `;
    document.getElementById('seo-output').innerHTML = html;
}

// ==========================================
// Paragraph Enhancer
// ==========================================
async function enhanceParagraph() {
    const topic = document.getElementById('enhance-topic').value.trim();
    const text = document.getElementById('enhance-text').value.trim();
    const btn = document.querySelector('#tab-enhance .submit-btn');

    if (!topic || !text) {
        showError('enhance-output', 'Please fill in both the topic and paragraph.');
        return;
    }
    if (text.split(/\s+/).length < 10) {
        showError('enhance-output', 'Paragraph must be at least 10 words.');
        return;
    }

    setLoading(btn, true);
    document.getElementById('enhance-output').innerHTML = `
        <div class="empty-state">
            <span class="spinner" style="width:32px;height:32px;border-width:3px;"></span>
            <p style="margin-top:16px;">Enhancing your paragraph...</p>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/api/enhance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, topic: topic })
        });
        const data = await res.json();

        if (data.status === 'success') {
            renderEnhanceResults(data);
        } else {
            showError('enhance-output', data.error || 'Enhancement failed.');
        }
    } catch (err) {
        showError('enhance-output', 'Failed to connect to server. Make sure the backend is running.');
    } finally {
        setLoading(btn, false);
    }
}

function renderEnhanceResults(data) {
    const readability = data.readability;

    // Build synonym cards
    let synonymHtml = '';
    const entries = Object.entries(data.synonym_suggestions);
    if (entries.length > 0) {
        synonymHtml = entries.map(([word, syns]) => `
            <div class="synonym-item">
                <span class="synonym-word">${word}</span>
                <div class="synonym-list">→ ${syns.join(', ')}</div>
            </div>
        `).join('');
    } else {
        synonymHtml = '<p class="llm-para" style="color:var(--text-muted);">No synonym suggestions available.</p>';
    }

    // Readability color
    let readabilityColor = 'green';
    if (readability.score < 50) readabilityColor = 'orange';
    if (readability.score < 30) readabilityColor = 'red';

    let html = `
        <div class="result-header">
            <span>✨</span>
            <h3>Paragraph Enhancement</h3>
        </div>

        <div class="result-score">
            <span class="score-number">${readability.score}</span>
            <div>
                <span class="score-label">${readability.level}</span><br>
                <small style="color:var(--text-muted)">Flesch Reading Ease</small>
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">📚 Synonym Suggestions</div>
            <div class="synonym-grid">${synonymHtml}</div>
        </div>

        <div class="result-section">
            <div class="result-section-title">🤖 AI Enhanced Version</div>
            <div class="llm-output">${formatLLMOutput(data.groq_enhancement)}</div>
        </div>
    `;
    document.getElementById('enhance-output').innerHTML = html;
}

// ==========================================
// Resume Optimizer
// ==========================================
async function optimizeResume() {
    const role = document.getElementById('resume-role').value.trim();
    const text = document.getElementById('resume-text').value.trim();
    const btn = document.querySelector('#tab-resume .submit-btn');

    if (!role || !text) {
        showError('resume-output', 'Please fill in both the target role and resume content.');
        return;
    }
    if (text.split(/\s+/).length < 30) {
        showError('resume-output', 'Resume must be at least 30 words.');
        return;
    }

    setLoading(btn, true);
    document.getElementById('resume-output').innerHTML = `
        <div class="empty-state">
            <span class="spinner" style="width:32px;height:32px;border-width:3px;"></span>
            <p style="margin-top:16px;">Optimizing your resume...</p>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/api/resume`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: text, target_role: role })
        });
        const data = await res.json();

        if (data.status === 'success') {
            renderResumeResults(data);
        } else {
            showError('resume-output', data.error || 'Optimization failed.');
        }
    } catch (err) {
        showError('resume-output', 'Failed to connect to server. Make sure the backend is running.');
    } finally {
        setLoading(btn, false);
    }
}

function renderResumeResults(data) {
    const entities = data.entities;
    const ka = data.keyword_analysis;

    let html = `
        <div class="result-header">
            <span>📄</span>
            <h3>Resume Optimization</h3>
        </div>

        <div class="result-section">
            <div class="result-section-title">🏢 Organizations Found</div>
            <div class="keyword-grid">
                ${entities.organizations.length
                    ? entities.organizations.map(o => `<span class="result-badge blue">${o}</span>`).join('')
                    : '<span style="color:var(--text-muted);font-size:13px;">None detected</span>'}
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">🛠️ Skills Detected</div>
            <div class="keyword-grid">
                ${entities.skills.length
                    ? entities.skills.slice(0, 20).map(s => `<span class="result-badge green">${s}</span>`).join('')
                    : '<span style="color:var(--text-muted);font-size:13px;">None detected</span>'}
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">🔑 Resume Keywords (TF-IDF)</div>
            <div class="keyword-grid">
                ${ka.resume_keywords.map(kw => `<span class="result-badge">${kw}</span>`).join('')}
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">🤖 AI Optimization Analysis</div>
            <div class="llm-output">${formatLLMOutput(data.groq_optimization)}</div>
        </div>
    `;
    document.getElementById('resume-output').innerHTML = html;
}

// ==========================================
// Tone Rewriter
// ==========================================
async function rewriteTone() {
    const tone = document.getElementById('tone-select').value;
    const text = document.getElementById('tone-text').value.trim();
    const btn = document.querySelector('#tab-tone .submit-btn');

    if (!text) {
        showError('tone-output', 'Please enter some text to rewrite.');
        return;
    }
    if (text.split(/\s+/).length < 5) {
        showError('tone-output', 'Text must be at least 5 words.');
        return;
    }

    setLoading(btn, true);
    document.getElementById('tone-output').innerHTML = `
        <div class="empty-state">
            <span class="spinner" style="width:32px;height:32px;border-width:3px;"></span>
            <p style="margin-top:16px;">Rewriting in ${tone} tone...</p>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/api/tone`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, desired_tone: tone })
        });
        const data = await res.json();

        if (data.status === 'success') {
            renderToneResults(data);
        } else {
            showError('tone-output', data.error || 'Rewriting failed.');
        }
    } catch (err) {
        showError('tone-output', 'Failed to connect to server. Make sure the backend is running.');
    } finally {
        setLoading(btn, false);
    }
}

function renderToneResults(data) {
    let html = `
        <div class="result-header">
            <span>🎭</span>
            <h3>Tone Rewriting</h3>
        </div>

        <div class="tone-comparison">
            <div class="tone-card detected">
                <div class="tone-card-label">Detected Tone</div>
                <div class="tone-card-value">${data.detected_tone}</div>
            </div>
            <div class="tone-arrow">→</div>
            <div class="tone-card desired">
                <div class="tone-card-label">Target Tone</div>
                <div class="tone-card-value">${data.desired_tone}</div>
            </div>
        </div>

        <div class="result-section">
            <div class="result-section-title">✍️ Rewritten Text & Analysis</div>
            <div class="llm-output">${formatLLMOutput(data.rewritten_text)}</div>
        </div>
    `;
    document.getElementById('tone-output').innerHTML = html;
}

// ==========================================
// Smooth scroll for nav links
// ==========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.style.borderBottomColor = 'rgba(255,255,255,0.12)';
    } else {
        nav.style.borderBottomColor = 'rgba(255,255,255,0.08)';
    }
});
