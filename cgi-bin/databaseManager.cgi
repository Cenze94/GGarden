#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);
use CGI;

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
	my $node = $doc->findnodes("//div[\@id='content']/form/h4")->get_node(1);
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
		my $imgNode = $node->findnodes("../fieldset/ul/li/p[label/\@for='image']")->get_node(1);
		$string = $parserxml->parse_string("<img class='productImg' src='../img database/$id.$value' alt='Immagine attuale del prodotto' width='200' height='200' />");
		$string = $string->removeChild($string->firstChild());
		$imgNode = $imgNode->insertBefore($string, $imgNode->firstChild());
		$imgNode = $imgNode->findnodes("../label")->get_node(1);
		$imgNode->removeChildNodes();
		$imgNode->appendTextNode("Sostituisci l'immagine del prodotto già inserita (max 5 MB):");
	}
	$value = $xml->findnodes("./p:nome/text()")->get_node(1);
	$node = $node->findnodes("../fieldset/ul/li/p/input[\@name='name']")->get_node(1);
	$node->setAttribute('value', $value);
	$value = $xml->findnodes("./p:tipo/text()")->get_node(1);
	$node = $node->findnodes("../../p/input[\@name='type']")->get_node(1);
	$node->setAttribute('value', $value);
	$node = $node->findnodes("../../../li/p/label[\@for='price']")->get_node(1);
	my @values = $xml->findnodes("./p:prezzo/p:pacchetto");
	$string = $parserxml->parse_string("<ul></ul>");
	$string = $string->removeChild($string->firstChild());
	$node = $node->parentNode();
	$node = $node->insertBefore($string, $node->firstChild());
	for (my $i=0; $i<scalar @values; $i++) {
		(my $price, my $format) = $values[$i]->childNodes();
		$price = $price->textContent();
		$format = $format->textContent();
		$string = $parserxml->parse_string("<li>
			<input type='button' id='buttonPrice$i' value='X' size='3'/>
			<span class='existingPrices'> &#8364; $price $format</span>
		</li>");
		$string = $string->removeChild($string->firstChild());
		$node = $node->parentNode()->insertBefore($string, $node);
	}
	$value = $xml->findnodes("./p:descrizione/text()")->get_node(1);
	$node = $node->findnodes("../../../li/p/textarea[\@name='description']")->get_node(1);
	$node->appendTextNode($value);
	$node = $node->findnodes("../../../li/p/label[\@for='dataName']")->get_node(1);
	@values = $xml->findnodes("./p:dettagli/p:dato");
	$string = $parserxml->parse_string("<ul></ul>");
	$string = $string->removeChild($string->firstChild());
	$node = $node->parentNode();
	$node = $node->insertBefore($string, $node->firstChild());
	for (my $i=0; $i<scalar @values; $i++) {
		(my $dataName, my $dataContent) = $values[$i]->childNodes();
		$dataName = $dataName->textContent();
		if($dataName ne '') {
			$dataName = $dataName.': ';
		}
		$dataContent = $dataContent->textContent();
		$string = $parserxml->parse_string("<li>
			<input type='button' id='buttonData$i' value='X' size='3'/>
			<span class='existingData'> $dataName$dataContent</span>
		</li>");
		$string = $string->removeChild($string->firstChild());
		$node = $node->parentNode()->insertBefore($string, $node);
	}
	$node = $node->findnodes("../../../li/p/input[\@type='submit']")->get_node(1);
	$node->setAttribute('value', "Modifica prodotto");
	if($itemType eq 'pianta') {
		$value = $xml->findnodes("./p:nome_scientifico/text()")->get_node(1);
		$node = $node->findnodes("../../../li/p/input[\@name='scientificName']")->get_node(1);
		$node->setAttribute('value', $value);
		$value = $xml->findnodes("./p:piantagione/text()")->get_node(1);
		$node = $node->findnodes("../../../li/p/textarea[\@name='plantation']")->get_node(1);
		$node->appendTextNode($value);
		$value = $xml->findnodes("./p:cura/text()")->get_node(1);
		$node = $node->findnodes("../../../li/p/textarea[\@name='care']")->get_node(1);
		$node->appendTextNode($value);
		$value = $xml->findnodes("./p:altre_info/text()")->get_node(1);
		$node = $node->findnodes("../../../li/p/textarea[\@name='otherInfos']")->get_node(1);
		$node->appendTextNode($value);
	}
	
	print "Content-type: text/html; charset=utf-8\n\n";
	print "<phtml>";
	print "<body>";
	print $doc;
	print "</body>";
	print "</phtml>";
}

sub createOperation {
	my $doc = $_[0];
	my $itemType = $_[1];
	my $node = $doc->findnodes("//div[\@id='content']/form/h4")->get_node(1);
	if($itemType eq 'pianta') {
		$node->appendTextNode('Inserisci i dati della nuova pianta:');
	} elsif($itemType eq 'attrezzo') {
		$node->appendTextNode('Inserisci i dati del nuovo attrezzo:');
	}
	$node = $node->findnodes("../fieldset/ul/li/p/input[\@type='submit']")->get_node(1);
	$node->setAttribute('value', "Aggiungi prodotto");
	print "Content-type: text/html; charset=utf-8\n\n";
	print "<phtml>";
	print "<body>";
	print $doc;
	print "</body>";
	print "</phtml>";
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
	my $div = $doc->findnodes("//div[\@id='content']")->get_node(1);
	my $form = $div->findnodes("form/fieldset/input[\@name='operation']")->get_node(1);
	$form->setAttribute('value', $operation);
	$form = $div->findnodes("form/fieldset/input[\@name='itemType']")->get_node(1);
	$form->setAttribute('value', $itemType);
	$form = $div->findnodes("form/fieldset/ul/li/p/label[\@for='type']")->get_node(1);
	$form->appendTextNode("Tipo di $itemType:");
	if($iteType eq 'pianta') {
		$form = $doc->findnodes("body")->get_node(1);
		$form->setAttribute('onload', 'caricamentoPianta();');
		$form = $div->findnodes("form")->get_node(1);
		$form->setAttribute('onsubmit', 'return validazioneFormPlant();');
	} elsif($itemType eq 'attrezzo') {
		$form = $doc->findnodes("body")->get_node(1);
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
