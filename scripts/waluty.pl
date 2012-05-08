#!/usr/bin/perl

use strict;
use warnings;
use LWP::UserAgent;
use YAML;

my @time = localtime;
exit if ($time[6] > 5 || $time[6] == 0);

our %old;
our %waluty;
our $infos;
if (-e "/tmp/economy.yaml")
{
	$infos = YAML::LoadFile("/tmp/economy.yaml");
	if (defined $infos->{Currencies})
	{
		%old = %{$infos->{"Currencies"}};
	}
}

my $ua = LWP::UserAgent->new;
my $response = $ua->get('http://mojeinwestycje.interia.pl/wal/wal_on');
if ($response->is_success)
{
	my $html = $response->decoded_content;

	my @wynik = ($html =~ m{.*?<b>(\w+)/(\w+).*?<td.*?</td>.*?<td.*?</td>.*?<b>(.*?)</b>.*?<b>(.*?)</b>}sg);
	for (my $i = 0; $i * 4 < $#wynik; $i++)
	{
		$waluty{$wynik[4*$i] . "/" . $wynik[4*$i+1]} = {kurs => $wynik[4*$i + 2], zmiana => $wynik[4*$i + 3]};
	}
	$infos->{Currencies} = \%waluty;
	YAML::DumpFile("/tmp/economy.yaml", $infos);
}
else
{
	%waluty = %old;
}
print "   +-- \${color #4477AA}Currencies: \${color yellow}\n";
foreach (qw{ EUR/PLN USD/PLN CHF/PLN EUR/USD })
{
	print "   |    +-- \${color #888888} $_: \${color #CCCCCC} " . $waluty{$_}->{kurs} . " " . $waluty{$_}->{zmiana} . "\${color yellow}\n";
}
