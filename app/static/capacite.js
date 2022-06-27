function gerercap(cappdt, semcourante){
let table = document.getElementById("table");   
let cap = document.getElementById("capacite").getElementsByTagName('tbody')[0];   

var pdt = []

let jsoncap = JSON.parse(cappdt)
let jsonsemcour = JSON.parse(semcourante)

console.log(jsonsemcour)
console.log(jsoncap)


console.log(cappdt)

for(var i = 2; i < table.rows.length; i++){
    pdt.push(table.rows[i].cells[3].innerHTML)
    } 

let pdtuni = [...new Set(pdt)];

pdtuni.sort();
pdtuni.reverse();
//pdtuni.sort((a,b) => (a > b) ? -1 : ((b > a) ? 1 : 0));

//création du tableau capacité
for (var i = 0; i < pdtuni.length; i++) {

let captr = cap.insertRow(-1); 

let capth = document.createElement("th"); 
capth.innerHTML = pdtuni[i];
captr.appendChild(capth);
        for (let j = 1; j < 7; j++){
            captr.insertCell(j)
        }

}

 
//test pour créer un object mais je ne m'en sert pas
let captot = {}


for (let i = 0; i < pdtuni.length; i++){

captot[pdtuni[i]] = {lundi:0, mardi:0, mercredi:0, jeudi:0, vendred:0}
 }



//compter les capacités
for (var i = 0; i < pdtuni.length; i++) {
    
 for (var j = 0; j < 5; j++) {
     
       let tot  = 0
       for (var k = 0; k < table.rows.length -2 ; k++) {                     
           
           if (table.rows[k+2].cells[3].innerHTML == pdtuni[i]){
           tot =  tot + parseInt(table.rows[k+2].cells[8+j].innerHTML)

           }
    
    cap.rows[i].cells[j+1].innerHTML = tot
      
 }
 
 
}

}  
console.log(table.rows[1].cells[8].innerHTML) 
// pour calculer le total par pdt
for (var i = 0; i < cap.rows.length ; i++) {
    let subtot = 0
    for (var j = 1; j < 6; j++) {
        subtot += parseInt(cap.rows[i].cells[j].innerHTML)
        console.log(cap.rows[i].cells[0].innerHTML)
        //console.log(jsoncap[cap.rows[i].cells[0].innerHTML][table.rows[1].cells[j+7].innerHTML])
        if (cap.rows[i].cells[j].innerHTML >  jsoncap[cap.rows[i].cells[0].innerHTML][jsonsemcour[j-1] + ' 00:00:00']){
            cap.rows[i].cells[j].style.color = 'red';
        }
    }

cap.rows[i].cells[6].innerHTML = subtot



if ((cap.rows[i].cells[0].innerHTML).match(/MREP/))   {
    cap.rows[i].setAttribute("class", "table-info")
    }
if ((cap.rows[i].cells[0].innerHTML).match(/MSER/))   {
    cap.rows[i].setAttribute("class", "table-success")
    }
if ((cap.rows[i].cells[0].innerHTML).match(/MFAC/))   {
    cap.rows[i].setAttribute("class", "table-warning")
    }
}

}
        