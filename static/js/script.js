$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $(".dropdown-trigger").dropdown({ hover: false });
    M.updateTextFields();
    $('.carousel').carousel();
    $('select').formSelect();
    $('.modal').modal();
  });

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

topFunction();