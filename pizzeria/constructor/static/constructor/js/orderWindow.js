function openSlideMenu () {
  document.getElementById('menu').style.width = '25vw';
  document.getElementById('content').style.marginRight = '25vw';
  document.getElementById('menu').style.borderBottomLeftRadius = '25px';
  document.getElementById('makeOrder').style.opacity = '0';
}

function closeSlideMenu () {
  document.getElementById('menu').style.width = '0';
  document.getElementById('content').style.marginRight = '0';
  document.getElementById('makeOrder').style.opacity = '1';
}