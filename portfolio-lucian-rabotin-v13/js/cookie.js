/* =========================================================
   cookie.js : le choix est mémorisé et le bandeau est affiché
   uniquement sur l'accueil.
   ========================================================= */
document.addEventListener('DOMContentLoaded', () => {
  const banner = document.querySelector('.cookie');
  const key = 'lucian_cookie_choice';
  const path = window.location.pathname;
  const isHome = path.endsWith('/') || path.endsWith('/index.html');

  if (banner && isHome && !localStorage.getItem(key)) {
    banner.classList.add('show');
  } else {
    banner?.classList.remove('show');
  }

  const hide = () => banner?.classList.remove('show');

  document.querySelector('#acceptCookies')?.addEventListener('click', () => {
    localStorage.setItem(key, 'accepted');
    hide();
  });

  document.querySelector('#refuseCookies')?.addEventListener('click', () => {
    localStorage.setItem(key, 'refused');
    hide();
  });

  document.querySelectorAll('[data-cookie-reset]').forEach(button => {
    button.addEventListener('click', () => {
      localStorage.removeItem(key);
      if (isHome) banner?.classList.add('show');
      else window.location.href = 'index.html#cookies';
    });
  });
});
