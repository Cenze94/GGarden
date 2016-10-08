#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use CGI::Session;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);
use LogModule;

my $session = CGI::Session->load() or die CGI::Session->errstr;
my $doc="";
if(!$session->is_expired && !$session->is_empty) {
	$doc = LogModule::log();
} else {
	my $xmlPage = "../data/database.xslt";
	my $parserxml = XML::LibXML->new;
	$doc = $parserxml->load_xml(location => $xmlPage);
}

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
