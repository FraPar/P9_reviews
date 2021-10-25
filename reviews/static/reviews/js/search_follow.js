$(function() {
    console.log("Hello ca fonctionne wesh")
})

/* SEARCH  MODULE */
const input = document.querySelector('input');
const log = document.getElementById('id_q');

input.addEventListener('keyup', () =>
    console.log(log.value)
);

var thisUser = "";

// get the selection of users and load it on the page
function getSelection(user_to_find) {
    var url = user_to_find;
    $.get(url).done(function(data) {
        //alert( "second success" )
        console.log("ca fonctionne")
     })
     .fail(function() {
         alert( "error" );
     })
     .always(function() {
         //alert( "finished" )
     }); 
}

function getSelectionTest(e) {
    console.log("Hello ca marche encore !")
}
