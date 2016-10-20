#!/usr/bin/perl
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use XML::LibXSLT;

my $session = CGI::Session->load() or die CGI::Session->errstr;
$session->delete();
my $xmlPage = "../data/database.xslt";
my $parserxml = XML::LibXML->new;
my $doc = $parserxml->load_xml(location => $xmlPage);
my $filexml = "../data/database.xml";
my $parserxslt = XML::LibXSLT->new;
my $stylesheet  = $parserxslt->parse_stylesheet($doc);
my $results     = $stylesheet->transform_file($filexml);
my $fileToPrint = $stylesheet->output_as_bytes($results);

print "Content-type: text/html; charset=utf-8\n\n";

	print $fileToPrint;