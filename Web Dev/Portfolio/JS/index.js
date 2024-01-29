/* start toggler coding*/

var toggler_btn = document.querySelector(".toggler-btn");
var side_nav = document.querySelector(".side-nav");

toggler_btn.onclick = function(){
    side_nav.classList.toggle("active");
}

/*  start title animation coding*/

var title = document.querySelector("#title");
var array =[" Web Developer","Software Engineer","Java Developer"];
var arrIndex =0;
var charIndex=0;

function updateTitle(){
    charIndex++;
    title.innerHTML ="I'm <span>"+array[arrIndex].slice(0,charIndex)+"</span";
    if(charIndex== array[arrIndex].length){
        arrIndex++;
        charIndex=0;
    }
    if(arrIndex==array.length){
        arrIndex=0;
    }
    setTimeout(updateTitle,400);
}
updateTitle();


// download cv
let downloadbtn = document.querySelector(".download-btn a");
downloadbtn.addEventListener("click", () =>{
const span = document.querySelector(".download-btn a span");
downloadbtn.style.paddingRight = '5px;';
span.style.visibility ="visible";
 setTimeout(() => {
span.style.visibility="hidden;";
downloadbtn.style.transition = "1s ease";
downloadbtn.style.paddingRight="5px";
},3000) ;
})





// start filter option in project section
$(document).ready(function(){
    $(".nav-box li").each(function(){
        $(this).click(function(){
            $(".All").hide();
            var filter = $(this).attr("filter");
            $("."+filter).each(function(){
                $("."+filter).show(500);
            });
        });
    });
});
