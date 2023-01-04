$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    console.log('im sidenav')
    $(".dropdown-trigger").dropdown({ hover: false });
    console.log('dropdown baby')
    M.updateTextFields();
  });
