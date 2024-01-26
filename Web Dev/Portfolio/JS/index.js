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
