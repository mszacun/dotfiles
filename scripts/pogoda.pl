#!/usr/bin/perl

use warnings;
use strict;

use LWP::UserAgent;
use Data::Dumper;

# constants
my $NAMYSLOW_INTERIA_WEATHER_URL = 
	"http://pogoda.interia.pl/prognoza-dlugoterminowa-namyslow,cId,22479";
my $TEMPERATURE_HASH_KEY = "temp";
my $MIN_TEMPERATURE_HASH_KEY = "min_temp";
my $SUNRISE_HASH_KEY = "sunrise";
my $SUNSET_HASH_KEY = "sunset";
my $WEATHER_DESCRIPTION_HASH_KEY = "description";
my $WEATHER_ICON_HASH_KEY = "icon";
my $CLOUDS_HASH_KEY = "clouds";
my $RAIN_AMOUNT_HASH_KEY = "rain";
my $WIND_SPEED_HASH_KEY = "wind_speed";
my $WIND_DIRECTION_HASH_KEY = "wind_direction";
my $PRESSURE_HASH_KEY = "pressure";

# color constants
my $CATEGORY_TITLE_COLOR = "\${color #4477AA}";
my $TITLE_COLOR = "\${color #888888}";
my $TREE_STUCTURE_COLOR = "\${color yellow}";
my $TEXT_COLOR = "\${color #CCCCCC}";

# display titles constants
my $CATEGORY_NAME = "Weather: ";
my $TEMPERATURE_TITLE = "Temp";
my $PRESSURE_TITLE = "Pres";
my $WIND_TITLE = "Wind";
my $RAIN_TITLE = "Rain";
my $DESCRIPTION_TITLE = "Desc";

my $RAIN_UNIT = "mm";
my $TEMPERATUR_UNIT = "C";
my $PRESSURE_UNIT = "hPa";
my $WIND_SPEED_UNIT = "km/h";

my $TODAY_WEATHER_INDEX = 0;

# result
my @weather;
my $i;

# get source
my $ua = LWP::UserAgent->new();
my $source = $ua->get ($NAMYSLOW_INTERIA_WEATHER_URL)->content;

# icons
my @icons = $source =~
	m{<span class="weather-forecast-longterm-list-entry-forecast-icon (.*?)"></span>}sg;
for ($i = 0; $i <= $#icons; $i++)
{
	$weather[$i]->{$WEATHER_ICON_HASH_KEY} = $icons[$i];
}

# average temperature
my @temp = $source =~
	m{<span class="weather-forecast-longterm-list-entry-forecast-temp">(-?\d*).*?</span>}sg;
for ($i = 0; $i <= $#temp; $i++)
{
	$weather[$i]->{$TEMPERATURE_HASH_KEY} = $temp[$i];
}

# min temperature
my @min_temp = $source =~
	m{<span class="weather-forecast-longterm-list-entry-forecast-lowtemp">(-?\d*).*?</span>}sg;
for ($i = 0; $i <= $#min_temp; $i++)
{
	$weather[$i]->{$MIN_TEMPERATURE_HASH_KEY} = $min_temp[$i];
}

# description
my @descriptions = $source =~
	m{<span class="weather-forecast-longterm-list-entry-forecast-phrase">(.*?)</span>}sg;
for ($i = 0; $i <= $#descriptions; $i++)
{
	$weather[$i]->{$WEATHER_DESCRIPTION_HASH_KEY} = $descriptions[$i];
}

# wind direction
my @wind_directions = $source =~ 
	m{<span class="weather-forecast-longterm-list-entry-wind-direction">(.*?)</span>}sg;
for ($i = 0; $i <= $#wind_directions; $i++)
{
	$weather[$i]->{$WIND_DIRECTION_HASH_KEY} = $wind_directions[$i];
}

# wind speed
my @wind_speeds = $source =~
	m{<span class="weather-forecast-longterm-list-entry-wind-value">(\d+)</span>}sg;
for ($i = 0; $i <= $#wind_speeds; $i++)
{
	$weather[$i]->{$WIND_SPEED_HASH_KEY} = $wind_speeds[$i];
}

# clouds
my @clouds = $source =~
	m{<span class="weather-forecast-longterm-list-entry-cloudy-cloudy-value">(\d+)<span class="cloudy-unit">%</span></span>}sg;
for ($i = 0; $i <= $#clouds; $i++)
{
	$weather[$i]->{$CLOUDS_HASH_KEY} = $clouds[$i];
}

# rain amount
my @rain_amounts = $source =~
	m{<span class="weather-forecast-longterm-list-entry-precipitation-value">(.*?)<span class="precipitation-unit">mm</span></span>}sg;
for ($i = 0; $i <=$#rain_amounts; $i++)
{
	$weather[$i]->{$RAIN_AMOUNT_HASH_KEY} = $rain_amounts[$i];
}

# preassure
my @preassures = $source =~
	m{<span class="weather-forecast-longterm-list-entry-pressure-value">(.*?)</span>}sg;
for ($i = 0; $i <= $#preassures; $i++)
{
	$weather[$i]->{$PRESSURE_HASH_KEY} = $preassures[$i];
}

# print Dumper(@weather);


print "$TREE_STUCTURE_COLOR+-- $CATEGORY_TITLE_COLOR$CATEGORY_NAME\n";
print "$TREE_STUCTURE_COLOR   |   |\n";
print "$TREE_STUCTURE_COLOR   |   +-- " .
	$TITLE_COLOR . $TEMPERATURE_TITLE . ": " 
	. $TEXT_COLOR . $weather[$TODAY_WEATHER_INDEX]->{$TEMPERATURE_HASH_KEY} .
	" " . $TEMPERATUR_UNIT . "\n";
print "$TREE_STUCTURE_COLOR   |   +-- " .
	$TITLE_COLOR . $RAIN_TITLE . ": " .
	$TEXT_COLOR . $weather[$TODAY_WEATHER_INDEX]->{$RAIN_AMOUNT_HASH_KEY} .
	" " . $RAIN_UNIT . "\n";
print "$TREE_STUCTURE_COLOR   |   +-- " .
	$TITLE_COLOR . $PRESSURE_TITLE . ": " .
	$TEXT_COLOR . $weather[$TODAY_WEATHER_INDEX]->{$PRESSURE_HASH_KEY} .
	" " . $PRESSURE_UNIT . "\n";
print "$TREE_STUCTURE_COLOR   |   +-- " .
	$TITLE_COLOR . $WIND_TITLE . ": " .
	$TEXT_COLOR . $weather[$TODAY_WEATHER_INDEX]->{$WIND_SPEED_HASH_KEY} .
	" " . $WIND_SPEED_UNIT . "\n";
print "$TREE_STUCTURE_COLOR   |   +-- " .
	$TITLE_COLOR . $DESCRIPTION_TITLE . ": " .
	$TEXT_COLOR . $weather[$TODAY_WEATHER_INDEX]->{$WEATHER_DESCRIPTION_HASH_KEY} .
	"\n";

