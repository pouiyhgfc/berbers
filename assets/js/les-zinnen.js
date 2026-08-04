// ==============================================================
// les-zinnen.js — "Uit het boek"-blok per les (runtime-injectie)
//
// PLAN-ZINNEN-WEBSITE.md stap 3.2. Geladen onderaan nl/cursus.html en en/cursus.html.
// Fetcht assets/zinnen/zinnen.csv één keer, bouwt een index les -> zinnen, en injecteert
// per section[id^="les-"] met >=1 bijbehorende zin een blok aan het eind van de sectie.
// Lessen zonder zinnen krijgen niets. Faalt de fetch, dan verschijnt er stil niets — de
// cursus mag nooit breken op de zinnenbank. Gebruikt parseCSV/normalize/escapeHtml/
// fetchTarifitCSV uit tarifit-search.js (moet vóór dit bestand geladen zijn).
//
// Exporteert ook window.tarifitZinnenReady — een Promise die resolvet naar een
// zin-id -> {tarifit, nl} index van dezelfde CSV-fetch. cursus.js (oefening-engine, type
// "ordenen") gebruikt die om de bronzin bij een zin_id op te halen zonder een tweede fetch
// en zonder de zin zelf in exercises-nl.json te hoeven zetten (§8 van het cursusbouwplan).
// ==============================================================

(function () {
  var MAX_PER_LES = 5;
  var resolveZinnenReady;
  window.tarifitZinnenReady = new Promise(function (resolve) { resolveZinnenReady = resolve; });
  var LANG = document.documentElement.lang === 'en' ? 'en' : 'nl';
  var LABELS = LANG === 'en'
    ? { heading: 'From the book', more: 'more on the sentences page', fallback: 'NL' }
    : { heading: 'Uit het boek', more: 'meer op de zinnenpagina', fallback: 'EN' };
  var ZINNEN_PAGE = LANG === 'en' ? 'zinnen.html' : 'zinnen.html';

  function pageNum(bron) {
    var m = (bron || '').match(/(\d+)/);
    return m ? parseInt(m[1], 10) : 999999;
  }

  function extractTag(tags, name) {
    var m = tags.match(new RegExp(name + ':([^;]+)'));
    return m ? m[1].trim() : '';
  }

  function buildLesIndex(rows) {
    // kolommen: 0 tarifit · 1 nl · 2 en · 3 gloss · 4 hoofdstuk · 5 les · 6 bron · 7 tags
    var byLes = {};
    var dataRows = rows.slice(1);
    dataRows.forEach(function (r) {
      var tarifit = (r[0] || '').trim();
      if (!tarifit) return;
      var lesValue = (r[5] || '').trim();
      if (!lesValue) return;
      var nl = (r[1] || '').trim();
      var en = (r[2] || '').trim();
      var bron = (r[6] || '').trim();
      var tags = (r[7] || '').trim();
      var translation = LANG === 'en' ? (en || nl) : (nl || en);
      var usedFallback = LANG === 'en' ? (!en && !!nl) : (!nl && !!en);
      var entry = {
        tarifit: tarifit, translation: translation, usedFallback: usedFallback,
        bron: bron, idTag: extractTag(tags, 'id'), pageNum: pageNum(bron),
      };
      lesValue.split(';').forEach(function (les) {
        les = les.trim();
        if (!les) return;
        var key = 'les-' + (les.length === 1 ? '0' + les : les);
        (byLes[key] = byLes[key] || []).push(entry);
      });
    });
    Object.keys(byLes).forEach(function (key) {
      byLes[key].sort(function (a, b) {
        return a.pageNum - b.pageNum || a.idTag.localeCompare(b.idTag);
      });
    });
    return byLes;
  }

  function buildIdIndex(rows) {
    // kolommen: 0 tarifit · 1 nl · 2 en · 7 tags (bevat "id:pNNN-NN")
    var byId = {};
    rows.slice(1).forEach(function (r) {
      var tarifit = (r[0] || '').trim();
      var tags = (r[7] || '').trim();
      var id = extractTag(tags, 'id');
      if (!tarifit || !id) return;
      byId[id] = { tarifit: tarifit, nl: (r[1] || '').trim(), en: (r[2] || '').trim() };
    });
    return byId;
  }

  // Inline styles i.p.v. een CSS-wijziging in styles.css of cursus.html — gebruikt de
  // bestaande globale custom properties, geen nieuwe klassen nodig in het stylesheet.
  var STYLE = {
    block: 'margin-top:32px;padding:16px 20px;border:1px solid var(--rule);border-radius:4px;background:var(--bg-warm);',
    heading: 'font-family:var(--font-display);font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;',
    list: 'list-style:none;margin:0;padding:0;',
    line: 'padding:5px 0;font-size:15px;line-height:1.5;',
    tarifit: 'font-family:var(--font-serif);color:var(--accent);font-weight:500;',
    vertaling: 'color:var(--text);',
    fallback: 'font-size:10px;letter-spacing:.05em;color:var(--text-muted);border:1px solid var(--rule);border-radius:2px;padding:0 4px;margin-left:2px;',
    bron: 'font-size:12px;color:var(--text-muted);',
    more: 'display:inline-block;margin-top:10px;font-family:var(--font-display);font-size:12px;letter-spacing:.04em;color:var(--accent);text-decoration:none;',
  };

  function renderBlock(entries, lesId) {
    var shown = entries.slice(0, MAX_PER_LES);
    var lines = shown.map(function (e) {
      var fb = e.usedFallback ? ' <span style="' + STYLE.fallback + '">(' + LABELS.fallback + ')</span>' : '';
      return '<li style="' + STYLE.line + '">'
        + '<span style="' + STYLE.tarifit + '">' + escapeHtml(e.tarifit) + '</span>'
        + ' — <span style="' + STYLE.vertaling + '">' + escapeHtml(e.translation) + '</span>' + fb
        + ' <span style="' + STYLE.bron + '">(' + escapeHtml(e.bron) + ')</span>'
        + '</li>';
    }).join('');
    var lesNum = lesId.replace('les-', '').replace(/^0/, '');
    var moreLink = entries.length > MAX_PER_LES
      ? '<a style="' + STYLE.more + '" href="' + ZINNEN_PAGE + '?les=' + lesNum + '">' + LABELS.more + ' &rarr;</a>'
      : '';
    return '<div class="lz-block" style="' + STYLE.block + '">'
      + '<div style="' + STYLE.heading + '">' + LABELS.heading + '</div>'
      + '<ul style="' + STYLE.list + '">' + lines + '</ul>'
      + moreLink
      + '</div>';
  }

  fetchTarifitCSV('/assets/zinnen/zinnen.csv', {
    onSuccess: function (rows) {
      var byLes = buildLesIndex(rows);
      var sections = document.querySelectorAll('section[id^="les-"]');
      sections.forEach(function (section) {
        var entries = byLes[section.id];
        if (!entries || entries.length === 0) return;
        var div = document.createElement('div');
        div.innerHTML = renderBlock(entries, section.id);
        section.appendChild(div.firstChild);
      });
      resolveZinnenReady(buildIdIndex(rows));
    },
    onFileProtocol: function () { resolveZinnenReady({}); },
    onOtherError: function () { resolveZinnenReady({}); },
  });
})();
