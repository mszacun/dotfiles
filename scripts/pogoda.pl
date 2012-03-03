#!/usr/bin/perl
#
use warnings;
use HTML::TreeBuilder;
use HTML::Element;
use LWP::Simple;

our %wyniki;
our $ilosc_spacji = 9; # ilosc spacji jaka dzieli dwa wyniki w conky

my $html = get("http://pogoda.interia.pl/miasta?id=11827");

# nowa wersja
my @wiatr = ($html =~ m{<b>Wiatr: (\d+)}g);
$wyniki->{"teraz"}->{"wiatr"} = $wiatr[0];
$wyniki->{"potem"}->{"wiatr"} = $wiatr[1];

my @deszcz = ($html =~ m{Deszcz: <b>([\d.]+)}g);
$wyniki->{teraz}->{deszcz} = $deszcz[0];
$wyniki->{potem}->{deszcz} = $deszcz[1];

my @temperatura = ($html =~ m{<td.*?<b>([-\d]+)</b>/<span.*?>([-\d]+)</span>/<span class="tex3B">([-\d]+)</span>}g);
$wyniki->{teraz}->{temperatura} = $temperatura[0] . "/" . $temperatura[1] . "/" . $temperatura[2];
$wyniki->{potem}->{temperatura} = $temperatura[3] . "/" . $temperatura[4] . "/" . $temperatura[5];

my @cisnienie = ($html =~ m{<td.*?>.*?<b>(\d+)</b> hPa.*?<img.*?</td>}g);
$wyniki->{teraz}->{cisnienie} = $cisnienie[0];
$wyniki->{potem}->{cisnienie} = $cisnienie[1];
#obrazek obrazujacy aktualny stan pogody
if ($html =~ m{<td width="62" rowspan="3" align="left"><img src="(.*?)" width="52" height="52" border="0" alt=""></td>})
{
	getstore("http://pogoda.interia.pl/$1", "/tmp/obrazek.gif");
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
