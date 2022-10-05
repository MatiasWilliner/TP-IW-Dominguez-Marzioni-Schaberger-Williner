

const menusidebar = document.getElementsByClassName('menu__active');
const sidebar = document.getElementsByClassName('sidebar');

console.log(menusidebar);

menusidebar[0].addEventListener('click', function onClick() {
  sidebar[0].classList.toggle('active');
});

const combobox_desactivar = document.getElementById('id_tarifa_set')

console.log(combobox_desactivar)
