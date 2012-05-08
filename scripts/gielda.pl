#!/usr/bin/perl

use warnings;
use strict;

use LWP::UserAgent;
use HTML::Entities;
use YAML; 

our $wyniki;
my $infos;

my @time = localtime;
exit if ($time[6] > 5 || $time[6] == 0);

if (-e "/tmp/economy.yaml")
{
	$infos = YAML::LoadFile("/tmp/economy.yaml")
}

my $ua = LWP::UserAgent->new;
my $response = $ua->get("http://mojeinwestycje.interia.pl/gie/notgpw/notc/c_akcje");
if ($response->is_success)
{
	my $content = $response->decoded_content;
	$content =~ s/&nbsp;/ /g;

	if ($content =~ m{.*?<b>WIG20</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
	{
		$wyniki->{WIG20}->{"zmiana"} = $4 . "%";
		$wyniki->{WIG20}->{"obroty"} = $6;
		$wyniki->{WIG20}->{"wartosc"} = $3;
	}
	if ($content =~ m{.*?<b>mWIG40</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
	{
		$wyniki->{mWIG40}->{"zmiana"} = $4 . "%";
		$wyniki->{mWIG40}->{"obroty"} = $6;
		$wyniki->{mWIG40}->{"wartosc"} = $3;
	}
	if ($content =~ m{.*?<b>WIG</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
	{
		$wyniki->{WIG}->{"zmiana"} = $4 . "%";
		$wyniki->{WIG}->{"obroty"} = $6;
		$wyniki->{WIG}->{"wartosc"} = $3;
	}
	if ($content =~ m{.*?<b>sWIG80</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
	{
		$wyniki->{sWIG80}->{"zmiana"} = $4 . "%";
		$wyniki->{sWIG80}->{"obroty"} = $6;
		$wyniki->{sWIG80}->{"wartosc"} = $3;
	}
	$infos->{Gielda} = $wyniki;
}
else
{
	$wyniki = $infos->{Gielda};
}
print "\n";
print "   +-- \${color #4477AA}Stocks: \${color yellow}\n";
print "   |   +-- \${color #888888} WIG:  \${color #CCCCCC} $wyniki->{WIG}->{wartosc} $wyniki->{WIG}->{zmiana} $wyniki->{WIG}->{obroty} \${color yellow}\n";
print "   |   +-- \${color #888888} WIG20: \${color #CCCCCC} $wyniki->{WIG20}->{wartosc} $wyniki->{WIG20}->{zmiana} $wyniki->{WIG20}->{obroty} \${color yellow}\n";
print "   |   +-- \${color #888888} sWIG40:\${color #CCCCCC} $wyniki->{mWIG40}->{wartosc} $wyniki->{mWIG40}->{zmiana} $wyniki->{mWIG40}->{obroty} \${color yellow}\n";
print "   |   +-- \${color #888888} mWIG80:\${color #CCCCCC} $wyniki->{sWIG80}->{wartosc} $wyniki->{sWIG80}->{zmiana} $wyniki->{sWIG80}->{obroty} \${color yellow}\n";
print "\n";


YAML::DumpFile("/tmp/economy.yaml", $infos);
