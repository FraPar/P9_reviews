$(function() {
    console.log("Hello ca fonctionne wesh")
})

/* SEARCH  MODULE */
const input = document.querySelector('input');
const log = document.getElementById('id_q');

input.addEventListener('keyup', () =>
    unecommande("SELECT * FROM *")
);

var thisUser = "";

// get the selection of users and load it on the page
function getSelection(user_to_find) {
    var url = "http://127.0.0.1:8000/view_follows/" + user_to_find;
    jQuery.get(url).done(function(data) {
        //alert( "second success" )
        console.log(data)
     })
     .fail(function() {
        console.log("error");
     })
     .always(function() {
         //alert( "finished" )
     }); 
}

function getSelectionTest(e) {
    console.log("Hello ca marche encore !")
}
