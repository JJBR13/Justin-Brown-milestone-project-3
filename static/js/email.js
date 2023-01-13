/* Contact form email functionality */
function sendMail() {
  /* Prevent Default */
  document.getElementById("contact_form").addEventListener('submit', function (event) {
    event.preventDefault();

    // getting elements
    let responseElement = document.getElementById('response');
    let contactForm = document.getElementById('contact_form');

    /* POST email */
    emailjs.sendForm("service_iak79un", "template_5adrgwn", "#contact_form")
      .then(function () {
        console.log('success');

        // reset contact form
        contactForm.reset()

        // success message
        responseElement.innerText = "Thank you for reaching out, we will respond to your message shortly.";
        // within 3secs page loads
        setInterval(() => window.location.reload(true), 3000);
        // If there is an error with form
      }, function (error) {
        console.log(error)
        responseElement.innerText = "<span style='color: red;'>Sorry we have encoutered a problem, Please try again in a few minutes.</span>";
      });
  });
}