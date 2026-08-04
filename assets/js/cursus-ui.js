// ==============================================================
// cursus-ui.js — UI-gedrag voor de gegenereerde cursuspagina's (nl/blok-N.html,
// en/blok-N.html; plan/BOUWPLAN-CURSUS-UITVOERING.md fase F7).
//
// Drie dingen, alle drie zonder framework, alle drie stil falend als iets ontbreekt:
//  1. Scrollspy — welke les-sectie is zichtbaar, markeer de bijbehorende sidebar-link met
//     zowel .active (bestaande CSS) als aria-current="true" (toegankelijkheid).
//  2. Voortgang per les in de sidebar — leest dezelfde localStorage-sleutel als de
//     oefening-engine (cursus.js: 'tarifit-cursus-progress-v1') en zet een klein bolletje
//     achter elke lesson-link. Ververst ook live via het 'tarifit-progress-updated'-event
//     dat cursus.js dispatcht na elk antwoord.
//  3. <details>-standen onthouden (kernwoorden "meer", verdieping-blokken) per pad, zodat
//     een open paneel open blijft bij een volgend bezoek aan dezelfde pagina.
// ==============================================================

(function () {
  'use strict';

  var PROGRESS_KEY = 'tarifit-cursus-progress-v1'; // moet gelijk blijven aan cursus.js
  var DETAILS_KEY = 'tarifit-cursus-details-v1';

  // --------------------------------------------------------------
  // 1. Scrollspy
  // --------------------------------------------------------------
  var links = document.querySelectorAll('.sidebar a');
  var sections = document.querySelectorAll('.content section');

  if (links.length && sections.length && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.remove('active');
          l.removeAttribute('aria-current');
        });
        var link = document.querySelector('.sidebar a[href="#' + e.target.id + '"]');
        if (!link) return;
        link.classList.add('active');
        link.setAttribute('aria-current', 'true');
        if (window.innerWidth <= 900) {
          var nav = document.getElementById('sidebar-nav');
          if (nav && nav.getBoundingClientRect) {
            var lRect = link.getBoundingClientRect();
            var nRect = nav.getBoundingClientRect();
            if (lRect.top < nRect.top || lRect.bottom > nRect.bottom) {
              link.scrollIntoView({ block: 'nearest' });
            }
          }
        }
      });
    }, { rootMargin: '-100px 0px -60% 0px' });
    sections.forEach(function (s) { observer.observe(s); });
  }

  // Mobiele sidebar-toggle (ongewijzigd overgenomen uit het sjabloon).
  var sidebar = document.getElementById('sidebar');
  var toggle = document.getElementById('sidebar-toggle');
  var nav = document.getElementById('sidebar-nav');
  if (sidebar && toggle && nav) {
    function isMobile() { return window.innerWidth <= 900; }
    toggle.addEventListener('click', function () {
      var open = sidebar.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function () {
        if (isMobile()) {
          sidebar.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  // --------------------------------------------------------------
  // 2. Voortgang per les in de sidebar
  // --------------------------------------------------------------
  function loadProgress() {
    try {
      var raw = localStorage.getItem(PROGRESS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function renderProgressDots() {
    var progress = loadProgress();
    document.querySelectorAll('.sidebar a[href*="les-"], .overzicht-les-link[href*="les-"]').forEach(function (a) {
      var m = (a.getAttribute('href') || '').match(/(les-\d+)/);
      if (!m) return;
      var entry = progress[m[1]];
      var existing = a.querySelector('.sidebar-progress-dot');
      if (existing) existing.remove();
      if (!entry || !Array.isArray(entry.results) || !entry.results.length) return;
      var total = entry.results.length;
      var done = entry.results.filter(function (r) { return r !== null; }).length;
      if (done === 0) return;
      var correct = entry.results.filter(function (r) { return r === true; }).length;
      var dot = document.createElement('span');
      dot.className = 'sidebar-progress-dot';
      if (done === total) dot.classList.add(correct === total ? 'is-perfect' : 'is-done');
      else dot.classList.add('is-partial');
      a.appendChild(dot);
    });
  }
  renderProgressDots();

  // Overzichtspagina (nl/cursus.html, en/course.html): totale voortgang over alle lessen
  // met een localStorage-entry, gebaseerd op dezelfde progress-data als de dots hierboven.
  function renderVoortgangSamenvatting() {
    var container = document.querySelector('[data-overzicht-voortgang]');
    if (!container) return;
    var progress = loadProgress();
    var lessen = Object.keys(progress);
    if (!lessen.length) {
      container.innerHTML = '';
      return;
    }
    var totalLessen = lessen.length;
    var totalVragen = 0, totalGoed = 0, totalBeantwoord = 0;
    lessen.forEach(function (key) {
      var r = progress[key].results || [];
      totalVragen += r.length;
      totalBeantwoord += r.filter(function (x) { return x !== null; }).length;
      totalGoed += r.filter(function (x) { return x === true; }).length;
    });
    var pct = totalBeantwoord > 0 ? Math.round((totalGoed / totalBeantwoord) * 100) : 0;
    var isEng = document.documentElement.lang === 'en';
    var label = isEng
      ? totalLessen + ' lesson(s) started · ' + totalGoed + '/' + totalBeantwoord + ' correct (' + pct + '%)'
      : totalLessen + ' les(sen) gestart · ' + totalGoed + '/' + totalBeantwoord + ' goed (' + pct + '%)';
    container.innerHTML = '<div class="overzicht-voortgang-balk"><div class="overzicht-voortgang-balk-fill" style="width:' + pct + '%"></div></div>' +
      '<div class="overzicht-voortgang-label">' + label + '</div>';
  }
  renderVoortgangSamenvatting();
  window.addEventListener('tarifit-progress-updated', renderVoortgangSamenvatting);
  window.addEventListener('tarifit-progress-updated', renderProgressDots);
  window.addEventListener('storage', function (e) {
    if (e.key === PROGRESS_KEY) renderProgressDots();
  });

  // --------------------------------------------------------------
  // 3. <details>-standen onthouden
  // --------------------------------------------------------------
  function loadDetailsState() {
    try {
      return JSON.parse(localStorage.getItem(DETAILS_KEY) || '{}');
    } catch (e) {
      return {};
    }
  }
  function saveDetailsState(state) {
    try {
      localStorage.setItem(DETAILS_KEY, JSON.stringify(state));
    } catch (e) { /* localStorage kan vol/geblokkeerd zijn — stille fallback */ }
  }

  var state = loadDetailsState();
  var pageKey = location.pathname;
  document.querySelectorAll('.content details').forEach(function (el, idx) {
    var key = pageKey + '#' + idx;
    if (state[key]) el.open = true;
    el.addEventListener('toggle', function () {
      var cur = loadDetailsState();
      cur[key] = el.open;
      saveDetailsState(cur);
    });
  });
})();
