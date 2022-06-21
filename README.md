# EPG_MAPPER_REGEX
#### automatically Map M3u Ids to XMLTC EPG IDs using regex. outputs a new xmltv with matching ids



usage:
    
    mapM3uGuide.pl playlist.m3u guide.xml > newguide.xml

newguide.xml will contain the guide with new ids.


Example of mapping Behavior:

Playlist:
*   id="ballysportssandiego.us"
*   desc="us bally sports san diego"
  
  
 EPG regex match:
 *   id=Bally.Sports.HDTV.San.Diego.us
