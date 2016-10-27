#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use LogModule;
use File::Basename;
use HTML::Entities;
$CGI::POST_MAX = 1024 * 5000;

sub error{
	my $type = $_[0];
	my $wrongData = $_[1];
	my $message;
	if($type eq 'update') {
		$message = "Errore durante la modifica dei dati: $wrongData";
	} elsif($type eq 'create') {
		$message = "Errore durante l'inserimento dei dati: $wrongData";
	}
	my $doc = LogModule::log();
	
	my @xslUpperHTML = $doc->findnodes("//xsl:template[\@match='/']")->get_node(1)->childNodes();
	my $HTML = $xslUpperHTML[1];
	my $xpc = XML::LibXML::XPathContext->new($HTML);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	my $node = $xpc->findnodes("//x:div[\@id='content']")->get_node(1);
	my $parserxml = XML::LibXML->new;
	my $string = $parserxml->parse_string("<p class='errorExecutor' xmlns=\'http://www.w3.org/1999/xhtml\'>$message</p>");
	$string = $string->removeChild($string->firstChild());
	$node->insertBefore($string, $node->firstChild());
	
	my $filexml = "../data/database.xml";
	my $parserxslt = XML::LibXSLT->new;
	my $stylesheet  = $parserxslt->parse_stylesheet($doc);
	my $results     = $stylesheet->transform_file($filexml);
	my $fileToPrint = $stylesheet->output_as_bytes($results);

	print "Content-type: text/html; charset=utf-8\n\n";
	print $fileToPrint;
}

sub createPlantItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	#carico il parser
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $id = $_[0];
	
	#Creo l'oggetto da inserire nell'XML
	my @prices = @{$_[5]};
	my @formats = @{$_[6]};
	my @dataNames = @{$_[8]};
	my @dataContents = @{$_[9]};
	my $item = $parser->parse_string("<p:pianta id='$id' formato='$_[1]' $namespace>
		<p:nome>$_[2]</p:nome>
		<p:nome_scientifico>$_[3]</p:nome_scientifico>
		<p:tipo>$_[4]</p:tipo>
		<p:prezzo></p:prezzo>
		<p:descrizione>$_[7]</p:descrizione>
		<p:dettagli></p:dettagli>
		<p:piantagione>$_[10]</p:piantagione>
		<p:cura>$_[11]</p:cura>
		<p:altre_info>$_[12]</p:altre_info>
	</p:pianta>"); #il namespace mi serve per poter aggiungere direttamente i prefissi, altrimenti lo script non funziona
	my $child = $item->findnodes("//p:prezzo")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		$formats[$i] = encode_entities($formats[$i]);
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$child = $item->findnodes("//p:dettagli")->get_node(1);
	my $max = 0;
	if(scalar @dataNames > scalar @dataContents) {
		$max = scalar @dataNames;
	} else {
		$max = scalar @dataContents;
	}
	for (my $i=0; $i<$max; $i++) {
		$dataNames[$i] = encode_entities($dataNames[$i]);
		$dataContents[$i] = encode_entities($dataContents[$i]);
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
	#carico il parser
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $id = $_[0];
	
	#Creo l'oggetto da inserire nell'XML
	my @prices = @{$_[4]};
	my @formats = @{$_[5]};
	my @dataNames = @{$_[7]};
	my @dataContents = @{$_[8]};
	my $item = $parser->parse_string("<p:attrezzo id='$id' formato='$_[1]' $namespace>
		<p:nome>$_[2]</p:nome>
		<p:tipo>$_[3]</p:tipo>
		<p:prezzo></p:prezzo>
		<p:descrizione>$_[6]</p:descrizione>
		<p:dettagli></p:dettagli>
	</p:attrezzo>"); #il namespace mi serve per poter aggiungere direttamente i prefissi, altrimenti lo script non funziona
	my $child = $item->findnodes("//p:prezzo")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		$formats[$i] = encode_entities($formats[$i]);
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$child = $item->findnodes("//p:dettagli")->get_node(1);
	my $max = 0;
	if(scalar @dataNames > scalar @dataContents) {
		$max = scalar @dataNames;
	} else {
		$max = scalar @dataContents;
	}
	for (my $i=0; $i<$max; $i++) {
		$dataNames[$i] = encode_entities($dataNames[$i]);
		$dataContents[$i] = encode_entities($dataContents[$i]);
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
	#scientificName
	my $child = $item->findnodes("./p:nome_scientifico")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[3]);
	#type
	my $child = $item->findnodes("./p:tipo")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[4]);
	#prices e formats, gli array contengono sicuramente almeno un valore perché il controllo viene effettuato prima dell'esecuzione di questa funzione
	my $pricesNode = $item->findnodes("./p:prezzo")->get_node(1);
	$pricesNode->removeChildNodes();
	my @prices = @{$_[5]};
	my @formats = @{$_[6]};
	for(my $i=0; $i<scalar @prices; $i++) {
		$formats[$i] = encode_entities($formats[$i]);
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());
		$pricesNode->appendChild($string);
	}
	#description
	my $child = $item->findnodes("./p:descrizione")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[7]);
	if($_[8] ne "" && $_[9] ne "") { #dataNames e dataContents
		my $detailsNode = $item->findnodes("./p:dettagli")->get_node(1);
		$detailsNode->removeChildNodes();
		my @dataNames = @{$_[8]};
		my @dataContents = @{$_[9]};
		my $max = 0;
		if(scalar @dataNames > scalar @dataContents) {
			$max = scalar @dataNames;
		} else {
			$max = scalar @dataContents;
		}
		for (my $i=0; $i<$max; $i++) {
			$dataNames[$i] = encode_entities($dataNames[$i]);
			$dataContents[$i] = encode_entities($dataContents[$i]);
			my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
			$string = $string->removeChild($string->firstChild());
			$detailsNode->appendChild($string);
		}
	}
	#plantation
	my $child = $item->findnodes("./p:piantagione")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[10]);
	#care
	my $child = $item->findnodes("./p:cura")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[11]);
	#otherInfos
	my $child = $item->findnodes("./p:altre_info")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[12]);
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
	#type
	my $child = $item->findnodes("./p:tipo")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[3]);
	#prices e formats, gli array contengono sicuramente almeno un valore perché il controllo viene effettuato prima dell'esecuzione di questa funzione
	my $pricesNode = $item->findnodes("./p:prezzo")->get_node(1);
	$pricesNode->removeChildNodes();
	my @prices = @{$_[4]};
	my @formats = @{$_[5]};
	for(my $i=0; $i<scalar @prices; $i++) {
		$formats[$i] = encode_entities($formats[$i]);
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());
		$pricesNode->appendChild($string);
	}
	#description
	$item->findnodes("./p:descrizione/text()")->get_node(1)->setData($_[6]);
	my $child = $item->findnodes("./p:descrizione")->get_node(1);
	$child->removeChildNodes();
	$child->appendTextNode($_[6]);
	if($_[7] ne "" && $_[8] ne "") { #dataNames e dataContents
		my $detailsNode = $item->findnodes("./p:dettagli")->get_node(1);
		$detailsNode->removeChildNodes();
		my @dataNames = @{$_[7]};
		my @dataContents = @{$_[8]};
		my $max = 0;
		if(scalar @dataNames > scalar @dataContents) {
			$max = scalar @dataNames;
		} else {
			$max = scalar @dataContents;
		}
		for (my $i=0; $i<$max; $i++) {
			$dataNames[$i] = encode_entities($dataNames[$i]);
			$dataContents[$i] = encode_entities($dataContents[$i]);
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
$name = encode_entities($name);
my $type = $logString->param('type');
$type = encode_entities($type);
my @prices = $logString->param('price[]');
my @formats = $logString->param('format[]');
my $description = $logString->param('description');
$description = encode_entities($description);
my @dataNames = $logString->param('dataName[]');
my @dataContents = $logString->param('dataContent[]');
	
#Faccio il controllo dei dati in modo da segnalare eventuali errori all'utente ed evitare di proseguire con l'operazione
my $imageFormat = substr($image, rindex($image, '.')+1);
my $checkPrices = 1; #dato che ho bisogno di un ciclo faccio il check prima, è l'unico array di dati su cui devo fare il check
for(my $i=0; $i<scalar @prices && $checkPrices!=0; $i++) {
	if($prices[$i] eq '' && $formats[$i] eq '') { #Elimino i prezzi con valore e formato vuoti
		splice(@prices, $i, 1);
		splice(@formats, $i, 1);
		$i = $i-1;
	} elsif($prices[$i] !~ /[0-9]+[.][0-9]{2}$/ || $formats[$i] eq '') {
		$checkPrices = 0;
	}
}
if($image ne '' && (index($image, '/')!=-1 || index($image, '..')!=-1 || $imageFormat eq '' || ($imageFormat ne 'jpeg' && $imageFormat ne 'jpg' && $imageFormat ne 'gif' && $imageFormat ne 'png' && $imageFormat ne 'svg' && $imageFormat ne 'bmp'))){
	&error($operation, "formato errato del nome dell'immagine caricata");
} elsif(scalar @prices == 0 && scalar @formats == 0) {
	&error($operation, "nessun prezzo inserito");
} elsif($checkPrices == 0){
	&error($operation, "formato errato dei prezzi");
} elsif($name eq '') {
	&error($operation, "nome del prodotto non inserito");
} else {
	my $max = 0;
	if(scalar @dataNames > scalar @dataContents) {
		$max = scalar @dataNames;
	} else {
		$max = scalar @dataContents;
	}
	for(my $i=0; $i<$max; $i++) {
		if($dataNames[$i] eq '' && $dataContents[$i] eq '') { #Elimino i dati con nome e contenuto vuoti
			splice(@dataNames, $i, 1);
			splice(@dataContents, $i, 1);
			$max = $max-1; #Se si elimina un elemento il valore della posizione dell'ultimo elemento diminuisce di uno
			$i = $i-1; #All'array viene tolto un elemento la cui posizione viene occupata dall'elemento successivo, se non viene diminuito il valore di $i questa cella verrebbe saltata
		}
	}
	my $id = "";
	if($operation eq 'create') {
		#carico il parser e ricavo l'id da usare
		my $filexml = '../data/database.xml';
		my $parser = XML::LibXML->new;
		my $doc = $parser->parse_file($filexml);
		$id = $doc->findnodes('(//@id)[last()]')->get_node(1)->textContent();
		$id = $id + 1;
		for(my $i=length($id); $i<8; $i++) {
			$id = '0'.$id;
		}
		#modifico il valore dell'immagine in modo da comunicare all'xslt che non c'è alcuna immagine da caricare
		if($image eq '') {
			$imageFormat = 'no_image';
		}
	} elsif($operation eq 'update') {
		$id = $logString->param('id');
	}
	
	#Se ho un'immagine caricata corretta allora la sostituisco già a quella esistente o creo quella nuova
	if($image ne '') {
		my $imgDir = '../public_html/img database';
		my $filehandle = $logString->upload("image");
		#Elimino l'eventuale immagine omonima già presente
		if(-e "$imgDir/$id.$imageFormat") {
			unlink "$imgDir/$id.$imageFormat";
		} elsif($operation eq 'update') { #L'immagine vecchia potrebbe avere un altro formato, quindi carico il formato vecchio salvato nel database ed eventualmente elimino il file vecchio
			my $filexml = '../data/database.xml';
			my $parser = XML::LibXML->new;
			my $doc = $parser->parse_file($filexml);
			my $oldFormat = $doc->findnodes("//p:$itemType\[\@id='$id'\]")->get_node(1)->getAttribute('formato');
			if($oldFormat ne $imageFormat && $oldFormat ne 'no_image' && -e "$imgDir/$id.$oldFormat") {
				unlink "$imgDir/$id.$oldFormat";
			}
		}
		open(UPLOADFILE, ">$imgDir/$id.$imageFormat") or die "$!";
		binmode UPLOADFILE;
		while ( <$filehandle> ){
			print UPLOADFILE;
		}
		close UPLOADFILE;
	}
	
	if($itemType eq "pianta") {
		my $scientificName = $logString->param('scientificName');
		$scientificName = encode_entities($scientificName);
		my $plantation = $logString->param('plantation');
		$plantation = encode_entities($plantation);
		my $care = $logString->param('care');
		$care = encode_entities($care);
		my $otherInfos = $logString->param('otherInfos');
		$otherInfos = encode_entities($otherInfos);
		if($operation eq "create") {
			&createPlantItem($id, $imageFormat, $name, $scientificName, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents, $plantation, $care, $otherInfos);
		} elsif($operation eq "update") { #in update uso un sistema diverso per aggiungere l'input dell'utente rispetto a create, che necessita di effettuare una decodifica per funzionare correttamente.
			$name = decode_entities($name);
			$scientificName = decode_entities($scientificName);
			$type = decode_entities($type);
			$description = decode_entities($description);
			$plantation = decode_entities($plantation);
			$care = decode_entities($care);
			$otherInfos = decode_entities($otherInfos);
			&updatePlantItem($id, $imageFormat, $name, $scientificName, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents, $plantation, $care, $otherInfos);
		}
	} elsif($itemType eq "attrezzo") { #inserisco la condizione anche nell'ultimo caso per evitare che un possibile errore, come una chiamata involontaria a questo script, possa compromettere il database
		if($operation eq "create") {
			&createToolItem($id, $imageFormat, $name, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents);
		} elsif($operation eq "update") {
			$name = decode_entities($name);
			$type = decode_entities($type);
			$description = decode_entities($description);
			&updateToolItem($id, $imageFormat, $name, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents);
		}
	}
}
