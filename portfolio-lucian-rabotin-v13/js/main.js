/* main.js : animations d'apparition et bouton retour en haut. */
document.addEventListener('DOMContentLoaded',()=>{
  const elements=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target)}}),{threshold:.12});
    elements.forEach(el=>observer.observe(el));
  }else elements.forEach(el=>el.classList.add('visible'));
  document.querySelectorAll('.scroll-top').forEach(el=>el.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'})));
});
