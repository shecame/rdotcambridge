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
    }
    sync();
    new MutationObserver(sync).observe(panel, { attributes: true, attributeFilter: ['class'] });

    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && panel.classList.contains('open')) { btn.click(); btn.focus(); }
    });
  });
})();
