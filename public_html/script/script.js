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
    "first_name": ["Mario", /^[A-Za-z]+/, "Inserisci il tuo nome"],
    "last_name": ["Rossi", /^[A-Z][a-z]+( ([A-Z][a-z]+))?/, "Inserisci il tuo cognome"],
    "email": ["Inserire e-mail", /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/, "Inserisci un indirizzo email valido"]
}

var dettagli_form_plant = {
    "name": ["Nome pianta", /^[A-Za-z- ]*$/, "Inserisci il nome della pianta"],
    "scientificName": ["Nome scientifico", /[A-Za-z- ]*/, ""],
    "type": ["Tipo", /.*/, ""],
    "price": ["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto"],
    //"format": ["", /.*/, ""],
    "dataName": ["Nome del dato", /.*/, ""],
    "dataContent": ["valore", /.*/, ""]
}

var dettagli_form_tool = {
    "name": ["Nome attrezzo", /^[a-zA-Z ]*$/, "Inserisci il nome dell'attrezzo'"],
    "type": ["Tipo", /.*/, ""],
    "price": ["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto"],
    // "format": ["al pezzo", /.*/, ""],
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
    if (((text == matrix[input.id][0])) || text.search(regex) != 0) //occhio! controllo che l'input sia diverso dal placeholder (con il primo check)
    {
        mostraErrore(matrix, input);
        return false;
    }
    return true;
}

// Funzioni per il controllo sul tipo dell'immagine inserita nella form
function checkPictureType(Extension) {
    return (Extension == "gif" || Extension == "png" || Extension == "svg" || Extension == "bmp" || Extension == "jpeg" || Extension == "jpg");
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
    var rImg = checkImage(); 
    var rFrm = validazioneForm(dettagli_form_plant); 
    var vDynFrm = validazioneForm(dettagli_dynamic_input);
    var valRes= (rImg && rFrm && vDynFrm);
    if (valRes == true)
        dettagli_dynamic_input={};
    //console.log(validazioneForm(dettagli_dynamic_input));
    return valRes;
}

function validazioneFormTool() {
    var rImg = checkImage(); 
    var rFrm = validazioneForm(dettagli_form_tool); 
    var vDynFrm = validazioneForm(dettagli_dynamic_input);
    var valRes= (rImg && rFrm && vDynFrm);
    if (valRes == true)
        dettagli_dynamic_input={};
    return valRes;
}

function validazioneFormContattaci(){
    return validazioneForm(dettagli_form_contattaci);
}

function validazioneForm(matrix) {
    var corretto = true;
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

var counter_prezzo = 1;
var counter_valore = 1;

function addNInputData(divname, number) {
    for(i=0; i<number; ++i){
        dettagli_dynamic_input['dataName'+counter_valore]=["Nome del dato", /.*/, ""];
        dettagli_dynamic_input['dataContent'+counter_valore]=["valore", /.*/, ""];
        counter_valore++;
    }
    caricamento(dettagli_dynamic_input, false);
}

function addNInputPrice(divName, number) {
    for(i=0; i<number; ++i){
        dettagli_dynamic_input['price'+counter_prezzo]=["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto"];
        counter_prezzo++;
    }
    caricamento(dettagli_dynamic_input, false);
}

function addInputPrice(divName) { 
    var toInsert = '<div class="inputsL"><label for="price" class="inputL">Prezzo (es. 7.50): &euro; </label><input type="text" name="price\[\]" id="price' + (counter_prezzo + 1) + '" class="inputL"/></div><div class="inputsR"><label for="format' + (counter_prezzo + 1) + '" class="inputR">Formato (es. al pezzo):</label><input type="text" name="format\[\]" id="format' + (counter_prezzo + 1) + '" class="inputR"/></div>';
    counter_prezzo = addInput(divName, counter_prezzo, toInsert);
    dettagli_dynamic_input['price'+counter_prezzo]=["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto"];
    // dettagli_dynamic_input['format'+counter_prezzo]=["", /.*/, ""];
    caricamento(dettagli_dynamic_input, false);
}

function addInputData(divName) {
    var toInsert = '<div class="inputsL"><label for="dataName" class="inputL">Dato (es. Altezza):</label><input type="text" name="dataName\[\]" id="dataName' + (counter_valore + 1)+'" class="inputL"/></div><div class="inputsR"><label for="dataContent' + (counter_valore + 1) + '" class="inputR">Formato (es. 10cm):</label><input type="text" name="dato\[\]" id="dataContent' + (counter_valore + 1) + '" class="inputR"/></div>';
    counter_valore = addInput(divName, counter_valore, toInsert);
    dettagli_dynamic_input['dataName'+counter_valore]=["Nome del dato", /.*/, ""];
    dettagli_dynamic_input['dataContent'+counter_valore]=["valore", /.*/, ""];
    caricamento(dettagli_dynamic_input, false);
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
