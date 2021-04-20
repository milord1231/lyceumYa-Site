
const filterBox = document.querySelectorAll('.main-catalogs.box');

document.getElementById('nav-side').addEventListener('click', (event) => {
  if (event.target.tagName !== 'LI') return false;
  let filterClass = event.target.dataset['f'];

  filterBox.forEach(elem => {
    elem.style.display=""
    if (!elem.classList.contains(filterClass) && filterClass !== 'all') {
      elem.style.display="none";
      
    }
  });
  var side_panel = document.querySelector('#side-panel')
  if (side_panel.style.left != '0px') {
    side_panel.style.left = '0px'
  }
  else {
    side_panel.style.left = '-50vh'
  };
  var open = document.getElementById('side-button-open')
  var close = document.getElementById('side-button-close')

  if (open.style.display == 'block') {
    open.style.display = 'none';
    close.style.display = 'block'

  }
  else{
    open.style.display = 'block'
    close.style.display = 'none'

  };

});

document.getElementById('1side-button-1-wr').addEventListener('click', (event) => {
  var side_panel = document.querySelector('#side-panel')
  if (side_panel.style.left != '0px') {
    side_panel.style.left = '0px'
  }
  else {
    side_panel.style.left = '-50vh'
  };
  var open = document.getElementById('side-button-open')
  var close = document.getElementById('side-button-close')

  if (open.style.display == 'block') {
    open.style.display = 'none';
    close.style.display = 'block'


  }
  else{
    open.style.display = 'block'
    close.style.display = 'none'

  };

});


document.getElementById('side-button-in-side').addEventListener('click', (event) => {
  var side_panel = document.querySelector('#side-panel')
  if (side_panel.style.left != '0px') {
    side_panel.style.left = '0px'
  }
  else {
    side_panel.style.left = '-50vh'
  };
  var open = document.getElementById('side-button-open')
  var close = document.getElementById('side-button-close')

  if (open.style.display == 'block') {
    open.style.display = 'none';
    close.style.display = 'block'

  }
  else{
    open.style.display = 'block'
    close.style.display = 'none'

  };

});


