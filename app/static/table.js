
jsdata = document.querySelector('meta[name="table"]').content

const jsonfile = JSON.parse(jsdata, function (key, value) {
    if (key == "Créer le" || key == "Début Prévu" ) {
      
      return new Date(value).getFullYear() + "-" + (new Date(value).getMonth()+1) + "-" + new Date(value).getDate() ;
    } else {
      return value;
    }
  });


//const jsonfile = JSON.parse(jsdata, dateTimeReviver);
    //console.log(jsonfile);  

var col = [];
for (var i = 0; i < jsonfile.length; i++) {
    for (var key in jsonfile[i]) {
        if (col.indexOf(key) === -1) {
            col.push(key);
         }
    }
}

var table = document.getElementById("table");
//var table = document.createElement("table");

var tr = table.insertRow(-1);                   // TABLE ROW.

for (var i = 0; i < col.length; i++) {
    var th = document.createElement("th");      // TABLE HEADER.
    th.innerHTML = col[i];
    tr.appendChild(th);
}
const tbody = document.createElement('tbody')
tbody.setAttribute("id","myTable")
const thead = document.getElementById("monheader");
table.append(tbody)

for (var i = 0; i < jsonfile.length; i++) {

    tr = tbody.insertRow(-1);

    for (var j = 0; j < col.length; j++) {
        var tabCell = tr.insertCell(-1);
        if (j > 0) {
        tabCell.innerHTML =  jsonfile[i][col[j]]
        tabCell.setAttribute('onclick', 'editcell('+i+', '+j+')')}
        else {
        tabCell.innerHTML =  jsonfile[i][col[j]]
        var inp = document.createElement("INPUT");
        inp.setAttribute("type", "checkbox");
        inp.setAttribute("value", "True");
        inp.setAttribute("id", "pousse" + i);
        tabCell.appendChild(inp)}    
        }
        
      
         
        //tabCell.innerHTML = <tr onclick= "editcell(i)"> </tr>;
        
    }


var divContainer = document.getElementById("showData");
divContainer.innerHTML = "";
divContainer.appendChild(table);

//var test = tr.getElementsByTagName("td");
//for (var i = 0; i< test.length; i++){
    //test.setAttribute("onclick", "editcell(i)") }//= "onclick = editcell(i)";




 function editcell(i,j) {
    
    if (table.rows[i+2].cells[j].innerHTML.match(/input/)){
        b =0;
    }
    else{ b =table.rows[i+2].cells[j].innerHTML;}

    var jour = table.getElementsByTagName('th')[j].innerHTML;

    var numordre = table.rows[i+2].cells[0].innerHTML;;//+ table.rows[i+2].cells[1].innerHTML;

    var numope = table.rows[i+2].cells[1].innerHTML;

    var sem = document.getElementById("semaine").value;
    
    table.rows[i+2].getElementsByTagName('td')[j].setAttribute('onclick', '  ')
    
    if (j === 8 || j === 9 || j === 10 || j === 11 || j === 12 ) {
    //table.rows[i+2].cells[j].innerHTML = "<td><input type='hidden' id='semaine1' name='semaine1' value= '"+sem+"'/><input type='hidden' id='jour' name='jour' value= '"+jour+"'/><input type='hidden' id='numordre' name='numordre' value= '"+numordre+"'/><input type='text' size = '2' name='heure' value = '"+b+"'/><br><input  type='submit' name='changheure' class='btn btn-success btn-xs' value = '&#10003' ><button type='button' class='btn btn-danger btn-xs' onclick =  'window.location.reload()'; document.getElementById['semaine'].submit() > X </button></td>";}
    //table.rows[i+2].cells[j].innerHTML = "<form method = 'POST' action= \"/sched\"><td><input type='hidden' id='semaine1' name='semaine1' value= '"+sem+"'/><input type='hidden' id='jour' name='jour' value= '"+jour+"'/><input type='hidden' id='numordre' name='numordre' value= '"+numordre+"'/><input type='hidden' id='numope' name='numope' value= '"+numope+"'/><input type='text' size = '2' name='heure' value = '"+b+"'/><br><input  type='submit' name='changheure' class='btn btn-success btn-xs' value = '&#10003' ><button type='button' class='btn btn-danger btn-xs' onclick =  'window.location.reload()'; document.getElementById['semaine'].submit() > X </button></td></form>";}
    table.rows[i+2].cells[j].innerHTML = "<td><input type='hidden' id='semaine1' name='semaine1' value= '"+sem+"'/><input type='hidden' id='jour' name='jour' value= '"+jour+"'/><input type='hidden' id='numordre' name='numordre' value= '"+numordre+"'/><input type='hidden' id='numope' name='numope' value= '"+numope+"'/><input type='text' size = '2' name='heure' value = '"+b+"'/><br><input  type='submit' name='changheure' class='btn btn-success btn-xs' value = '&#10003' ><button type='button' class='btn btn-danger btn-xs' onclick =  'window.location.reload()'; document.getElementById['semaine'].submit() > X </button></td>";}
    
    
   //console.log(table.rows[i].cells[j].innerHTML)

   //"<form method = 'POST' action= \"/sched\"><td><input type='text' size = '2' name='heure' value = '"+b+"'/><br><input  type='submit' name='changheure' class='btn btn-success btn-xs' value = '&#10003' ><button type='button' class='btn btn-danger btn-xs' onclick =  'window.location.reload()'; document.getElementById['semaine'].submit() > X </button></td></form>";}
     
    console.log(j)
    console.log(sem)
    //ok = table.getElementsByTagName('th')
    console.log(table.getElementsByTagName('th')[j].innerHTML)
 
 
}


 function setAction(form) {
     console.log('hoho')
     d = document.getElementById('jour').value
     console.log(d)

     console.log(table.rows.length)
     var numordre = [];
     var jour = [table.getElementsByTagName('th')[8].innerHTML, table.getElementsByTagName('th')[9].innerHTML,table.getElementsByTagName('th')[10].innerHTML,table.getElementsByTagName('th')[11].innerHTML, table.getElementsByTagName('th')[12].innerHTML]
     console.log(jour)
     for (var i = 0; i < table.rows.length -2 ; i++){
        if (document.getElementById('pousse'+ i).checked ){
        
        numordre.push(table.rows[i+2].cells[0].innerHTML.substr(0,7) + table.rows[i+2].cells[1].innerHTML)
        console.log(numordre)}
        else
        {console.log('crotte')}
    }
    document.getElementById('numordre').value = numordre
    document.getElementById('jour').value = jour

     



     form.action = "/sched";
     //alert(form.action);
//     //return false;

 }

function pousser()  {

  


    console.log('hoho')
    console.log(document.getElementById('pousse0').value)
    console.log(table.rows.length)
    var numordre = []
    var jour = [table.getElementsByTagName('th')[7].innerHTML, table.getElementsByTagName('th')[8].innerHTML,table.getElementsByTagName('th')[9].innerHTML,table.getElementsByTagName('th')[10].innerHTML, table.getElementsByTagName('th')[11].innerHTML]
    console.log(jour)
    

    for (var i = 0; i < table.rows.length -2 ; i++){
        if (document.getElementById('pousse'+ i).checked ){
        
        numordre.push(table.rows[i+2].cells[0].innerHTML.substr(0,7) + table.rows[i+2].cells[1].innerHTML)
        console.log(numordre)}
        else
        {console.log('crotte')}
    }
    document.getElementById('numordre').value = numordre

   
    
 
    
    
    //if (table.rows[i+2].cells.getElementsByTagName('input')[0].value = False){
    
    //}}
    
 
 
}