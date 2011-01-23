#!/usr/bin/perl

use strict;
use warnings;

#################################Class Livescore################################

package Livescore;

use LWP::Simple;
use HTML::TreeBuilder;
use YAML::Tiny;

sub new 
{
	my $class = shift;
	my $self = {};

	bless $self, $class;
	return $self;
}

# downloads and parses information about goals in match
sub Get_match_goals
{	
	my $link = shift;

	my @results = ();
	my $content = get("http://livescore.com$link");
	my $tree = HTML::TreeBuilder->new;
	$tree->parse($content);
	$tree->eof;

	my @rows = $tree->look_down("_tag", "tr", "class", qr/(light)|(dark)/);
	foreach (@rows)
	{
		if ($_->as_HTML =~ m{<td.*?>(.*?)</td><td.*?<b>(.*?)</b>.*?(?:<td.*?></td>)?<td.*?>(.*?)<img.*?src="(.*?)"})
		{
			my $info = "$1 $2 $3";
			if ($4 eq "http://cdn3.livescore.com/img/yellow.gif")
			{
				$info .= " Yellow card";
			}
			$info =~ s/&#39;/'/;
			push @results, $info;
		}
	}
	return \@results;
}

# return hash containing info abuout matches in league

sub Find_league 
{
	my $self = shift;
	my $league = shift;
	my %leagues = %{$self->{scores}};

	foreach (keys %leagues)
	{
		if ($_ eq $league)
		{
			return %{$leagues{$_}};
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
		foreach (@{$self->{scores}->{$league}->{"matches"}})
		{
			if ($$_{home} eq $team || $$_{away} eq $team)
			{
				return %$_;
			}
		}
	}
	return ();
}

# serializes class to file in YAML format

sub Serialize
{
	my $self = shift;
	my $file_name = shift;
	my %scores = %{$self->{scores}};
	my $file;

	unless (open($file, '>', $file_name))
	{
		warn "Couldn't open file for serialize";
		return undef;
	}
	print $file Dump(%scores);
	close $file;
}

# deserializes class from file in YAML format

sub Deserialize
{
	my $self = shift;
	my $file_name = shift;
	my $file;
	
	unless (open($file, '<', $file_name))
	{
		warn "Couldn't open file for deserialize";
		return undef;
	}
	my @content = <$file>;
	my $content = join "", @content;
	my %scores = Load($content);
	$$self{scores} = \%scores;
}

sub Update
{
	my $league;
	my %scores; # parsing results
	my $i; # match number in array
	my $self = shift;
	my $with_goals = shift || 0; # do we need info about goals

	getstore("http://livescore.com/", "/tmp/scores.html");
	my $tree = HTML::TreeBuilder->new;
	$tree->parse_file("/tmp/scores.html");

	my @lines = $tree->look_down("_tag", "tr");
	foreach my $line (@lines)
	{
	#	let's find league name
		if ($line->as_HTML =~ m{<td.*? class="title".*<b>(.*?)</b>(?:</a>)? - (?:<a.*?>)?(.*?)(:?</a>)?</td>}s)
		{
			my $name = $2;
			my $country = $1;
			$name =~ s{ \(Tabela.*}{}g; # get rid of league's table link
			$league = $country . " - " . $name;
			$i = 0;
			next; 
		}
	# let's find time in country (league)
		if ($line->as_HTML =~ m{<td.*? class="match-light".*?>&nbsp;(.*?)<})
		{
			$scores{$league}{time} = $1;
		}
	#	let's find scores
		if ($line->as_HTML =~ m{<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(?:<a.*?href="(.*?)".*?>)?(.*?)(?:</a>)?</td><td.*?>(.*?)</td>}s) # it's a kind of magic :)
		{
			next if (!$league);
			$scores{$league}{"matches"}[$i]{"home"} = $2;
			$scores{$league}{"matches"}[$i]{"away"} = $5;
			$scores{$league}{"matches"}[$i]{"score"} = $4;
			# parse goals in that match
			if ($3)
			{
				my $link = $3;
				$link =~ s/&amp;/&/;
				if ($with_goals)
				{
					my $goals = Get_match_goals($link);
					$scores{$league}{"matches"}[$i]{"goals"} = $goals;
				}
				else
				{
					$scores{$league}{"matches"}[$i]{"link"} = $link;
				}
			}
	#		let's find time
			my $time = $1;
			$time =~ s/&nbsp;//;
			if ($time =~ m{(?:<img.*?>)?\s?(.+)})
			{
				$time = $1;
				if ($time =~ /([0-9:]+)/)
				{
					$time = $1;
				}
			}
			$scores{$league}{"matches"}[$i]{"time"} = $time;
			$i++
		}
	}
	$$self{"scores"} = \%scores;
}

1;

#############################End of class Livescore#############################

our $team_width = 18;
our $time_width = 8;
our @priority = ("England - Premier League", "Poland - Ekstraklasa",
	"England - FA Cup", "England - League Cup",
	"Spain - Primera Division", "Italy - Serie A",
	"Germany - Bundesliga I.", "England - League Championship",
	"France - Ligue 1",
	"Internationals - Friendly", "Internationals - Friendly (Under 21)",
	"Champions League - Group A", " Champions League - Group B",
	"Champions League - Group C", "Champions League - Group D",
	"Champions League - Group E", "Champions League - Group F",
	"Champions League - Group G", "Champions League - Group H",
	"Europa League - Group D", "Europa League - Group E",
	"Europa League - Group F", "Europa League - Group J",
	"Europa League - Group K", "Europa League - Group L",
	"International - Club World Cup", "International - Club Friendlies"
	);
our $i = 30; # number of matches, we can display

sub Print_match
{
	my $match = shift; # reference to hash containing match result
	my $spaces = $team_width - length($$match{home}); # number of spaces betwin team names and score

	print $$match{time};
	print " " x ($time_width - length($$match{time}));
	print $$match{home};
	print " " x $spaces;
	print $$match{score};
	print " " x 5;
	print $$match{away};
}

my $actual_scores = Livescore->new;
my $old_scores = Livescore->new;
$actual_scores->Update(0);
$old_scores->Deserialize("/tmp/scores.yaml");
$actual_scores->Serialize("/tmp/scores.yaml");

LINE: foreach my $league (@priority)
{
	my %league_info = $actual_scores->Find_league($league);
	if (%league_info)
	{
		my @match_list = @{$league_info{"matches"}};
		# name of league
		print "   |   +-- \${color #CCCCCC}$league   $league_info{time}\${color yellow}\n";
		print "   |   |   |\n";
		$i -= 2;
		foreach my $match (@match_list)
		{
			my %old_match = $old_scores->Find_team($$match{"home"});
			# if this match has finished than don't display it
			if (($$match{"time"} eq "FT") || ($$match{"time"} eq "HT"))
			{
				next if ($old_match{time} eq "FT");
				my @goals = @{Livescore::Get_match_goals($$match{link})};
				# body of notifiaction
				my $body = "\"$$match{home} $$match{score} $$match{away}"; 
				foreach (@goals)
				{
					$body .= "\n";
					$body .= $_;
				}
				$body .= "\"";
				if ($$match{time} eq "FT")
				{
					system "notify-send -t 10000 \"Koniec meczu\" $body ";
				}
				else
				{
					if (!($old_match{"time"} eq "HT"))
					{
						system "notify-send -t 10000 \"Koniec I polowy\" $body ";
					}
				}

			}
			# if we hadn't this match before we show notification
			if (!%old_match)
			{
				system "notify-send \"Nowy mecz\" \"$$match{time} $$match{home} $$match{score} $$match{away}\"";
			}
			print "   |   |   +-- ";
			# write this in color, if result has changed
			if ((%old_match) && ($old_match{"score"} ne $$match{"score"}) && 
				($old_match{"score"} ne "? - ?") &&
				($$match{home} ne "Liverpool"))
			{
				my @goals = @{Livescore::Get_match_goals($$match{link})};
				my $shooter = $goals[$#goals];
				system "notify-send GOOOOOAL \"$$match{home} $$match{score} $$match{away}\"\$'\n'\"$shooter\"";
				system "milena_say Go o o o o ol";
				print "\${color red}";
			}
			else
			{
				print "\${color #CCCCCC}";
			}
			Print_match($match);
			print "\${color yellow}\n";
			$i--;
			last LINE  if $i < 0;
		}
	}
}
