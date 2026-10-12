/* navigation.js : menu mobile + page active. */
document.addEventListener('DOMContentLoaded',()=>{
  const button=document.querySelector('.menu-btn');
  const nav=document.querySelector('.nav-links');
  if(button&&nav) button.addEventListener('click',()=>nav.classList.toggle('open'));
  document.querySelectorAll('.nav-links a').forEach(a=>a.addEventListener('click',()=>nav?.classList.remove('open')));
  const current=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.nav-links a').forEach(a=>{if(a.getAttribute('href')===current)a.classList.add('active')});
});
