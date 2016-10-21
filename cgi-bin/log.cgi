#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;
use XML::LibXML;
use XML::LibXSLT;
use LogModule;

sub update {
	my $username=$_[0];
	my $password=$_[1];
	my $expectedUsername=$_[2];
	my $expectedPassword=$_[3];
	my $doc = &LogModule::log();
	my $xpc = XML::LibXML::XPathContext->new($doc);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	my $form = $xpc->findnodes('//x:div[@id="contenitore-login"]')->get_node(1);
	my $parserxml  = XML::LibXML->new;
	my $childString;
	if(($username ne $expectedUsername || $password ne $expectedPassword) && !($username eq '' && $password eq '')) {
		#Se ho lo username vuoto o la password vuota mantengo il dato vecchio
		if($username eq '') {
			$username = $expectedUsername;
		}
		if($password eq '') {
			$password = $expectedPassword;
		}
		$childString = "<span id='updateOk'>Modifica dei dati avvenuta con successo</span>";
		my $filexml = "../data/profili.xml";
		my $xml = $parserxml->parse_file($filexml);
		my $xnode = $xml->findnodes("//p:profilo[\@tipo = 'amministratore']/p:username")->get_node(1);
		$xnode->removeChildNodes();
		$xnode->appendTextNode($username);
		$xnode = $xnode->findnodes("../p:password")->get_node(1);
		$xnode->removeChildNodes();
		$xnode->appendTextNode($password);
		$xml->toFile($filexml);
	} else {
		$childString = "<span id='updateError' xmlns=\'http://www.w3.org/1999/xhtml\'>Dati inseriti errati</span>";
	}
	my $child = $parserxml->parse_string($childString);
	$child = $child->removeChild($child->firstChild());
	$form->insertAfter($child, $form->lastChild);
	return $doc;
}

sub logError {
	#carico l'html
	my $htmlPage = "../data/database.xslt";
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->parse_file($htmlPage);
	my $xpc = XML::LibXML::XPathContext->new($doc);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	
	#aggiungo il messaggio di errore
	my $form = $xpc->findnodes('//x:div[@id="contenitore-login"]')->get_node(1);
	my $childString = '<span id="logError" xmlns=\'http://www.w3.org/1999/xhtml\'>Dati inseriti errati</span>';
	my $child = $parserxml->parse_string($childString); #elimino il tag che identifica la versione dell'xml perché non devo aggiungerlo
	$child = $child->removeChild($child->firstChild());
	$form->insertAfter($child, $form->lastChild);
	
	#restituisco la pagina modificata
	return $doc;
}

#estraggo le parole del login
my $logString = CGI->new();
my $username = $logString->param('inputUsername');
my $password = $logString->param('inputPassword');
my $update = $logString->param('update');
my $finalDoc;

#estraggo i dati dall'XML
my $filexml = "../data/profili.xml";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->parse_file($filexml);
my $expectedUsername = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:username');
my $expectedPassword = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:password');

if($update eq "yes") {
	$finalDoc = &update($username, $password, $expectedUsername, $expectedPassword);
	print "Content-type: text/html; charset=utf-8\n\n";
} else {
	if($username eq $expectedUsername && $password eq $expectedPassword) {
		#creo la sessione
		my $session = new CGI::Session() or die CGI::Session->errstr;
		print $session->header(-charset=>'utf-8');
		$session->param('username', 'amministratore');
		$session->expire('+1h');
		$session->flush();
		$finalDoc = LogModule::log();
	} else {
		$finalDoc = &logError();
		print "Content-type: text/html; charset=utf-8\n\n";
	}
}

#applico il foglio di stile al file modificato
$filexml = "../data/database.xml";
my $parserxslt = XML::LibXSLT->new;
my $stylesheet  = $parserxslt->parse_stylesheet($finalDoc);
my $results     = $stylesheet->transform_file($filexml);
my $fileToPrint = $stylesheet->output_as_bytes($results);

print $fileToPrint;
