/* ============================================
   Tarifit Cursus — oefening-engine
   Vanilla JS, geen frameworks. Voortgang in localStorage.
   Vraagtypes: mc | fill | translate | match
   ============================================ */

(function () {
  'use strict';

  const STORAGE_KEY = 'tarifit-cursus-progress-v1';

  function loadProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveProgress(progress) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch (e) {
      /* localStorage kan vol of geblokkeerd zijn — stille fallback */
    }
  }

  function clearLessonProgress(lessonId) {
    const progress = loadProgress();
    delete progress[lessonId];
    saveProgress(progress);
  }

  /**
   * Normaliseer een antwoord voor vergelijking:
   * - lowercase
   * - trim + verminder whitespace
   * - NFC unicode (precomposed)
   * - geen leesteken-eindes
   */
  function normalizeAnswer(s) {
    return String(s || '')
      .normalize('NFC')
      .toLowerCase()
      .trim()
      .replace(/\s+/g, ' ')
      .replace(/[.!?,;:]+$/, '');
  }

  function answerMatches(given, expected) {
    return normalizeAnswer(given) === normalizeAnswer(expected);
  }

  function pickElement(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  }

  // ----------------------------------------
  // Renderer per vraagtype
  // ----------------------------------------

  function renderMc(article, ex, onResult) {
    const list = pickElement('ul', 'exercise-options');
    list.setAttribute('role', 'radiogroup');

    ex.options.forEach((optHtml, idx) => {
      const li = document.createElement('li');
      const btn = pickElement('button', 'exercise-opt');
      btn.type = 'button';
      btn.innerHTML = optHtml;
      btn.dataset.idx = String(idx);
      btn.setAttribute('role', 'radio');
      btn.addEventListener('click', () => {
        const isCorrect = idx === ex.correct;
        // Disable alle opties
        list.querySelectorAll('.exercise-opt').forEach(b => {
          b.disabled = true;
          const i = Number(b.dataset.idx);
          if (i === ex.correct) b.classList.add('is-correct');
          if (i === idx && !isCorrect) b.classList.add('is-wrong');
        });
        onResult(isCorrect, ex.options[ex.correct]);
      });
      li.appendChild(btn);
      list.appendChild(li);
    });

    article.appendChild(list);
  }

  function renderInput(article, ex, onResult) {
    const row = pickElement('div', 'exercise-input-row');
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'exercise-input';
    input.autocomplete = 'off';
    input.autocapitalize = 'off';
    input.spellcheck = false;
    input.placeholder = ex.placeholder || 'Typ je antwoord…';
    input.setAttribute('aria-label', 'Antwoord');

    const submit = pickElement('button', 'exercise-submit', 'Controleer');
    submit.type = 'button';

    const reveal = pickElement('button', 'exercise-reveal', 'Toon antwoord');
    reveal.type = 'button';

    function check() {
      const accepted = ex.accept || [ex.correct];
      const given = input.value;
      const isCorrect = accepted.some(a => answerMatches(given, a));
      input.disabled = true;
      submit.disabled = true;
      reveal.disabled = true;
      input.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
      if (!isCorrect && !given.trim()) {
        // Leeg ingeleverd — toon antwoord meteen
      }
      onResult(isCorrect, ex.correct);
    }

    function showAnswer() {
      input.value = ex.correct;
      input.disabled = true;
      submit.disabled = true;
      reveal.disabled = true;
      input.classList.add('is-wrong');
      onResult(false, ex.correct, true);
    }

    submit.addEventListener('click', check);
    reveal.addEventListener('click', showAnswer);
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        check();
      }
    });

    row.appendChild(input);
    row.appendChild(submit);
    row.appendChild(reveal);
    article.appendChild(row);
  }

  function renderMatch(article, ex, onResult) {
    /**
     * ex.pairs: [{left, right, leftIsTar, rightIsTar}]
     * Klik 1× links, klik 1× rechts → koppeling.
     * Goede koppelingen blijven groen; foute koppelingen tonen even rood en resetten.
     */
    const pairs = ex.pairs;
    const leftItems = pairs.map((p, i) => ({ id: 'L' + i, text: p.left, isTar: p.leftIsTar }));
    const rightItems = shuffle(pairs.map((p, i) => ({ id: 'R' + i, text: p.right, isTar: p.rightIsTar, pairIdx: i })));

    const wrap = pickElement('div', 'exercise-match');
    const colL = pickElement('div', 'exercise-match-col');
    const colR = pickElement('div', 'exercise-match-col');

    let selected = null; // { side: 'L'|'R', el, idx }
    let resolved = 0;
    let attempts = 0;
    let mistakes = 0;

    function makeBtn(item, side, idx) {
      const btn = pickElement('button', 'exercise-match-item');
      btn.type = 'button';
      btn.innerHTML = item.text;
      btn.dataset.side = side;
      btn.dataset.idx = String(idx);
      if (item.isTar) btn.classList.add('is-tar');

      btn.addEventListener('click', () => {
        if (btn.classList.contains('is-paired')) return;
        if (selected && selected.el === btn) {
          btn.classList.remove('is-selected');
          selected = null;
          return;
        }
        if (selected && selected.side === side) {
          selected.el.classList.remove('is-selected');
          selected = null;
        }
        if (!selected) {
          btn.classList.add('is-selected');
          selected = { side, el: btn, idx, item };
          return;
        }

        // We hebben nu één links + één rechts geselecteerd
        const leftSel = selected.side === 'L' ? selected : { side, el: btn, idx, item };
        const rightSel = selected.side === 'R' ? selected : { side, el: btn, idx, item };

        attempts += 1;
        const correct = leftSel.idx === rightSel.item.pairIdx;

        if (correct) {
          leftSel.el.classList.remove('is-selected');
          rightSel.el.classList.remove('is-selected');
          leftSel.el.classList.add('is-correct', 'is-paired');
          rightSel.el.classList.add('is-correct', 'is-paired');
          leftSel.el.disabled = true;
          rightSel.el.disabled = true;
          resolved += 1;
          if (resolved === pairs.length) {
            // Alle paren goed — eindresultaat
            const allFirstTry = mistakes === 0;
            onResult(allFirstTry, null);
          }
        } else {
          mistakes += 1;
          // Flits beide rood, reset na 700ms
          leftSel.el.classList.add('is-wrong');
          rightSel.el.classList.add('is-wrong');
          setTimeout(() => {
            leftSel.el.classList.remove('is-wrong', 'is-selected');
            rightSel.el.classList.remove('is-wrong', 'is-selected');
          }, 700);
        }
        selected = null;
      });

      return btn;
    }

    leftItems.forEach((it, i) => colL.appendChild(makeBtn(it, 'L', i)));
    rightItems.forEach((it, i) => colR.appendChild(makeBtn(it, 'R', i)));

    wrap.appendChild(colL);
    wrap.appendChild(colR);
    article.appendChild(wrap);
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // ----------------------------------------
  // Hoofdlogica per oefening-blok
  // ----------------------------------------

  function buildExercise(ex, idx, lessonId, onProgress) {
    const article = pickElement('article', 'exercise');
    article.dataset.idx = String(idx);

    const num = pickElement('div', 'exercise-num', 'Vraag ' + (idx + 1));
    article.appendChild(num);

    const prompt = pickElement('div', 'exercise-prompt');
    prompt.innerHTML = ex.q;
    article.appendChild(prompt);

    const feedback = pickElement('div', 'exercise-feedback');
    feedback.setAttribute('role', 'status');
    feedback.setAttribute('aria-live', 'polite');

    function onResult(isCorrect, expected, revealed) {
      article.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
      feedback.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
      let html;
      if (isCorrect) {
        html = '<strong>Goed.</strong>';
        if (ex.explain) html += ' ' + ex.explain;
      } else if (revealed) {
        html = '<strong>Antwoord:</strong> <span class="tar">' + escapeHtml(expected) + '</span>.';
        if (ex.explain) html += ' ' + ex.explain;
      } else {
        html = '<strong>Niet goed.</strong> ';
        if (expected) {
          html += 'Het juiste antwoord is <span class="tar">' + escapeHtml(expected) + '</span>.';
        }
        if (ex.explain) html += ' ' + ex.explain;
      }
      feedback.innerHTML = html;
      onProgress(idx, isCorrect);
    }

    if (ex.type === 'mc') renderMc(article, ex, onResult);
    else if (ex.type === 'fill' || ex.type === 'translate') renderInput(article, ex, onResult);
    else if (ex.type === 'match') renderMatch(article, ex, onResult);

    article.appendChild(feedback);
    return article;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function setupBlock(block) {
    const lessonId = block.dataset.lesson;
    const dataScript = block.querySelector('script[type="application/json"]');
    if (!dataScript) {
      console.warn('Oefening-blok zonder data-script overgeslagen', block);
      return;
    }
    let exercises;
    try {
      exercises = JSON.parse(dataScript.textContent);
    } catch (e) {
      console.error('Ongeldige JSON in oefening-blok', lessonId, e);
      return;
    }
    if (!Array.isArray(exercises) || !exercises.length) return;

    // Header
    const header = pickElement('div', 'exercises-header');
    const h3 = pickElement('h3', null, 'Oefeningen');
    const progressEl = pickElement('div', 'exercises-progress');
    header.appendChild(h3);
    header.appendChild(progressEl);
    block.appendChild(header);

    // State
    const total = exercises.length;
    const results = new Array(total).fill(null); // null | true | false

    function updateProgress() {
      const answered = results.filter(r => r !== null).length;
      const correct = results.filter(r => r === true).length;
      progressEl.innerHTML = '<strong>' + correct + '</strong> van ' + total + ' goed · ' + answered + '/' + total + ' beantwoord';
      // Persist
      const all = loadProgress();
      all[lessonId] = { results: results, ts: Date.now() };
      saveProgress(all);
    }
    updateProgress();

    // Build elke oefening
    exercises.forEach((ex, idx) => {
      const article = buildExercise(ex, idx, lessonId, (i, ok) => {
        results[i] = ok;
        updateProgress();
      });
      block.appendChild(article);
    });

    // Footer met reset
    const actions = pickElement('div', 'exercises-actions');
    const summary = pickElement('div', 'exercise-summary');
    summary.innerHTML = 'Voortgang wordt opgeslagen in deze browser.';
    const reset = pickElement('button', 'exercise-reset', 'Opnieuw');
    reset.type = 'button';
    reset.addEventListener('click', () => {
      clearLessonProgress(lessonId);
      // Eenvoudigste reset — herlaad de pagina
      window.location.reload();
    });
    actions.appendChild(summary);
    actions.appendChild(reset);
    block.appendChild(actions);
  }

  function init() {
    const blocks = document.querySelectorAll('.exercises[data-lesson]');
    blocks.forEach(setupBlock);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
