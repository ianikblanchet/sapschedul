
function ceduler(form){

var table = document.getElementById("table"); 
var numordre = []
for (var i = 1; i < table.rows.length ; i++){
    if (document.getElementById('ordre'+ i).checked ){
    
    numordre.push(table.rows[i].cells[1].innerHTML)
    console.log(table.rows[i].cells[1].innerHTML)
    console.log(document.getElementById("semaine").value)
}
    //else
    //{console.log('crotte')}
}
document.getElementById('numordre').value = numordre

form.action = "/ceduler";
}