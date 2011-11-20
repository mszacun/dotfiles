#!/usr/bin/perl

use strict;
use warnings;
use LWP::Simple;

my @time = localtime;
exit if ($time[6] > 5 || $time[6] == 0);

my $html = get('http://mojeinwestycje.interia.pl/wal/wal_on');
our %waluty;

# CHF/PLN
if ($html =~ m{.*?<b>CHF/PLN.*?<td.*?</td>.*?<td.*?</td>.*?<b>(.*?)</b>.*?<b>(.*?)</b>}s)
{
	$waluty{'CHF/PLN'} = {kurs => $1, zmiana => $2};
}
if ($html =~ m{.*?<b>EUR/PLN.*?<td.*?</td>.*?<td.*?</td>.*?<b>(.*?)</b>.*?<b>(.*?)</b>}s)
{
	$waluty{'EUR/PLN'} = {kurs => $1, zmiana => $2};
}
if ($html =~ m{.*?<b>USD/PLN.*?<td.*?</td>.*?<td.*?</td>.*?<b>(.*?)</b>.*?<b>(.*?)</b>}s)
{
	$waluty{'USD/PLN'} = {kurs => $1, zmiana => $2};
}
if ($html =~ m{.*?<b>EUR/USD.*?<td.*?</td>.*?<td.*?</td>.*?<b>(.*?)</b>.*?<b>(.*?)</b>}s)
{
	$waluty{'EUR/USD'} = {kurs => $1, zmiana => $2};
}

print "+-- \${color #4477AA}Currencies: \${color yellow}\n";
foreach (keys %waluty)
{
	print "   |   +-- \${color #888888} $_: \${color #CCCCCC} " . $waluty{$_}->{kurs} . " " . $waluty{$_}->{zmiana} . "%\${color yellow}\n";
}
