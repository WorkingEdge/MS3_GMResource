/*jshint esversion: 6*/
//Send email using EmailJS template, report success on console and clear the form.

function sendMail(ms3_contact_form){
    emailjs.send("service_iiut1qe","template_1py6mif",{
from_name: ms3_contact_form.name.value,
from_email: ms3_contact_form.email_address.value,
query_type: ms3_contact_form.query_type.value,
grower_type: ms3_contact_form.grower_type.value,
add_message: ms3_contact_form.message_text.value,
})
      .then(
       function(response){
           console.log("Successful", response);
       },
       function(error){
          console.log("Failed", error);  
       })
       .then( 
         function (){
           document.getElementById("ms3_contact_form").reset(); 
        })
       ;
       return false; 
}