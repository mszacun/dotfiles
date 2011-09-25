#!/usr/bin/perl

use warnings;
use strict;

use LWP::Simple;
use HTML::Entities;

our %wig20;
our %mwig40;
our %swig80;
our %wig;

my @time = localtime;
exit if ($time[6] > 5 || $time[6] == 0);

my $content = get("http://mojeinwestycje.interia.pl/gie/notgpw/notc/c_akcje");
$content =~ s/&nbsp;/ /g;

print "\n";
if ($content =~ m{.*?<b>WIG20</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
{
	$wig20{"zmiana"} = $4 . "%";
	$wig20{"obroty"} = $6;
	$wig20{"wartosc"} = $3;
}
if ($content =~ m{.*?<b>mWIG40</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
{
	$mwig40{"zmiana"} = $4 . "%";
	$mwig40{"obroty"} = $6;
	$mwig40{"wartosc"} = $3;
}
if ($content =~ m{.*?<b>WIG</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
{
	$wig{"zmiana"} = $4 . "%";
	$wig{"obroty"} = $6;
	$wig{"wartosc"} = $3;
}
if ($content =~ m{.*?<b>sWIG80</b></a>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?<b>(.*?)</b>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>}s)
{
	$swig80{"zmiana"} = $4 . "%";
	$swig80{"obroty"} = $6;
	$swig80{"wartosc"} = $3;
}

print "   +-- \${color #4477AA}Stocks: \${color yellow}\n";
print "   |    +-- \${color #888888} WIG:  \${color #CCCCCC} $wig{wartosc} $wig{zmiana} $wig{obroty} \${color yellow}\n";
print "   |    +-- \${color #888888} WIG20: \${color #CCCCCC} $wig20{wartosc} $wig20{zmiana} $wig20{obroty} \${color yellow}\n";
print "   |    +-- \${color #888888} sWIG40:\${color #CCCCCC} $mwig40{wartosc} $mwig40{zmiana} $mwig40{obroty} \${color yellow}\n";
print "   |    +-- \${color #888888} mWIG80:\${color #CCCCCC} $swig80{wartosc} $swig80{zmiana} $swig80{obroty} \${color yellow}\n";

