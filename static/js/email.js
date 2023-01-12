/* Contact form email functionality */

function sendMail(contactForm) {
  emailjs.send("gmail", "ms3", {
    "from_name": contactForm.name.value,
    "from_email": contactForm.email.value,
    "comments": contactForm.message_content.value
  })
    .then(
      function () {
        $('#response').html("Thank you for reaching out, we will respond to your message shortly.");
      },
      function () {
        $('#response').html("Sorry we have encoutered a problem, Please try again in a few minutes.");
      }
    );
    // Return Form Input 
    return false;
};
