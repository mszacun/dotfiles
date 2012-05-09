#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use feature 'unicode_strings';

use LWP::UserAgent;
use HTML::TreeBuilder;
use YAML;

# check if it's weekend
my @time = localtime;
exit if ($time[6] > 5 || $time[6] == 0);

sub Display;

our %wyniki;
our @weekdays = qw /NULL Poniedzialek Wtorek Sroda Czwartek Piatek/;
our @countries = qw /Polska USA Niemcy/;
our @data = ("Stopa bezrobocia", "	Inflacja CPI M/M", "Inflacja CPI R/R",
	"Indeks PMI przemyslu", "Stopa procentowa", "PKB R/R", "PKB K/K",
	"Inflacja PPI R/R", "Inflacja PPI M/M", "Produkcja przemyslowa R/R",
	"Bazowa inflacja CPI R/R", "Sprzedaz detaliczna R/R", "Wnioski o kredyt hipoteczny",
	"Zapasy ropy Crude", "Nowozarejestrowani bezrobotni");
our %old;
our $infos;
if (-e "/tmp/economy.yaml")
{
	$infos = YAML::LoadFile("/tmp/economy.yaml");
	if (defined $infos->{Events})
	{
		%old = %{$infos->{Events}};
	}
}

my $ua = LWP::UserAgent->new;
my $content = $ua->get("http://stooq.pl/kalendarium/");
my $weekday;
if ($content->is_success)
{
	my $temp = $content->decoded_content;
	my $tree = HTML::TreeBuilder->new;
	$tree->parse($temp);
	$tree->eof;

	my @rows = $tree->look_down("_tag", "tr");
	foreach (@rows)
	{
		my $content = $_->as_HTML;
		if ($_->as_HTML =~ m{<td colspan="8"><b><a.*?>(.*?),})
		{
			my $temp = $1;
			$temp =~ s/&#x105;/a/gs;
			$temp =~ s/&#x142;/l/gs;
			$temp =~ s/&#x15A;/S/gs;
			$weekday = $temp;
		}
		if ($_->as_HTML =~ m{<td align="right">(.*?)</td>.*?<td.*/td>.*?<td><a.*?>(.*?)<.*?<td.*?/td>.*?<td>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td id=.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
		{
			my @captured = ($1, $2, $3, $4, $5, $6, $7);
			foreach (@captured)
			{
				s/&#x105;/a/g;
				s/&#x142;/l/g;
				s/&oacute;/o/g;
				s/&nbsp;/ /g;
				s/&#x15A;/S/g;
				s/&#x17C;/z/g;
				s/&#x144;/n/g;
				s/&#x15B;/s/g;
				s/&#x17A;/z/g;
				s/&#x107;/c/g;
				if (m/^\s*$/)
				{
					$_ = "---";
				}
			}
			$wyniki{$weekday}->{$captured[1]}->{$captured[2]} = {now => $captured[4], expected => $captured[5], previously => $captured[6]};
		}
	}
	$infos->{Events} = \%wyniki;
	YAML::DumpFile("/tmp/economy.yaml", $infos);
}
else
{
	%wyniki = %old;
}

print "\n   +-- \${color #4477AA}Macroeconomy: \${color yellow}\n";
my ($s, $m, $h, $d, $mon, $y, $day_of_week, $day_of_year) = localtime;
$weekday = $weekdays[$day_of_week];
foreach my $country (@countries)
{
	next unless exists $wyniki{$weekday}->{$country};
	my %items;

	foreach (@data)
	{
		if (exists $wyniki{$weekday}->{$country}->{$_})
		{
			if (exists $old{$weekday}->{$country}->{$_})
			{
				if ($old{$weekday}->{$country}->{$_}->{now} ne $wyniki{$weekday}->{$country}->{$_}->{now})
				{
					system "notify-send \"$country\" \"$_: " . $wyniki{$weekday}->{$country}->{$_}->{previously} . " -> " . $wyniki{$weekday}->{$country}->{$_}->{now} . " (" . $wyniki{$weekday}->{$country}->{$_}->{expected} . ")\"";
				}
			}
			$items{$_} = $wyniki{$weekday}->{$country}->{$_};
		}
	}
	Display($country, \%items);
}


sub Display
{
	my ($country, $ref) = @_;
	my %hash = %$ref;

	if (scalar %hash)
	{
		print "   |   +-- \${color #888888}$country:\${color yellow}\n";
		foreach (keys %hash)
		{
			print "   |   |   +-- \${color #888888}" . $_ . ": \${color #CCCCCC}" . $hash{$_}->{previously} . " " . $hash{$_}->{expected} . " " . $hash{$_}->{now} . "\${color yellow}\n";
		}
	}
}
