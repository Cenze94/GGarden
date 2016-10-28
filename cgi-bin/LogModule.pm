#!/usr/bin/perl
package LogModule;
use strict;
use warnings;
use XML::LibXML;
use CGI::Session;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);

sub log {
	my $xmlPage = "../data/database.xslt";
	my $parserxml = XML::LibXML->new;
	my $doc = $parserxml->load_xml(location => $xmlPage, recover => 1);
	
	#modifico il form
	my @xslUpperHTML = $doc->findnodes("//xsl:template[\@match='/']")->get_node(1)->childNodes();
	my $HTML = $xslUpperHTML[1];
	my $xpc = XML::LibXML::XPathContext->new($HTML);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	my $node = $xpc->findnodes("//x:div[\@id='contenitore-login']/x:input")->get_node(1);
	$xpc->setContextNode($node);
	$node->setAttribute('value', 'Modifica dati amministratore');
	$node = $xpc->findnodes("../x:div/x:form")->get_node(1);
	$node->setAttribute('action', '../cgi-bin/log.cgi');
	$xpc->setContextNode($node);
	$node = $xpc->findnodes("x:fieldset/x:legend/text()")->get_node(1);
	$node->setData('Modifica dati amministratore');
	$xpc->setContextNode($node);
	$node = $xpc->findnodes("../../x:div/x:input")->get_node(1);
	$node->setAttribute('value', 'yes');
	$xpc->setContextNode($node);
	$node = $xpc->findnodes("../x:button/text()")->get_node(1);
	$node->setData("Modifica");
	my $string = "<a xmlns=\'http://www.w3.org/1999/xhtml\' href='logout.cgi' class='logout' tabindex='3'>Logout</a>";
	my $child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $xpc->findnodes('..')->get_node(1);
	$node = $node->insertAfter($child, $node->lastChild);

	#inserisco i pulsanti per la gestione del database
	$xpc->setContextNode($HTML);
	$node = $xpc->findnodes("//x:div[\@id = 'piante']")->get_node(1);
	$string = "<div class='createButtons' xmlns=\'http://www.w3.org/1999/xhtml\'>
						<a href='../cgi-bin/databaseManager.cgi?operation=create&amp;tipo=pianta' class='createButton'>Inserisci nuova pianta</a>
						<a href='../cgi-bin/databaseManager.cgi?operation=create&amp;tipo=attrezzo' class='createButton'>Inserisci nuovo attrezzo</a>
				  </div>";
	$child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $node->parentNode()->insertBefore($child, $node);
	my @nodes = $xpc->findnodes("//x:p[\@class='prezzo']");
	$string = '<div class=\'productButtons\' xmlns=\'http://www.w3.org/1999/xhtml\'>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=update&amp;tipo=pianta&amp;id={$id}\' class=\'productButton\'>Modifica prodotto</a>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=delete&amp;id={$id}\' class=\'productButton\'>Elimina prodotto</a>
			   </div>';
	$child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $nodes[0]->parentNode()->insertAfter($child, $nodes[0]->lastChild()->parentNode());
	# $node = $nodes[0]->insertAfter($child, $nodes[0]->lastChild());
	$string = '<div class=\'productButtons\' xmlns=\'http://www.w3.org/1999/xhtml\'>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=update&amp;tipo=attrezzo&amp;id={$id}\' class=\'productButton\'>Modifica prodotto</a>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=delete&amp;id={$id}\' class=\'productButton\'>Elimina prodotto</a>
			   </div>';
	$child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $nodes[1]->parentNode()->insertAfter($child, $nodes[1]->lastChild()->parentNode());
	#$node = $nodes[1]->insertAfter($child, $nodes[1]->lastChild());
	#restituisco la pagina modificata
	return $doc;
}

1;