#!/usr/bin/perl

use warnings;
use strict;

our @days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);

# fist date must be less then second
# doesnt support years, and lap year
sub Days_between($$)
{
	my $result = 0;
	my %a = %{$_[0]};
	my %b = %{$_[1]};
	# do konca miesiaca
	$result = $days_in_month[$a{month}] - $a{day};
	$a{month}++;
	while ($a{month} != $b{month})
	{
		$a{month} = 0 if $a{month} > 11;
		$result += $days_in_month[$a{month}];
		$a{month}++;
	}
	$result += $b{day};
	return $result;
}

my %a;
my %b;
$a{month} = 4;
$a{day} = 4;
my @time = localtime;
$b{day} = $time[3];
$b{month} = $time[4];
print Days_between(\%b, \%a);
