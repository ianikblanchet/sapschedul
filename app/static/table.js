function fairetable (jsdata, listcheck)
{

 
//let jsdata = document.querySelector('meta[name="table"]').content

//import {untest} from '/sched.html';
let list = listcheck.split(',')


let jsonfile = JSON.parse(jsdata, function (key, value) {
    if (key == "Créer le" || key == "Début Prévu" ) {
      
      return new Date(value).getFullYear() + "-" + (new Date(value).getMonth()+1) + "-" + new Date(value).getDate() ;    
    } 
    else {
      return value;
    }
    
  });


//ajouter les checked
for (let i =0; i< list.length; i++){
    
    document.getElementById(list[i]).checked = true;
    
}

//trier à partir de case a cocher
for (let key in jsonfile){
    console.log(key, jsonfile[key]);
}

console.log(list)

let listejob = jsonfile.filter(ordre => list.includes(ordre['Poste de Travail']));
console.log(listejob)

listejob.sort((a,b) => (a['Poste de Travail'] > b['Poste de Travail']) ? -1 : ((b['Poste de Travail'] > a['Poste de Travail']) ? 1 : 0))


// let ok2 = [] 
// for (let i = 0; i < jsonfile.length; i++) {          
//     if (!list.includes(jsonfile[i]['Poste de Travail'])) {
//     //if (jsonfile[i]['Poste de Travail'] == '') {
//         //console.log(jsonfile[i]['Poste de Travail'])
//         //delete jsonfile[i]
//         ok2.push(i)
//         jsonfile.splice(i,1)
//     }
// }
// console.log(ok2)

// console.log(jsonfile) 

let col = [];
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

for (let i = 0; i < listejob.length; i++) {

    tr = tbody.insertRow(-1);

    for (var j = 0; j < col.length; j++) {
        var tabCell = tr.insertCell(-1);
        if (j > 0) {
        tabCell.innerHTML =  listejob[i][col[j]]
        tabCell.setAttribute('onclick', 'editcell('+i+', '+j+')')}
        else {
        tabCell.innerHTML =  listejob[i][col[j]]
        var inp = document.createElement("INPUT");
        inp.setAttribute("type", "checkbox");
        inp.setAttribute("value", "True");
        inp.setAttribute("id", "pousse" + i);
        tabCell.appendChild(inp)}                
        }

    if ((table.rows[i+2].cells[3].innerHTML).match(/MREP/))   {
        table.rows[i+2].setAttribute("class", "table-info")
    }
    if ((table.rows[i+2].cells[3].innerHTML).match(/MSER/))   {
        table.rows[i+2].setAttribute("class", "table-success")
    }
    if ((table.rows[i+2].cells[3].innerHTML).match(/MFAC/))   {
        table.rows[i+2].setAttribute("class", "table-warning")
    }
         
        
        
    }


var divContainer = document.getElementById("showData");
divContainer.innerHTML = "";
divContainer.appendChild(table);

//var test = tr.getElementsByTagName("td");
//for (var i = 0; i< test.length; i++){
    //test.setAttribute("onclick", "editcell(i)") }//= "onclick = editcell(i)";

}

//fin de la fonction creertable

//fonction pour changer de semaine
function chsem(form) {
    let checkboxes = document.querySelectorAll('input[name^= "PDT"]:checked')
    let choi = []
    checkboxes.forEach((checkbox) => {
             choi.push(checkbox.value)
             })
    document.getElementById('listcheck').value = choi
    
    console.log(choi)

form.action = "/sched";
}


console.log(document.getElementById('listcheck').value)


 function editcell(i,j) {

    let checkboxes = document.querySelectorAll('input[name^= "PDT"]:checked')
    let choi = []
    checkboxes.forEach((checkbox) => {
             choi.push(checkbox.value)
             })
    
    
    if (table.rows[i+2].cells[j].innerHTML.match(/input/)){
        b =0;
    }
    else{ b =table.rows[i+2].cells[j].innerHTML;}

    let jour = table.getElementsByTagName('th')[j].innerHTML;

    let numordre = table.rows[i+2].cells[0].innerHTML;;//+ table.rows[i+2].cells[1].innerHTML;

    let numope = table.rows[i+2].cells[1].innerHTML;

    let sem = document.getElementById("semaine").value;
    
    table.rows[i+2].getElementsByTagName('td')[j].setAttribute('onclick', '  ')
    
    if (j === 8 || j === 9 || j === 10 || j === 11 || j === 12 ) {
    
    table.rows[i+2].cells[j].innerHTML = "<td><input type='hidden' id='listcheck3' name='listcheck3' value= '"+choi+"'/>  <input type='hidden' id='semaine1' name='semaine1' value= '"+sem+"'/><input type='hidden' id='jour' name='jour' value= '"+jour+"'/><input type='hidden' id='numordre' name='numordre' value= '"+numordre+"'/><input type='hidden' id='numope' name='numope' value= '"+numope+"'/><input type='text' size = '2' name='heure' value = '"+b+"'/><br><input  type='submit' name='changheure' class='btn btn-success btn-xs' value = '&#10003' ><button type='button' class='btn btn-danger btn-xs' onclick =  'window.location.reload()'; document.getElementById['semaine'].submit() > X </button></td>";}
    
    
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

    let checkboxes = document.querySelectorAll('input[name^= "PDT"]:checked')
    let choi = []
    checkboxes.forEach((checkbox) => {
             choi.push(checkbox.value)
             })
    console.log(choi)
    document.getElementById('listcheck2').value = choi



    form.action = "/sched";
     //alert(form.action);
//     //return false;

 }


//créer ma liste de choix
function modifcheck(form) {
    let checkboxes = document.querySelectorAll('input[name^= "PDT"]:checked')
    let choi = []
    checkboxes.forEach((checkbox) => {
             choi.push(checkbox.value)
             })
    document.getElementById('listcheck').value = choi
    console.log(choi)
// let test1 = document.getElementById("choix");

// let choi = []
// test1.addEventListener('change', () => {
//     let checkboxes = document.querySelectorAll('input[name="PDT"]:checked');
//     checkboxes.forEach((checkbox) => {
//     choi.push(checkbox.value)
//     })
//     document.querySelector('meta[name="listcheck"]').content = choi 
//     console.log(document.querySelector('meta[name="listcheck"]').content)
// })
form.action = "/sched";
}



function allseron(titre, equi) {    
    let pdts = document.querySelectorAll("input[name='"+titre+"']")
    
    console.log(pdts)
    pdts.forEach((pdt) => {
    console.log(pdt.value)
    document.getElementById(pdt.value).checked= true;
    //pdt.checked= true;
    })
    //document.getElementById("MSERMEC").checked= true;
    //document.getElementById("MSEREL").checked= true;
    //document.getElementById("MSERMAI").checked= true;
    //document.getElementById("MSERSYH").checked= true;
    console.log(equi)
    document.getElementById(equi.id).setAttribute("onClick", "allseroff('"+titre+"', this)")
    document.getElementById(equi.id).style.backgroundColor = ''
}

function allseroff(titre, equi) {
    let pdts = document.querySelectorAll("input[name='"+titre+"']")
    
    console.log(pdts)
    pdts.forEach((pdt) => {
    console.log(pdt.value)
    document.getElementById(pdt.value).checked= false;
    //pdt.checked= true;
    })
    
    console.log(equi)
    document.getElementById(equi.id).setAttribute("onClick", "allseron('"+titre+"' , this)")
    document.getElementById(equi.id).style.backgroundColor = ''

}



//const btn = document.querySelector('#btn');


// const test4 = function validechoix(){

//     let checkboxes = document.querySelectorAll('input[name="PDT"]:checked');
//     checkboxes.forEach((checkbox) => {
//     choi.push(checkbox.value)
// })
// document.querySelector('meta[name="listcheck"]').content = choi

//  }

// let test5 = []
// test1.addEventListener('change', () => {test5 = test4()});
// console.log(document.querySelector('meta[name="listcheck"]').content)

// test1.addEventListener('change', () => {
//     let checkboxes = document.querySelectorAll('input[name="PDT"]:checked');
//     checkboxes.forEach((checkbox) => {
//     choi.push(checkbox.value)
//     })
//     document.querySelector('meta[name="listcheck"]').content = choi 
//     console.log(document.querySelector('meta[name="listcheck"]').content)
// })

    //let checkboxes = document.querySelectorAll('input[name="PDT"]:checked');
    //let choi = []
    //checkboxes.forEach((checkbox) => {
//         choi.push(checkbox.value);
//     });
//     console.log(choi)
//     //console.log(checkboxes)
//     return choi
// }); 



// let elements = document.getElementById("choix").elements
// for (let i = 0; i < elements.length; i++){
//     if (elements[i].checked) {
//         choix.push(element.value)
//     }
// }



//  function pousser()  {  


//     console.log('hoho')
//     console.log(document.getElementById('pousse0').value)
//     console.log(table.rows.length)
//     var numordre = []
//     var jour = [table.getElementsByTagName('th')[7].innerHTML, table.getElementsByTagName('th')[8].innerHTML,table.getElementsByTagName('th')[9].innerHTML,table.getElementsByTagName('th')[10].innerHTML, table.getElementsByTagName('th')[11].innerHTML]
//     console.log(jour)
    

//     for (var i = 0; i < table.rows.length -2 ; i++){
//         if (document.getElementById('pousse'+ i).checked ){
        
//         numordre.push(table.rows[i+2].cells[0].innerHTML.substr(0,7) + table.rows[i+2].cells[1].innerHTML)
//         console.log(numordre)}
//         else
//         {console.log('crotte')}
//     }
//     document.getElementById('numordre').value = numordre      
//}
    
    
    //if (table.rows[i+2].cells.getElementsByTagName('input')[0].value = False){
    
    //}}
    
 
 
