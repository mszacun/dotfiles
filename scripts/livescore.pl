#!/usr/bin/perl

use strict;
use warnings;

#################################Class Livescore################################

package Livescore;

use LWP::Simple;
use Data::Dumper;
use HTML::TreeBuilder;

sub new 
{
	my $class = shift;
	my $self = {};

	bless $self, $class;
	return $self;
}

# return array with match list

sub Find_league 
{
	my $self = shift;
	my $league = shift;
	my %leagues = %{$self->{scores}};

	foreach (keys %leagues)
	{
		if ($_ eq $league)
		{
			return @{$leagues{$_}};
		}
	}
	return ();
}

# return match with searched team

sub Find_team
{
	my $self = shift;
	my $team = shift;

	foreach my $league (keys %{$self->{scores}})
	{
		foreach (@{$self->{scores}->{$league}})
		{
			if ($$_{home} eq $team || $$_{away} eq $team)
			{
				return %{$_};
			}
		}
	}
	return ();
}

sub Update
{
	my $league;
	my %scores; # parsing results
	my $i; # match number in array
	my $self = shift;
	my $content = get("http://livescore.com/");
	my $tree = HTML::TreeBuilder->new;

	$tree->parse($content);
	$tree->eof;
	my @lines = $tree->look_down("_tag", "tr");
	foreach my $line (@lines)
	{
	#	let's find league name
		if ($line->as_HTML =~ m{<td.*? class="title".*<b>(.*?)</b>(.*?)</td>})
		{
			$league = $1 . $2;
			$i = 0;
			next; 
		}
	#	let's find scores
		if ($line->as_HTML =~ m{<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(?:<a.*?>)?(.*?)(?:</a>)?</td><td.*?>(.*?)</td>}s) # it's a kind of magic :)
		{
			next if (!$league);
			$scores{$league}[$i]{"home"} = $2;
			$scores{$league}[$i]{"away"} = $4;
			$scores{$league}[$i]{"score"} = $3;
	#		let's find time
			my $time = $1;
			$time =~ s/&nbsp;//;
			if ($time =~ m{(?:<img.*?>)?(.+)})
			{
				$time = $1;
				if ($time =~ /([0-9:]+)/)
				{
					$time = $1;
				}
			}
			$scores{$league}[$i]{"time"} = $time;
			$i++
		}
	}
	$$self{"scores"} = \%scores;
}
1;

#############################End of class Livescore#############################

our $team_width = 20;
our $time_width = 8;
our @priority = ("England - Premier League", "Poland - Ekstraklasa");

sub Print_match
{
	my $match = shift; # reference to hash containing match result
	my $spaces = $time_width - length($$match{time}); # number of spaces betwin team names and score

	print $$match{time};
	print " " x ($time_width - length($$match{time}));
	print $$match{home};
	print " " x $spaces;
	print $$match{score};
	print " " x $spaces;
	print $$match{away} . "\n";
}

my $scores = Livescore->new;
$scores->Update;
my %liverpool_match = $scores->Find_team("Liverpool");
foreach my $league (@priority)
{
	my @match_list = $scores->Find_league($league);
	if (@match_list)
	{
		push @match_list, \%liverpool_match 
			if (%liverpool_match && $league ne "England - Premier League");
		foreach my $match (@match_list)
		{
			print "|   +-- \${color #CCCCCC}";
			Print_match($match);
			print "\${color yellow}";
			print "   ";
		}
		last;
	}
}
