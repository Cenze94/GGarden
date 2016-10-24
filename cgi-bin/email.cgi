#!/usr/bin/perl
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use XML::LibXML;
use Net::SMTP;

#Carico i dati trasmessi dalla pagina e l'email del gruppo
my $logString = CGI->new();
my $name = &veryclean($logString->param('first_name'));
my $surname = &veryclean($logString->param('last_name'));
my $userEmail = &veryclean($logString->param('email'));
my $email = 'ggardengroup@gmail.com';
my $text = $clean($logString->param('comments'));

#Carico contattaci.html in modo da modificarla per comunicare all'utente se l'operazione ha avuto successo o no
my $htmlPage = "../public_html/contattaci.html";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);

#Aggiorno il link ai CSS
my $string = $doc->findnodes('//link[@href="css/home.css"]')->get_node(0);
$string->setAttribute("href", '../css/home.css');
$string = $doc->findnodes('//link[@href="css/print.css"]')->get_node(0);
$string->setAttribute("href", '../css/print.css');
$string = $doc->findnodes('//link[@href="css/small-devices.css"]')->get_node(0);
$string->setAttribute("href", '../css/small-devices.css');
$string = $doc->findnodes('//comment()')->get_node(1);
$string->setData('[if lte IE 8]><link rel="stylesheet" type="text/css" href="../css/explorer.css"/><![endif]');

#Aggiorno il link dell'immagine di Google Mpas
$string = $doc->findnodes('//a/img[@id="fotoMappa"]')->get_node(0);
$string->setAttribute("src", '../img/mappa.png');

#Aggiorno il link dello script JavaScript
$string = $doc->findnodes('//script')->get_node(0);
$string->setAttribute("src", '../script/script.js');

#Aggiorno i link alle altre pagine
my @links = $doc->findnodes('//a[@href="index.html"]');
foreach my $link(@links){
	$link->setAttribute("href", '../index.html');
}
@links = $doc->findnodes('//a[@href="realizzazioni.html"]');
foreach my $link(@links){
	$link->setAttribute("href", '../realizzazioni.html');
}
@links = $doc->findnodes('//a[@href="cgi-bin/checkLog.cgi"]');
foreach my $link(@links){
	$link->setAttribute("href", 'checkLog.cgi');
}
@links = $doc->findnodes('//a[@href="contattaci.html"]');
foreach my $link(@links){
	$link->setAttribute("href", '../contattaci.html');
}
$string = $doc->findnodes('//form[@action="cgi-bin/search.cgi"]')->get_node(0);
$string->setAttribute("action", 'search.cgi');
$string = $doc->findnodes('//form[@action="cgi-bin/email.cgi"]')->get_node(0);
$string->setAttribute("action", 'email.cgi');

#Faccio il check del formato dei dati, se viene rilevato un errore allora viene aggiunta alla pagina da stampare una riga in cui si segnala l'errore
if($name eq '' || $surname eq '' || $userEmail eq '' || (index($userEmail, '.')==-1 || index($userEmail, '@')>rindex($userEmail, '.') || $userEmail=~tr/@// != 1) || $text eq '') {
	$string = $doc->findnodes('//div[@class="body_contattaci"]/form/ul')->get_node(0);
	my $fragment = $parserxml->parse_string("<li>
		<p class='messaggio'>Errore: dato mancante o errato.</p>
	</li>");
	$fragment = $fragment->removeChild($fragment->firstChild());
	$string = $string->insertBefore($fragment, $string->firstChild());
}
else{
	#Il codice seguente è stato tratto dalla pagina https://www.studenti.math.unipd.it/index.php?id=corsi_tecweb.
	my $smtp = Net::SMTP->new('smtp.studenti.math.unipd.it',
							   Hello => 'studenti.math.unipd.it',
							   Timeout => 30,
							   Debug => 1,
	);

	$smtp->mail($userEmail);
	$smtp->to($email);
	$smtp->data();
	$smtp->datasend($name." ".$surname." ha posto la seguente domanda:\n".$text);
	$smtp->dataend();
	$smtp->quit;
}
my $redirect=0;
if($redirect) {
	my @check = $doc->findnodes('//p[@class=\'messaggio\']');
	if(scalar @check==0){
		$string = $doc->findnodes('//div[@class="body_contattaci"]/form/ul')->get_node(0);
		my $fragment = $parserxml->parse_string("<li>
			<p class='messaggio'>Errore di redirect durante l'invio dell'email.</p>
		</li>");
		$fragment = $fragment->removeChild($fragment->firstChild());
		$string = $string->insertBefore($fragment, $string->firstChild());
	}
} else {

#Controlla se è già stata aggiunta una segnalazione d'errore nella pagina, in caso negativo allora segnala che l'operazione è avvenuta con successo.
	my @check = $doc->findnodes('//p[@class=\'messaggio\']');
	if(scalar @check==0){
		$string = $doc->findnodes('//div[@class="body_contattaci"]/form/ul')->get_node(0);
		my $fragment = $parserxml->parse_string("<li>
			<p class='messaggio'>Email inviata con successo.</p>
		</li>");
		$fragment = $fragment->removeChild($fragment->firstChild());
		$string = $string->insertBefore($fragment, $string->firstChild());
	}

#stampa contattaci.html

	print "Content-type: text/html; charset=utf-8\n\n";
	print $doc->toStringHTML;
}

sub clean
{
	# Clean up any leading and trailing whitespace
	# using regular expressions.
	my $s = shift @_;
	$s =~ s/^\s+//;
	$s =~ s/\s+$//;
	return $s;
}

sub veryclean
{
	# Also forbid newlines by folding all internal whitespace to
	# single spaces. This prevents faking extra headers to cc 
	# extra people.
	my $s = shift @_;
	$s = &clean($s);
	$s =~ s/\s+$/ /g;
	return $s;
}