#!/usr/bin/perl
#
use warnings;
use HTML::TreeBuilder;
use HTML::Element;
use LWP::Simple;

our $wiatr = "";
our $temp = "";
our $deszcz = "";
our $cisnienie = "";

system "rm pogoda.html";
getstore("http://pogoda.interia.pl/miasta?id=11827", "pogoda.html");
my $tree = HTML::TreeBuilder->new;
$tree->parse_file("pogoda.html");
my @elements = $tree->find("table");
@elements = $elements[8]->find("td");
if ($elements[5]->as_HTML =~ /Wiatr:\s+(\d+\s+km)/)
{
	$wiatr = $1;
}
if ($elements[10]->as_HTML =~ m{<b>(\d+)</b>.*?>(\d+)<})
{
	$temp = $2;
}
if ($elements[15]->as_HTML =~ m{<b>(.+)</b>})
{
	$deszcz = $1;
}
if ($elements[16]->as_HTML =~ m{<b>(\d+)</b>})
{
	$cisnienie = $1;
}
#obrazek obrazujacy aktualny stan pogody
if ($elements[6]->as_HTML =~ m/src="(.+?)"/)
{
	getstore("http://pogoda.interia.pl$1", "obrazek.gif");
}
foreach(@ARGV)
{
	if ($_ eq "-w")
	{
		print $wiatr;
	}
	if ($_ eq "-r")
	{
		print $deszcz;
	}
	if ($_ eq "-p")
	{
		print $cisnienie . "hPa";
	}
	if ($_ eq "-t")
	{
		print $temp . "C";
	}
	print "\n";
}
