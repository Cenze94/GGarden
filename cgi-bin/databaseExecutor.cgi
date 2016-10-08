#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);
use CGI;

sub error{
	my $type = $_[0];
	my $wrongData = $_[1];
	my $message;
	if($type eq 'update') {
		$message = "Errore durante la modifica dei dati: formato errato di $wrongData";
	} elsif($type eq 'insert') {
		$message = "Errore durante l'inserimento dei dati: formato errato di $wrongData";
	}
	my $doc = LogModule::log();
	
	my @xslUpperHTML = $doc->findnodes("//xsl:template[\@match='/']")->get_node(1)->childNodes();
	my $HTML = $xslUpperHTML[1];
	my $xpc = XML::LibXML::XPathContext->new($HTML);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	my $node = $xpc->findnodes("//x:div[\@id='createButtons']")->get_node(1);
	my $parserxml = XML::LibXML->new;
	my $string = $parserxml->parse_string("<p class='errorExecutor'>$message</p>");
	$string = $string->removeChild($string->firstChild());
	$node->parent()->insertAfter($string, $node);
	
	my $filexml = "../data/database.xml";
	my $parserxslt = XML::LibXSLT->new;
	my $stylesheet  = $parserxslt->parse_stylesheet($doc);
	my $results     = $stylesheet->transform_file($filexml);
	my $fileToPrint = $stylesheet->output_as_bytes($results);

	print "Content-type: text/html; charset=utf-8\n\n";
	print "<phtml>";
	print "<body>";
	print $fileToPrint;
	print "</body>";
	print "</phtml>";
}

sub createPlantItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	#carico il parser e ricavo l'id da usare
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $id = $doc->findnodes('(//@id)[last()]')->get_node(1)->textContent();
	$id = $id + 1;
	for(my $i=length($id); $i<8; $i++) {
		$id = '0'.$id;
	}
	
	#Creo l'oggetto da inserire nell'XML
	my @prices = @{$_[4]};
	my @formats = @{$_[5]};
	my @dataNames = @{$_[7]};
	my @dataContents = @{$_[8]};
	my $item = $parser->parse_string("<p:pianta id='$id' formato='$_[0]' $namespace>
		<p:nome>$_[1]</p:nome>
		<p:nome_scientifico>$_[2]</p:nome_scientifico>
		<p:tipo>$_[3]</p:tipo>
		<p:prezzo></p:prezzo>
		<p:descrizione>$_[6]</p:descrizione>
		<p:dettagli></p:dettagli>
		<p:piantagione>$_[9]</p:piantagione>
		<p:cura>$_[10]</p:cura>
		<p:altre_info>$_[11]</p:altre_info>
	</p:pianta>"); #il namespace mi serve per poter aggiungere direttamente i prefissi, altrimenti lo script non funziona
	my $child = $item->findnodes("//p:prezzo")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());;
		$child->appendChild($string);
	}
	$child = $item->findnodes("//p:dettagli")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$item = $item->removeChild($item->firstChild());
	$child = $doc->getDocumentElement();
	$child = $child->appendChild($item);
	$doc->toFile($filexml);
	require "checkLog.cgi";
}

sub createToolItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	#carico il parser e ricavo l'id da usare
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $id = $doc->findnodes('(//@id)[last()]')->get_node(1)->textContent();
	$id = $id + 1;
	for(my $i=length($id); $i<8; $i++) {
		$id = '0'.$id;
	}
	
	#Creo l'oggetto da inserire nell'XML
	my @prices = @{$_[3]};
	my @formats = @{$_[4]};
	my @dataNames = @{$_[6]};
	my @dataContents = @{$_[7]};
	my $item = $parser->parse_string("<p:attrezzo id='$id' formato='$_[0]' $namespace>
		<p:nome>$_[1]</p:nome>
		<p:tipo>$_[2]</p:tipo>
		<p:prezzo></p:prezzo>
		<p:descrizione>$_[5]</p:descrizione>
		<p:dettagli></p:dettagli>
	</p:attrezzo>"); #il namespace mi serve per poter aggiungere direttamente i prefissi, altrimenti lo script non funziona
	my $child = $item->findnodes("//p:prezzo")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$child = $item->findnodes("//p:dettagli")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$item = $item->removeChild($item->firstChild());
	$child = $doc->getDocumentElement();
	$child = $child->appendChild($item);
	$doc->toFile($filexml);
	require "checkLog.cgi";
}

sub updatePlantItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $item = $doc->findnodes("//p:pianta[\@id='$_[0]']")->get_node(1);
	if($_[1] ne "") { #imageformat
		$item->setAttribute('formato', "$_[1]");
	}
	if($_[2] ne "") { #name
		my $child = $item->findnodes("./p:nome")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[2]);
	}
	if($_[3] ne "") { #scientificName
		my $child = $item->findnodes("./p:nome_scientifico")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[3]);
	}
	if($_[4] ne "") { #type
		my $child = $item->findnodes("./p:tipo")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[4]);
	}
	if($_[5] ne "" && $_[6] ne "") { #prices e formats
		my $pricesNode = $item->findnodes("./p:prezzo")->get_node(1);
		$pricesNode->removeChildNodes();
		my @prices = @{$_[5]};
		my @formats = @{$_[6]};
		for(my $i=0; $i<scalar @prices; $i++) {
			my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
			$string = $string->removeChild($string->firstChild());
			$pricesNode->appendChild($string);
		}
	}
	if($_[7] ne "") { #description
		my $child = $item->findnodes("./p:descrizione")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[7]);
	}
	if($_[8] ne "" && $_[9] ne "") { #dataNames e dataContents
		my $detailsNode = $item->findnodes("./p:dettagli")->get_node(1);
		$detailsNode->removeChildNodes();
		my @dataNames = @{$_[8]};
		my @dataContents = @{$_[9]};
		for(my $i=0; $i<scalar @dataNames; $i++) {
			my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
			$string = $string->removeChild($string->firstChild());
			$detailsNode->appendChild($string);
		}
	}
	if($_[10] ne "") { #plantation
		my $child = $item->findnodes("./p:piantagione")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[10]);
	}
	if($_[11] ne "") { #care
		my $child = $item->findnodes("./p:cura")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[11]);
	}
	if($_[12] ne "") { #otherInfos
		my $child = $item->findnodes("./p:altre_info")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[12]);
	}
	$doc->toFile($filexml);
	require "checkLog.cgi";
}

sub updateToolItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $item = $doc->findnodes("//p:attrezzo[\@id='$_[0]']")->get_node(1);
	if($_[1] ne "") { #imageformat
		$item->setAttribute('formato', "$_[1]");
	}
	if($_[2] ne "") { #name
		my $child = $item->findnodes("./p:nome")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[2]);
	}
	if($_[3] ne "") { #type
		my $child = $item->findnodes("./p:tipo")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[3]);
	}
	if($_[4] ne "" && $_[5] ne "") { #prices e formats
		my $pricesNode = $item->findnodes("./p:prezzo")->get_node(1);
		$pricesNode->removeChildNodes();
		my @prices = @{$_[4]};
		my @formats = @{$_[5]};
		for(my $i=0; $i<scalar @prices; $i++) {
			my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
			$string = $string->removeChild($string->firstChild());
			$pricesNode->appendChild($string);
		}
	}
	if($_[6] ne "") { #description
		$item->findnodes("./p:descrizione/text()")->get_node(1)->setData($_[6]);
		my $child = $item->findnodes("./p:descrizione")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[6]);
	}
	if($_[7] ne "" && $_[8] ne "") { #dataNames e dataContents
		my $detailsNode = $item->findnodes("./p:dettagli")->get_node(1);
		$detailsNode->removeChildNodes();
		my @dataNames = @{$_[7]};
		my @dataContents = @{$_[8]};
		for(my $i=0; $i<scalar @dataNames; $i++) {
			my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
			$string = $string->removeChild($string->firstChild());
			$detailsNode->appendChild($string);
		}
	}
	$doc->toFile($filexml);
	require "checkLog.cgi";
}

my $logString = CGI->new();
my $operation = $logString->param('operation');
my $itemType = $logString->param('itemType');
my $image = $logString->param('image');
my $name = $logString->param('name');
my $type = $logString->param('type');
my @prices = $logString->param('price[]');
my @formats = $logString->param('format[]');
my $description = $logString->param('description');
my @dataNames = $logString->param('dataName[]');
my @dataContents = $logString->param('dataContent[]');
	
#Faccio il controllo dei dati in modo da segnalare eventuali errori all'utente ed evitare di proseguire con l'operazione
my $imageFormat = substr($string, rindex($string, '.')+1);
my $checkPrices = false; #dato che ho bisogno di un ciclo faccio il check prima, è l'unico array di dati su cui devo fare il check
for(my $i=0; $i<scalar @prices && $checkPrices==true; $i++) {
	if($prices[$i] !~ /[0-9]+[.][0-9]{2}$/) {
		$checkPrices = true;
	}
}
if($image ne '' && $imageFormat eq '' && $imageFormat ne 'jpeg' && $imageFormat ne 'gif' && $imageFormat ne 'png' && $imageFormat ne 'svg' && $imageFormat ne 'bmp'){
	&error($operation, "immagine caricata");
} elsif(){

} else {	
	if($itemType eq "pianta") {
		my $scientificName = $logString->param('scientificName');
		my $plantation = $logString->param('plantation');
		my $care = $logString->param('care');
		my $otherInfos = $logString->param('otherInfos');
		if($operation eq "create") {
			&createPlantItem($imageFormat, $name, $scientificName, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents, $plantation, $care, $otherInfos);
		} elsif($operation eq "update") {
			my $id = $logString->param('id');
			&updatePlantItem($id, $imageFormat, $name, $scientificName, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents, $plantation, $care, $otherInfos);
		}
	} elsif($itemType eq "attrezzo") { #inserisco la condizione anche nell'ultimo caso per evitare che un possibile errore, come una chiamata involontaria a questo script, possa compromettere il database
		if($operation eq "create") {
			&createToolItem($imageFormat, $name, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents);
		} elsif($operation eq "update") {
			my $id = $logString->param('id');
			&updateToolItem($id, $imageFormat, $name, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents);
		}
	}
}
