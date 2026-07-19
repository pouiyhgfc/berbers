/* ============================================
   Tarifit Cursus — oefening-engine
   Vanilla JS, geen frameworks. Voortgang in localStorage.
   Vraagtypes: mc | fill | translate | match
   ============================================ */

(function () {
  'use strict';

  const STORAGE_KEY = 'tarifit-cursus-progress-v1';

  const isEng = document.documentElement.lang === 'en';
  const i18n = {
    nl: {
      exercises: 'Oefeningen',
      question: 'Vraag',
      check: 'Controleer',
      reveal: 'Toon antwoord',
      placeholder: 'Typ je antwoord.',
      answer_label: 'Antwoord',
      correct: 'Goed.',
      incorrect: 'Niet goed.',
      answer_is: 'Antwoord:',
      correct_answer: 'Het juiste antwoord is',
      of: 'van',
      good: 'goed',
      answered: 'beantwoord',
      retry: 'Opnieuw',
      progress: 'Voortgang wordt opgeslagen in deze browser.',
      type_mc: 'Meerkeuze',
      type_translate: 'Vertalen',
      type_match: 'Koppelen',
      type_fill: 'Invullen',
      result_perfect: 'Alles goed!',
      result_good: 'Goed gedaan!',
      result_ok: 'Blijf oefenen!',
      result_score: 'Score'
    },
    en: {
      exercises: 'Exercises',
      question: 'Question',
      check: 'Check',
      reveal: 'Show answer',
      placeholder: 'Type your answer.',
      answer_label: 'Answer',
      correct: 'Correct.',
      incorrect: 'Incorrect.',
      answer_is: 'Answer:',
      correct_answer: 'The correct answer is',
      of: 'of',
      good: 'correct',
      answered: 'answered',
      retry: 'Retry',
      progress: 'Progress is saved in this browser.',
      type_mc: 'Multiple choice',
      type_translate: 'Translate',
      type_match: 'Match',
      type_fill: 'Fill in',
      result_perfect: 'Perfect!',
      result_good: 'Well done!',
      result_ok: 'Keep practicing!',
      result_score: 'Score'
    }
  };
  function t(key) {
    return isEng ? i18n.en[key] : i18n.nl[key];
  }


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
    input.setAttribute('aria-label', t('answer_label'));

    const submit = pickElement('button', 'exercise-submit', t('check'));
    submit.type = 'button';

    const reveal = pickElement('button', 'exercise-reveal', t('reveal'));
    reveal.type = 'button';

    function check() {
      const accepted = ex.accept || [ex.correct];
      const given = input.value;
      const isCorrect = accepted.some(a => answerMatches(given, a));
      input.disabled = true;
      submit.disabled = true;
      reveal.disabled = true;
      input.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
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
  // Voltooiingscherm
  // ----------------------------------------

  function showCompletion(block, correct, total) {
    const existing = block.querySelector('.exercises-result');
    if (existing) existing.remove();

    const pct = total > 0 ? Math.round(correct / total * 100) : 0;

    let msg;
    if (pct === 100) msg = t('result_perfect');
    else if (pct >= 70) msg = t('result_good');
    else msg = t('result_ok');

    // Kleur bepalen
    const barColor = pct >= 80 ? '#4a7c2a' : pct >= 60 ? '#b85c00' : '#9e1b1e';

    const result = document.createElement('div');
    result.className = 'exercises-result';
    result.innerHTML =
      '<div class="exercises-result-msg">' + msg + '</div>' +
      '<div class="exercises-result-stats">' + t('result_score') + ': ' +
        '<strong>' + correct + '/' + total + '</strong> (' + pct + '%)</div>' +
      '<div class="exercises-result-bar">' +
        '<div class="exercises-result-bar-fill" style="width:' + pct + '%;background:' + barColor + '"></div>' +
      '</div>';

    // Invoegen vóór de acties-footer
    const actions = block.querySelector('.exercises-actions');
    if (actions) {
      block.insertBefore(result, actions);
    } else {
      block.appendChild(result);
    }

    // Scroll zacht naar resultaat
    setTimeout(() => result.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50);
  }

  // ----------------------------------------
  // Hoofdlogica per oefening-blok
  // ----------------------------------------

  function buildExercise(ex, idx, lessonId, onProgress) {
    const article = pickElement('article', 'exercise');
    article.dataset.idx = String(idx);

    // Vraagnummer + type-badge
    const numRow = pickElement('div', 'exercise-num-row');
    const num = pickElement('span', 'exercise-num', t('question') + ' ' + (idx + 1));
    const typeLabels = {
      mc: t('type_mc'),
      translate: t('type_translate'),
      match: t('type_match'),
      fill: t('type_fill')
    };
    const badge = pickElement('span', 'exercise-type-badge', typeLabels[ex.type] || ex.type);
    numRow.appendChild(num);
    numRow.appendChild(badge);
    article.appendChild(numRow);

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
        html = '<strong>' + t('correct') + '</strong>';
        if (ex.explain) html += ' ' + ex.explain;
      } else if (revealed) {
        html = '<strong>' + t('answer_is') + '</strong> <span class="tar">' + escapeHtml(expected) + '</span>.';
        if (ex.explain) html += ' ' + ex.explain;
      } else {
        html = '<strong>' + t('incorrect') + '</strong> ';
        if (expected) {
          html += t('correct_answer') + ' <span class="tar">' + escapeHtml(expected) + '</span>.';
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

  function setupBlock(block, exercises) {
    const lessonId = block.dataset.lesson;
    if (!Array.isArray(exercises) || !exercises.length) return;

    // Header
    const header = pickElement('div', 'exercises-header');
    const h3 = pickElement('h3', null, t('exercises'));
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
      progressEl.innerHTML = '<strong>' + correct + '</strong> ' + t('of') + ' ' + total + ' ' + t('good') + ' — ' + answered + '/' + total + ' ' + t('answered');
      // Persist
      const all = loadProgress();
      all[lessonId] = { results: results, ts: Date.now() };
      saveProgress(all);
      // Voltooiingscherm zodra alle vragen beantwoord zijn
      if (answered === total) {
        showCompletion(block, correct, total);
      }
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
    summary.innerHTML = t('progress');
    const reset = pickElement('button', 'exercise-reset', t('retry'));
    reset.type = 'button';
    reset.addEventListener('click', () => {
      clearLessonProgress(lessonId);
      // Reset zonder pagina-reload — wis en herbouw het blok
      block.innerHTML = '';
      setupBlock(block, exercises);
    });
    actions.appendChild(summary);
    actions.appendChild(reset);
    block.appendChild(actions);
  }

  async function init() {
    const blocks = document.querySelectorAll('.exercises[data-lesson]');
    if (!blocks.length) return;

    const lang = isEng ? 'en' : 'nl';
    const jsonUrl = '/assets/oefeningen/exercises-' + lang + '.json';

    let allExercises = null;
    try {
      const res = await fetch(jsonUrl);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      allExercises = await res.json();
    } catch (_) {
      // Fallback: lees inline JSON als externe fetch mislukt (legacy/offline)
      blocks.forEach(block => {
        const dataScript = block.querySelector('script[type="application/json"]');
        if (!dataScript) return;
        try { setupBlock(block, JSON.parse(dataScript.textContent)); } catch (_) {}
      });
      return;
    }

    blocks.forEach(block => {
      const exercises = allExercises[block.dataset.lesson];
      if (exercises) setupBlock(block, exercises);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
