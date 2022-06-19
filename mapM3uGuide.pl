#!/usr/bin/perl
use Data::Dumper;

$M3U_FILE = $ARGV[0] || die "specifiy m3u playlist";
$GUIDE_FILE = $ARGV[1] || die "specifiy xml guide file";

#load the contents of the files
my $m3uContent = do{local(@ARGV,$/)=$M3U_FILE;<>};
my $guideContent = do{local(@ARGV,$/)=$GUIDE_FILE;<>};

my %playlist; #map of playlist ID to playlist description/name
my %guide; #map of guide id to guide name
my %playlistToGuide; #mappig if playlist id to guide id, for the new guide


while ($m3uContent =~ /tvg-id\=\"(\w+.+?)\".+tvg-name=\"(\w+.+?)\"/g)
{
	my $m3uID=$1;
	my $m3uName=$2;
	$m3uName =~ s/\W+/ /g;
	push(@{$playlist{$m3uID}},lc($m3uName));
}
#print Dumper(%playlist);

while ($guideContent =~ /channel id=\"(\w+.+?)\"/g)
{
	my $guideID=$1;
	my $guideIDClean = $guideID;;
	$guideIDClean =~ s/\W+/ /g;
	$guide{$guideID} = lc $guideIDClean;
}


for my $pid (keys %playlist)
{
	for my $playlistName (@{$playlist{$pid}})
	{
		print STDERR "$pid<$playlistName>\n";
		@playlistTokens = split /\s+/,$playlistName;
		for my $gid (keys %guide)
		{
			my @guideTokens = split /\s+/,$guide{$gid};
			my $found = scalar @playlistTokens;
			for my $ptoken (@playlistTokens)
			{
				$found-- if $ptoken ~~ @guideTokens;		
			}

			#we have matched all tokens in the playlist name/desc
			if($found == 0)
			{
				print STDERR "\tMATCH: $pid<$playlistName}> = $gid<$guide{$gid}>\n";

				#we may have found a match that was better than the previous match, if its a closer match, replace it
				if($playlistToGuide{$pid})
				{
					my @prevGuideTokens = split /\s+/,$guide{$playlistToGuide{$pid}};
					if($#guideTokens < $#prevGuideTokens)
					{
						print STDERR  "\t\tBETTER MATCH, REPLACING $playlistToGuide{$pid} $guide{$playlistToGuide{$pid}}\n";
						$playlistToGuide{$pid} = $gid;
					}
				}

				#otherwise this is the first and only match so far
				else
				{
					$playlistToGuide{$pid} = $gid;
				}
			}
		}
	}	
}

#print the mapping to debug, and then display the new remapped guide
for my $pid (sort keys %playlistToGuide)
{ 
	$oldgid = $playlistToGuide{$pid};
	print STDERR "[$pid] -> [$oldgid]\n";
	$guideContent =~ s/\Q"$oldgid"/\"$pid\"/g;
}
print $guideContent;
