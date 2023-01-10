$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    console.log('im sidenav')
    $(".dropdown-trigger").dropdown({ hover: false });
    console.log('dropdown baby')
    M.updateTextFields();
    $('.carousel').carousel();
    $('select').formSelect();
  });

  document.write(new Date().getFullYear());

// Credit to w3school

mybutton = document.getElementById("top-btn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}