/* Private WLAN preview routing only; canonical anchor hrefs remain public URLs.
   Never ships as a production EstateShell asset. */
(() => {
  const map = {
    estate: '/estate/',
    teatro: '/teatro/',
    solstice: '/solstice/editions/first-reading/',
    satzfunk: 'http://192.168.8.50:8194/'
  };
  if (!['192.168.8.50', '127.0.0.1', 'localhost'].includes(location.hostname)) return;
  document.addEventListener('click', event => {
    const target = event.target.closest?.('header.fc-estate-shell a[data-estate-id]');
    if (!target || event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const url = map[target.dataset.estateId];
    if (!url) return;
    event.preventDefault();
    location.assign(url);
  });
  document.addEventListener('click', event => {
    const brand = event.target.closest?.('header.fc-estate-shell a.fc-publisher');
    if (brand && !event.metaKey && !event.ctrlKey && !event.shiftKey) {
      event.preventDefault();
      location.assign('/estate/');
    }
  });
})();
