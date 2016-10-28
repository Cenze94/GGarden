#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use HTML::Entities;

sub deleteItem {
	my $filexml = '../data/database.xml';
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $item = $doc->findnodes("//p:pianta[\@id='$_[0]'] | //p:attrezzo[\@id='$_[0]']")->get_node(1);
	$item->unbindNode();
	$doc->toFile($filexml);
	require "checkLog.cgi";
}

sub updateOperation {
	my $doc = $_[0];
	my $id = $_[1];
	my $itemType = $_[2];
	my $filexml = "../data/database.xml";
	my $parserxml  = XML::LibXML->new;
	my $node = $doc->findnodes("//div[\@id='content']/form/fieldset/legend")->get_node(1);
	if($itemType eq 'pianta') {
		$node->appendTextNode('Inserisci i dati da modificare della pianta selezionata:');
	} elsif($itemType eq 'attrezzo') {
		$node->appendTextNode('Inserisci i dati da modificare dell\'attrezzo selezionato:');
	}
	$node = $node->findnodes("..")->get_node(1);
	my $string = $parserxml->parse_string("<input type='hidden' name='id' value='$id'/>");
	$string = $string->removeChild($string->firstChild());
	$node = $node->insertBefore($string, $node->firstChild());
	
	#carico i dati già salvati nel database
	my $xml = $parserxml->parse_file($filexml);
	$xml = $xml->findnodes("//p:pianta[\@id='$id'] | //p:attrezzo[\@id='$id']")->get_node(1); #dato che mi serve solo il prodotto con l'id ricevuto posso riutilizzare la variabile
	my $value = $xml->getAttribute('formato');
	if($value ne '') {
		my $imgNode = $node->findnodes("../ul/li/p[label/\@for='image']")->get_node(1);
		$string = $parserxml->parse_string("<img class='productImg' src='../img database/$id.$value' alt='Immagine attuale del prodotto' width='200' height='200' />");
		$string = $string->removeChild($string->firstChild());
		$imgNode = $imgNode->insertBefore($string, $imgNode->firstChild());
		$imgNode = $imgNode->findnodes("../label")->get_node(1);
		$imgNode->removeChildNodes();
		$imgNode->appendTextNode("Sostituisci l'immagine del prodotto già inserita (max 5 MB):");
	}
	$value = $xml->findnodes("./p:nome/text()")->get_node(1);
	$value = decode_entities($value);
	$node = $node->findnodes("../ul/li/p/input[\@name='name']")->get_node(1);
	$node->setAttribute('value', $value);
	$value = $xml->findnodes("./p:tipo/text()")->get_node(1);
	$value = decode_entities($value);
	$node = $node->findnodes("../../p/input[\@name='type']")->get_node(1);
	$node->setAttribute('value', $value);
	$node = $node->findnodes("../../../li/ul[\@id='dynamicInputPrice']/li")->get_node(1);
	my @values = $xml->findnodes("./p:prezzo/p:pacchetto");
	
	(my $price, my $format) = $values[0]->childNodes();
	$price = $price->textContent();
	$format = $format->textContent();
	$format = encode_entities($format, '<>&"');
	$node = $node->findnodes("./div[\@class='inputsL']/input[\@id='price']")->get_node(1);
	
	$node->setAttribute('value', $price);
	$node = $node->findnodes("../../div[\@class='inputsR']/input[\@id='format']")->get_node(1);
	$node->setAttribute('value', $format);
	$node=$node->parentNode();
	for (my $i=1; $i<scalar @values; $i++) {
		(my $price, my $format) = $values[$i]->childNodes();
		$price = $price->textContent();
		$format = $format->textContent();
		$format = encode_entities($format);
		$string = $parserxml->parse_string("<li>
			<div class='inputsL'>
				<label for='price'  class='inputL'>Prezzo (es. 7.50): &#8364; </label>
				<input type='text' name='price[".$i."]' id='price' class='inputL' value='$price'/>
			</div><div class='inputsR'>
				<label for='format".$i."' class='inputR'>Formato (es. al pezzo):</label>
				<input type='text' name='format[".$i."]' id='format".$i."' class='inputR' value=\"".$format."\"/>
			</div>
		</li>");
		$string = $string->removeChild($string->firstChild());
		# if($i==0){ #L'unico figlio già presente è quello del primo dato nuovo da inserire, che voglio per ultimo
			$node = $node->parentNode()->insertAfter($string, $node);
		# } else {
		# 	$node = $node->parentNode()->insertAfter($string, $node);
		# }
	}

	$value = $xml->findnodes("./p:descrizione/text()")->get_node(1);
	$value = decode_entities($value);
	$node = $node->findnodes("../../../../li/p/textarea[\@name='description']")->get_node(1);
	$node->appendTextNode($value);
	$node = $node->findnodes("../../../li/ul[\@id='dynamicInputData']/li")->get_node(1);
	@values = $xml->findnodes("./p:dettagli/p:dato");

	(my $dataName, my $dataContent) = $values[0]->childNodes();
	$dataName = $dataName->textContent();
	$dataName = encode_entities($dataName);
	$dataContent = $dataContent->textContent();
	$dataContent = encode_entities($dataContent);
	$node = $node->findnodes("./div[\@class='inputsL']/input[\@id='dataName']")->get_node(1);
	$node->setAttribute('value', $dataName);
	$node = $node->findnodes("../../div[\@class='inputsR']/input[\@id='dataContent']")->get_node(1);
	$node->setAttribute('value', $dataContent);
	$node=$node->parentNode();
	for (my $i=1; $i<scalar @values; $i++) {
		(my $dataName, my $dataContent) = $values[$i]->childNodes();
		$dataName = $dataName->textContent();
		$dataName = encode_entities($dataName);
		$dataContent = $dataContent->textContent();
		$dataContent = encode_entities($dataContent);
		$string = $parserxml->parse_string("<li>
			<div class='inputsL'>
				<label for='dataName".$i."' class='inputL'>Dato (es. Altezza):</label>
				<input type='text' name='dataName[".$i."]' id='dataName".$i."' class='inputL' value=\"".$dataName."\"/>
			</div>
			<div class='inputsR'>
				<label for='dataContent' class='inputL'>Formato (es. 10cm):</label>
				<input type='text' name='dataContent[".$i."]' id='dataContent".$i."' class='inputR' value=\"".$dataContent."\"/>
			</div>
			</li>");
		$string = $string->removeChild($string->firstChild());
		#if($i==0){ #L'unico figlio già presente è quello del primo dato nuovo da inserire, che voglio per ultimo
		#	$node = $node->parentNode()->parentNode()->insertBefore($string, $node);
		# } 
		# else {
			$node = $node->parentNode()->insertAfter($string, $node);
		#}
	}

	$node = $node->findnodes("../../../../li/p/input[\@type='submit']")->get_node(1);
	$node->setAttribute('value', "Modifica prodotto");
	if($itemType eq 'pianta') {
		$value = $xml->findnodes("./p:nome_scientifico/text()")->get_node(1);
		$value = decode_entities($value);
		$node = $node->findnodes("../../../li/p/input[\@name='scientificName']")->get_node(1);
		$node->setAttribute('value', $value);
		$value = $xml->findnodes("./p:piantagione/text()")->get_node(1);
		$value = decode_entities($value);
		$node = $node->findnodes("../../../li/p/textarea[\@name='plantation']")->get_node(1);
		$node->appendTextNode($value);
		$value = $xml->findnodes("./p:cura/text()")->get_node(1);
		$value = decode_entities($value);
		$node = $node->findnodes("../../../li/p/textarea[\@name='care']")->get_node(1);
		$node->appendTextNode($value);
		$value = $xml->findnodes("./p:altre_info/text()")->get_node(1);
		$value = decode_entities($value);
		$node = $node->findnodes("../../../li/p/textarea[\@name='otherInfos']")->get_node(1);
		$node->appendTextNode($value);
	}
	
	print "Content-type: text/html; charset=utf-8\n\n";
	#cambiata 
	# print $doc->toStringHTML;
	print $doc;
}

sub createOperation {
	my $doc = $_[0];
	my $itemType = $_[1];
	my $node = $doc->findnodes("//div[\@id='content']/form/fieldset/legend")->get_node(1);
	if($itemType eq 'pianta') {
		$node->appendTextNode('Inserisci i dati della nuova pianta:');
	} elsif($itemType eq 'attrezzo') {
		$node->appendTextNode('Inserisci i dati del nuovo attrezzo:');
	}
	$node = $node->findnodes("../ul/li/p/input[\@type='submit']")->get_node(1);
	$node->setAttribute('value', "Aggiungi prodotto");
	print "Content-type: text/html; charset=utf-8\n\n";
	#cambiata 
	# print $doc->toStringHTML;
	print $doc;
}

my $logString = CGI->new();
my $operation = $logString->param('operation');
if($operation eq "delete") {
	my $id = $logString->param('id');
	&deleteItem($id);
} else {
	my $htmlPage = "../public_html/databaseManager.html";
	my $itemType = $logString->param('tipo');
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
	#Aggiorno il tag HTML
	my $var=$doc->findnodes('/html')->get_node(0);
	$var->removeAttribute("xmlns");
	$var->removeAttribute("lang");
	my $div = $doc->findnodes("//div[\@id='content']")->get_node(1);
	my $form = $div->findnodes("form/fieldset/input[\@name='operation']")->get_node(1);
	$form->setAttribute('value', $operation);
	$form = $div->findnodes("form/fieldset/input[\@name='itemType']")->get_node(1);
	$form->setAttribute('value', $itemType);
	$form = $div->findnodes("form/fieldset/ul/li/p/label[\@for='type']")->get_node(1);
	$form->appendTextNode("Tipo di $itemType:");
	if($itemType eq 'pianta') {
		$form = $doc->findnodes("//body")->get_node(1);
		$form->setAttribute('onload', 'caricamentoPianta();');
		$form = $div->findnodes("form")->get_node(1);
		$form->setAttribute('onsubmit', 'return validazioneFormPlant();');
	} elsif($itemType eq 'attrezzo') {
		$form = $doc->findnodes("//body")->get_node(1);
		$form->setAttribute('onload', 'caricamentoAttrezzi();');
		$form = $div->findnodes("form")->get_node(1);
		$form->setAttribute('onsubmit', 'return validazioneFormTool();');
	}
	if($itemType eq "pianta") { #aggiungo i nodi di pianta comuni ad update e create
		$form = $parserxml->parse_string("<p>
								<label for='scientificName'>Nome scientifico:</label>
								<input type='text' name='scientificName' id='scientificName'/>
							</p>");
		$form = $form->removeChild($form->firstChild());
		my $child = $div->findnodes("form/fieldset/ul/li[p/label/\@for='name']")->get_node(1);
		$child->insertAfter($form, $child->findnodes("./p[label/\@for='name']")->get_node(1));
		$child = $div->findnodes("form/fieldset/ul")->get_node(1);
		my $succChild = $child->findnodes("./li[p/input/\@name='submitOperation']")->get_node(1);
		$form = $parserxml->parse_string("<li>
							<p>
								<label for='plantation'>Piantagione:</label>
								<textarea rows='4' cols='50' name='plantation' id='plantation'></textarea>
							</p>
						</li>");
		$form = $form->removeChild($form->firstChild());
		$child->insertBefore($form, $succChild);
		$form = $parserxml->parse_string("<li>
							<p>
								<label for='care'>Cura:</label>
								<textarea rows='4' cols='50' name='care' id='care'></textarea>
							</p>
						</li>");
		$form = $form->removeChild($form->firstChild());
		$child->insertBefore($form, $succChild);
		$form = $parserxml->parse_string("<li>
							<p>
								<label for='otherInfos'>Altre informazioni:</label>
								<textarea rows='4' cols='50' name='otherInfos' id='otherInfos'></textarea>
							</p>
						</li>");
		$form = $form->removeChild($form->firstChild());
		$child->insertBefore($form, $succChild);
	}
	if($operation eq "create") {
		&createOperation($doc, $itemType);
	} elsif($operation eq "update") {
		my $id = $logString->param('id');
		&updateOperation($doc, $id, $itemType);
	}
}
