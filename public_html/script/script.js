function logform() {
    // if(document.getElementById('log').clicked{
    // prompt(“Inserisci la login:”,“guest”);
    // }
}

// funzione per rendere a scomparsa il login dell'amministratore
function nascondi() {
    //salvo sulla variabile nasc, lo style dell'elemento passato

    var e = document.getElementById('login');
    if (e.style.display != 'block')
        e.style.display = 'block';
    else
        e.style.display = 'none';
}

// Funzioni per la form delle pagine
/*
chiave: nome dell'input da controllare
[0]: prima indicazione per la compilazione dell'input
[1]: l'espressione regolare da controllare
[2]: hint nel caso in cui l'inpuit fornito sia sbagliato
*/

// Campi dati per le varie form
var dettagli_form_contattaci = {
    "first_name": ["Mario", /^[A-Z][a-z]+/, "Inserisci il tuo nome"],
    "last_name": ["Rossi", /^[A-Z][a-z]+( ([A-Z][a-z]+))?/, "Inserisci il tuo cognome"],
    "email": ["Inserire e-mail", /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/, "Inserisci un indirizzo email valido"]
}

var dettagli_form_plant = {
    "name": ["Nome pianta", /^[A-Z][a-z]+/, "Inserisci il nome della pianta"],
    "scientificName": ["Nome scientifico", /.*/, ""],
    "type": ["Tipo", /.*/, ""],
    "price": ["", /^\d+(.\d{1,2})?$/, "Inserisci il prezzo separato da un punto"],
    "format": ["per una confezione di 10 fiori", /.*/, ""],
    "dataName": ["Nome del dato", /.*/, ""],
    "dataContent": ["valore", /.*/, ""]
}

var dettagli_form_tool = {
    "name": ["Nome pianta", /^[A-Z][a-z]+/, "Inserisci il nome dell'attrezzo'"],
    "type": ["Tipo", /.*/, ""],
    "price": ["", /^\d+(.\d{1,2})?$/, "Inserisci il prezzo separato da un punto"],
    "format": ["al pezzo", /.*/, ""],
    "dataName": ["Nome del dato", /.*/, ""],
    "dataContent": ["valore", /.*/, ""]
}

var dettagli_form_admin = {
    "inputUsername": ["Username", /.*/, ""],
    "inputPassword": ["Password", /.*/, ""]
}

var dettagli_dynamic_input = {}

function caricamentoPianta() {
    return caricamento(dettagli_form_plant, true);
}

function caricamentoAttrezzi() {
    return caricamento(dettagli_form_tool, true);
}

function caricamentoContattaci() {
    return caricamento(dettagli_form_contattaci, false);
}

function caricamentoPannelloAdmin() {
    return caricamento(dettagli_form_admin, false);
}

// Funzione che data la matrice dei campi dati, li inserisce all'interno della form e stabilisce i controlli
function caricamento(matrix, checkImg) //carica i dati nei campi
{
    if (checkImg == true) {
        var img = document.getElementById("image");
        img.onchange = function() {
            checkImage(this);
        };
    }

    for (var key in matrix) {
        var input = document.getElementById(key);
        campoDefault(matrix, input);

        input.onfocus = function() {
            campoPerInput(matrix, this);
        }; //toglie l'aiuto
        input.onblur = function() {
            validazioneCampo(matrix, this);
        }; //fa la validazione del campo
    }
}

function campoDefault(matrix, input) {
    if (input.value == "") {
        input.value = matrix[input.id][0];
    }
}

function campoPerInput(matrix, input) {
    if (input.value == matrix[input.id][0]) {
        input.value = "";
    }
}

function validazioneCampo(matrix, input) {
    var p = input.parentNode; //prende lo span
    var errore = document.getElementById(input.id + "errore");
    if (errore) {
        p.removeChild(errore)
    }

    var regex = matrix[input.id][1];
    var text = input.value;
    if ((text == matrix[input.id][0]) || text.search(regex) != 0) //occhio! controllo che l'input sia diverso dal placeholder (con il primo check)
    {
        mostraErrore(matrix, input);
        return false;
    }
    return true;
}

// Funzioni per il controllo sul tipo dell'immagine inserita nella form
function checkPictureType(Extension) {
    return (Extension == "gif" || Extension == "png" || Extension == "bmp" || Extension == "jpeg" || Extension == "jpg");
}

function checkImage() {
    var fuData = document.getElementById('image');
    var p = fuData.parentNode; //prende lo span
    var errore = document.getElementById(fuData.id + "errore");
    if (errore) {
        p.removeChild(errore);
    }
    var FileUploadPath = fuData.value;

    if (FileUploadPath == '') {
        // alert("Please upload an image");
        // errImg(fuData);
        return true;
    } 
    else {
        var Extension = FileUploadPath.substring(
            FileUploadPath.lastIndexOf('.') + 1).toLowerCase();
        if (checkPictureType(Extension)){
            return true;
        } 
        else {
            // alert("Photo only allows file types of GIF, PNG, JPG, JPEG and BMP. ");
            errImg(fuData);
            return false;
        }
    }
}
// fine

function validazioneFormPlant() {
    return validazioneForm(dettagli_form_plant);
}

function validazioneFormTool() {
    return validazioneForm(dettagli_form_tool);
}

function validazioneForm(matrix) {
    var corretto = true;
    var resImg = checkImage();
    console.log("image", resImg);
    corretto = corretto && resImg;
    for (var key in matrix) {
        var input = document.getElementById(key);
        var risultato = validazioneCampo(matrix, input);
        console.log(key, risultato);
        corretto = corretto && risultato;
    }
    return corretto;
}


function mostraErrore(matrix, input) {
    console.log(input);
    var p = input.parentNode;
    var e = document.createElement("strong");
    e.className = "errorSuggestion";
    e.id = input.id + "errore";
    e.appendChild(document.createTextNode(matrix[input.id][2]));
    p.appendChild(e);
}

function errImg(fuData) {
    var p = fuData.parentNode;
    var e = document.createElement("strong");
    e.className = "errorSuggestion";
    e.id = (document.getElementById("image")).id + "errore";
    e.appendChild(document.createTextNode("Inserisci un file immagine"));
    p.appendChild(e);
}

// Funzioni per aumentare dinamicamente il numero di campi dati della form

var n_Prezzo = 1;
var n_Valore = 1;

function addPrezzo() {
    var container = document.getElementsByClassName('create');
    // container.appendChild(document.createTextNode("Member " + (i+1)));
    // Create an <input> element, set its type and name attributes
    var ln = document.createElement("li");
    var par = document.createElement("p");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "price" + n_Prezzo;
    var lbl = document.createElement("label");
    lbl.setAttribute("for", "price" + (n_Prezzo + 1));
    var t = document.createTextNode("Prezzo: &euro; ");
    lbl.appendChild(t);
    par.appendChild(lbl);
    par.appendChild(input);
    ln.appendChild(par)
    container.appendChild(ln);
    n_Prezzo = n_Prezzo + 1;
}

var counter_prezzo = 1;
var counter_valore = 1;

function addInputPrice(divName) { 
    var toInsert = '<div class="inputsL"><label for="price" class="inputL">Prezzo: &euro; </label><input type="text" name="price\[' + (counter_prezzo + 1) + '\]" id="price' + (counter_prezzo + 1) + '" placeholder="3.99" class="inputL"/></div><div class="inputsR"><label for="format' + (counter_prezzo + 1) + '" class="inputR">Formato:</label><input type="text" name="price\[' + (counter_prezzo + 1) + '\]" id="format' + (counter_prezzo + 1) + '" placeholder="al pezzo" class="inputR"/></div>';
    counter_prezzo = addInput(divName, counter_prezzo, toInsert);
}

function addInputData(divName) {
    var toInsert = '<div class="inputsL"><label for="dataName" class="inputL">Dato:</label><input type="text" name="dataName" id="dato\[' + (counter_prezzo + 1) + '\]" placeholder="Lunghezza manico" class="inputL"/></div><div class="inputsR"><label for="dataContent' + (counter_prezzo + 1) + '" class="inputR">Contenuto:</label><input type="text" name="dato\[' + (counter_prezzo + 1) + '\]" id="dataContent' + (counter_prezzo + 1) + '" placeholder="10 cm" class="inputR"/></div>';
    counter_valore = addInput(divName, counter_valore, toInsert);
}

function addInput(divName, counter, toInsert) {
    var newspan = document.createElement('span');
    newspan.innerHTML = toInsert;
    document.getElementById(divName).appendChild(newspan);
    counter++;
    return counter;
}


//funzione che sostituisce l'immagine della mappa con la mappa in google maps
function replaceMap() {
    var map = document.getElementById("visualizzaMappa");
    map.innerHTML = "<iframe id='frameMappa' class='noprint' src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2800.9012391702986!2d11.885443115555669!3d45.41133107910034!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x477eda58b44676df%3A0xfacae5884fca17f5!2sTorre+Archimede%2C+Via+Trieste%2C+63%2C+35121+Padova+PD!5e0!3m2!1sit!2sit!4v1472819512186'></iframe><img id=\"fotoMappa\" class=\"print\" src=\"img/mappa.png\" alt=\"Mappa della sede di GGarden\" />";
}
// fine

// Funzioni per la pagina Realizzazioni

function loadPics() {
    if (!document.getElementById || !document.getElementsByTagName) return;
    links = document.getElementById("minipics").getElementsByTagName("a");
    for (i = 0; i < links.length; i++)
        links[i].onclick = function() {
            Show(this);
            return (false)
        }
}

function Show(obj) {
    bigimg = document.getElementById("bigimage");
    bigimg.src = obj.getAttribute("href");
    smallimg = obj.getElementsByTagName("img")[0];
    t = document.getElementById("titolo");
    t.removeChild(t.lastChild);
    t.appendChild(document.createTextNode(smallimg.title));
}