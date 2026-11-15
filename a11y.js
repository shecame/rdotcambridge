/* Shared accessibility layer: keeps the menu button and panel in sync for
   screen readers and keyboards, whatever script a page uses to open it. */
(function(){
  [['hamburger','navPanel'],['navBtn','mobileMenu']].forEach(function(pair){
    var btn = document.getElementById(pair[0]);
    var panel = document.getElementById(pair[1]);
    if (!btn || !panel) return;

    var openLabel = btn.getAttribute('aria-label') || 'Open menu';
    btn.setAttribute('aria-controls', pair[1]);

    function sync(){
      var open = panel.classList.contains('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : openLabel);
      if (open) { panel.removeAttribute('inert'); panel.removeAttribute('aria-hidden'); }
      else { panel.setAttribute('inert', ''); panel.setAttribute('aria-hidden', 'true'); }
      /* The page must not scroll behind the open panel, on every page */
      document.documentElement.style.overflow = open ? 'hidden' : '';
    }
    sync();
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ['class'] });

    /* Tapping a link closes the panel, including same-page section links */
    panel.addEventListener('click', function(e){
      if (e.target.closest('a') && panel.classList.contains('open')) btn.click();
    });

    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && panel.classList.contains('open')) { btn.click(); btn.focus(); }
    });
  });

  /* Every page opens at the top: no restored scroll position on reload,
     back, or forward, and a link to the page you are on goes to the top. */
  function toTop(){ window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  window.addEventListener('pageshow', function(e){ if (e.persisted) toTop(); });

  function pageKey(path){ return path.replace(/\.html$/, '').replace(/\/(index)?$/, '/'); }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href]');
    if (!a || a.target === '_blank' || (a.getAttribute('href') || '').charAt(0) === '#') return;
    if (a.origin !== location.origin || pageKey(a.pathname) !== pageKey(location.pathname)) return;
    /* Same page: let the menu close and any tab switch first, then go to the top */
    setTimeout(toTop, 0);
  });
})();
