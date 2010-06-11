#!/usr/bin/perl
#
use warnings;
use HTML::TreeBuilder;
use HTML::Element;
use LWP::Simple;

our %wyniki;
our $ilosc_spacji = 7; # ilosc spacji jaka dzieli dwa wyniki w conky

my $html = get("http://pogoda.interia.pl/miasta?id=11827");
my $tree = HTML::TreeBuilder->new;
$tree->parse($html);
$tree->eof;
my @elements = $tree->find("table");
@elements = $elements[8]->find("td");
if ($elements[5]->as_HTML =~ /Wiatr:\s+(\d+)/)
{
	$wyniki->{"teraz"}->{"wiatr"} = $1;
}
if ($elements[8]->as_HTML =~ /Wiatr:\s+(\d+)/)
{
	$wyniki->{"potem"}->{"wiatr"} = $1;
}
if ($elements[10]->as_HTML =~ m{<b>(\d+)</b>.*?>(\d+)<})
{
	$wyniki->{"teraz"}->{"temperatura"} = $2;
}
if ($elements[12]->as_HTML =~ m{<b>(\d+)</b>.*?>(\d+)<})
{
	$wyniki->{"potem"}->{"temperatura"} = $2;
}
if ($elements[15]->as_HTML =~ m{<b>(.+) mm</b>})
{
	$wyniki->{"teraz"}->{"deszcz"} = $1;
}
if ($elements[17]->as_HTML =~ m{<b>(.+) mm</b>})
{
	$wyniki->{"potem"}->{"deszcz"} = $1;
}
if ($elements[14]->as_HTML =~ m{<b>(\d+)</b>})
{
	$wyniki->{"teraz"}->{"cisnienie"} = $1;
}
if ($elements[16]->as_HTML =~ m{<b>(\d+)</b>})
{
	$wyniki->{"potem"}->{"cisnienie"} = $1;
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
		print $wyniki->{"teraz"}->{"wiatr"} . " "x ($ilosc_spacji - length($wyniki->{"teraz"}->{"wiatr"})) . $wyniki->{"potem"}->{"wiatr"};
	}
	if ($_ eq "-r")
	{
		print $wyniki->{"teraz"}->{"deszcz"} . " " x ($ilosc_spacji - length($wyniki->{"teraz"}->{"deszcz"})). $wyniki->{"potem"}->{"deszcz"};
	}
	if ($_ eq "-p")
	{
		print $wyniki->{"teraz"}->{"cisnienie"} . " " x ($ilosc_spacji - length($wyniki->{"teraz"}->{"cisnienie"})). $wyniki->{"potem"}->{"cisnienie"};
	}
	if ($_ eq "-t")
	{
		print $wyniki->{"teraz"}->{"temperatura"} . " " x ($ilosc_spacji - length($wyniki->{"teraz"}->{"temperatura"})). $wyniki->{"potem"}->{"temperatura"};
	}
	print "\n";
}
