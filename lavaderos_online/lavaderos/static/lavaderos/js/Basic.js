

const select_menu = document.querySelectorAll('.nav-item');
const active_sidebar = document.getElementsByClassName('menu__active');
const sidebar = document.getElementsByClassName('sidebar');
var URLactual = window.location;
console.log(URLactual.href)

console.log(select_menu);

select_menu.forEach(element => {
  console.log(element)
  element.addEventListener('click',()=>{
    console.log(element)
    element.classList.toggle('active');
  })
});

if (URLactual.href.includes('/lavaderos/')) {
  select_menu[0].classList.add('active')
}
if (URLactual.href.includes('/search')) {
  select_menu[1].classList.add('active')
}
if (URLactual.href.includes('/registrolavadero/')) {
  document.getElementsByClassName('sidebarregistrolavadero')[0].classList.add('active')
}
if (URLactual.href.includes('/milavadero/')) {
  document.getElementsByClassName('sidebarmilavadero')[0].classList.add('active')
}
if (URLactual.href.includes('/solicitudeslavado/')) {
  document.getElementsByClassName('sidebarsolicitudeslavado')[0].classList.add('active')
}
if (URLactual.href.includes('/search')) {
  select_menu[1].classList.add('active')
}
console.log(active_sidebar[0])
active_sidebar[0].addEventListener('click',()=>{
  sidebar[0].classList.toggle('active')
})

var select = document.getElementsByTagName("select");
console.log(select)

