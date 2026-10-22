/* Same-origin, CSP-safe active reel retention (not a publisher). */
(() => {
  const header = document.querySelector('header.fc-estate-shell[data-estate-identity]');
  const reel = header?.querySelector('nav.fc-shell-reel');
  if (!header || !reel) return;
  const ident = header.dataset.estateIdentity;
  const apply = () => {
    for (const item of reel.querySelectorAll('a[data-estate-id]')) {
      if (item.dataset.estateId === ident) {
        if (item.getAttribute('aria-current') !== 'page') item.setAttribute('aria-current', 'page');
      } else if (item.hasAttribute('aria-current')) item.removeAttribute('aria-current');
    }
  };
  const observer = new MutationObserver(apply);
  observer.observe(reel, {attributes: true, subtree: true, attributeFilter: ['aria-current']});
  apply();
  document.addEventListener('DOMContentLoaded', apply);
  window.addEventListener('pageshow', apply);
})();
