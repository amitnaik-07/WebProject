document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is running!");

    setTimeout(function () {
    let modal=document.getElementById("signup-modal");
              if (modal) 
                {
                  modal.style.display = "flex";
                  console.log("Modal should be visible now!");
                } 
              else 
              {
                console.error("signupModal not found!");
              }
            }, 6000);    
    let closeButton = document.querySelector(".close-btn");
    if (closeButton) {
        closeButton.addEventListener("click", function () {
            document.getElementById("signupModal").style.display = "none";
            console.log("Modal closed!");
        });
    } else {
        console.error("Close button not found!");
    }
});

 