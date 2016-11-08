function logform() {
    // if(document.getElementById('log').clicked{
    // prompt(“Inserisci la login:”,“guest”);
    // }
}

// funzione per rendere a scomparsa il login dell'amministratore
function nascondi() {
    //salvo sulla variabile nasc, lo style dell'elemento passato

    var e = document.getElementById("login");
    if (e.style.display != "block")
        e.style.display = "block";
    else
        e.style.display = "none";
}

// Funzioni per la form delle pagine
/*
chiave: nome dell'input da controllare
[0]: prima indicazione per la compilazione dell'input
[1]: l'espressione regolare da controllare
[2]: hint nel caso in cui l'input fornito sia sbagliato
*/

// Campi dati per le varie form
var dettagli_form_contattaci = {
    "first_name": ["Mario", /^[A-Za-z]+/, "Inserisci il tuo nome"],
    "last_name": ["Rossi", /^[A-Z][a-z]+( ([A-Z][a-z]+))?/, "Inserisci il tuo cognome"],
    "email": ["Inserire e-mail", /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/, "Inserisci un indirizzo email valido"]
};

var dettagli_form_plant = {
    "name": ["Nome pianta", /^[a-zA-ZÀ-ÿ0-9 -]+$/, "Inserisci il nome della pianta"],
    "scientificName": ["Nome scientifico", /[A-Za-z- ]*/, ""],
    "type": ["Tipo", /.*/, ""],
    "dataName": ["Nome del dato", /.*/, ""],
    "dataContent": ["valore", /.*/, ""]
};

var dettagli_form_tool = {
    "name": ["Nome attrezzo", /^[a-zA-ZÀ-ÿ0-9 -v]+$/, "Inserisci il nome dell'attrezzo"],
    "type": ["Tipo", /.*/, ""],
    "dataName": ["Nome del dato", /.*/, ""],
    "dataContent": ["valore", /.*/, ""]
};

var dettagli_form_admin = {
    "inputUsername": ["Username", /.*/, ""],
    "inputPassword": ["Password", /.*/, ""]
};

var dettagli_dynamic_data = {};

var dettagli_dynamic_price = {
    "price": ["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto", "format"]
};

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
    var e = document.getElementById('login');
    e.style.display = 'none';
    return caricamento(dettagli_form_admin, false);
}

// Funzione che data la matrice dei campi dati, li inserisce all'interno della form e stabilisce i controlli
function caricamento(matrix, checkImg) //carica i dati nei campi
{
    if (checkImg === true) {
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
    if (input.value === "") {
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
        p.removeChild(errore);
    }
    var regex = matrix[input.id][1];
    var text = input.value;
    // if (((text == matrix[input.id][0])) || text.search(regex) != 0) //occhio! controllo che l'input sia diverso dal placeholder (con il primo check)
    if (text.search(regex) !== 0)
    {
        mostraErrore(matrix, input);
        return false;
    }
    return true;
}

function validazioneCampoDinamico(matrix, input) {
    var p = input.parentNode; //prende lo span
    var errore = document.getElementById(input.id + "errore");
    if (errore) {
        p.removeChild(errore);
    }
    var regex1 = matrix[input.id][1];
    var text = input.value;
    var companion=document.getElementById(matrix[input.id][3]);
    var c_p=companion.parentNode;
    var c_errore=document.getElementById(matrix[input.id][3] + "errore");
    var ris=true;
    if (c_errore) {
        c_p.removeChild(c_errore);
    }
    var text2 = companion.value; //prendo il valore del secondo valore
    if (((text == matrix[input.id][0])) || text.search(regex1) !== 0) //occhio! controllo che l'input sia diverso dal placeholder (con il primo check)
    {
        mostraErrore(matrix, input);
        ris = false;
    }
    if (text2 === "")
    {
        var e = document.createElement("strong");
        e.className = "errorSuggestion";
        e.id = matrix[input.id][3] + "errore";
        e.appendChild(document.createTextNode("Inserisci un formato"));
        c_p.appendChild(e);
        ris = false;
    }
    if(text === "" && text2 ==="")
        ris = true;
    return ris;
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

    if (FileUploadPath === '') {
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
            errImg(fuData);
            return false;
        }
    }
}

function validazioneFormPlant() {
    var rImg = checkImage(); 
    var rFrm = validazioneForm(dettagli_form_plant, true); 
    var vDynPrc = validazioneForm(dettagli_dynamic_price, false);
    var vDynDt = validazioneForm(dettagli_dynamic_data, true);
    var valRes= (rImg && rFrm && vDynPrc && vDynDt);
    if (valRes === true)
        dettagli_dynamic_price={};
    else document.getElementById('errors').innerHTML="Sono presenti errori, potresti ricontrollare?";
    return valRes;
}

function validazioneFormTool() {
    var rImg = checkImage(); 
    var rFrm = validazioneForm(dettagli_form_tool, true); 
    var vDynPrc = validazioneForm(dettagli_dynamic_price, false);
    var vDynDt = validazioneForm(dettagli_dynamic_data, true);
    var valRes= (rImg && rFrm && vDynPrc && vDynDt);
    if (valRes === true)
        dettagli_dynamic_price={};
    else document.getElementById('errors').innerHTML="Sono presenti errori, potresti ricontrollare?";
    return valRes;
}

function validazioneFormContattaci(){
    var ris= validazioneForm(dettagli_form_contattaci, true);
    if(ris===false)
        document.getElementById('errors').innerHTML="Sono presenti errori, potresti ricontrollare?";
    return ris;
}

function validazioneForm(matrix, Mstatica) {
    var corretto = true;
    var risultato=false;
    for (var key in matrix) {
        var input = document.getElementById(key);
        if(Mstatica===true)
            risultato = validazioneCampo(matrix, input);
        else
            risultato = validazioneCampoDinamico(matrix, input);
        corretto = corretto && risultato;
    }
    return corretto;
}

function mostraErrore(matrix, input) {
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

var counter_prezzo = 0;
var counter_valore = 0;

function addNInputData(divname, number) {
    for(var i=1; i<number; ++i){
        dettagli_dynamic_data['dataName'+i] = ["Nome del dato", /.*/, "","dataContent"+i,/.*/, ""];
        dettagli_dynamic_data['dataContent'+i] = ["valore", /.*/, ""];
        counter_valore++;
    }
    caricamento(dettagli_dynamic_data, false);
}

function addNInputPrice(divName, number) {
    var to_set={};
    for(var i=1; i<number; ++i){
        to_set['price' + i] = ["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto"];
        to_set['format' + i] = ["", /.*/, ""];
        dettagli_dynamic_price['price'+i]=["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto", "format"+i, "", /.*/, ""];
        counter_prezzo++;
    }
    caricamento(to_set, false);
}

function addInputPrice(divName) { 
    var toInsert = '<li><div class="inputsL"><label for="price" class="inputL">Prezzo (es. 7.50): &euro; </label><input type="text" name="price\[\]" id="price' + (counter_prezzo + 1) + '" class="inputL"/></div><div class="inputsR"><label for="format' + (counter_prezzo + 1) + '" class="inputR">Formato (es. al pezzo):</label><input type="text" name="format\[\]" id="format' + (counter_prezzo + 1) + '" class="inputR"/></div></li>';
    counter_prezzo = addInput(divName, counter_prezzo, toInsert);
    var to_set={};
    to_set['price' + counter_prezzo] = ["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto"];
    to_set['format' + counter_prezzo] = ["", /.*/, ""];
    dettagli_dynamic_price['price'+counter_prezzo]=["", /^\d+[\.]?(\d{1,2})?$/, "Inserisci il prezzo separato da un punto", "format"+counter_prezzo, "", /.*/, ""];
    // dettagli_dynamic_price['format'+counter_prezzo]=["", /.*/, ""];
    caricamento(to_set, false);
}

function addInputData(divName) {
    var toInsert = '<li><div class="inputsL"><label for="dataName" class="inputL">Dato (es. Altezza):</label><input type="text" name="dataName\[\]" id="dataName' + (counter_valore + 1)+'" class="inputL"/></div><div class="inputsR"><label for="dataContent' + (counter_valore + 1) + '" class="inputR">Formato (es. 10cm):</label><input type="text" name="dataContent\[\]" id="dataContent' + (counter_valore + 1) + '" class="inputR"/></div></li>';
    counter_valore = addInput(divName, counter_valore, toInsert);
    dettagli_dynamic_data['dataName'+counter_valore] = ["Nome del dato", /.*/, "","dataContent"+counter_valore,/.*/, ""];
    dettagli_dynamic_data['dataContent'+counter_valore] = ["valore", /.*/, ""];
    caricamento(dettagli_dynamic_data, false);
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
    var links = document.getElementById("minipics").getElementsByTagName("a");
    for (var i = 0; i < links.length; i++)
        links[i].onclick = function() {
            Show(this);
            return (false);
        };
}

function Show(obj) {
    var bigimg = document.getElementById("bigimage");
    bigimg.src = obj.getAttribute("href");
    var smallimg = obj.getElementsByTagName("img")[0];
    var t = document.getElementById("titolo");
    t.removeChild(t.lastChild);
    t.appendChild(document.createTextNode(smallimg.title));
}