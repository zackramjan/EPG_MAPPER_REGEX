#!/usr/bin/env python3
import sys
import re
import xml.etree.ElementTree



def readfile (fileName):
    text_file = open(fileName, "r")
    data = text_file.read()
    text_file.close()
    return data

def main() -> int:
    playlist = {}
    guide = {}
    playlistToGuide = {}
    m3uContent = readfile(sys.argv[1])
    guideContent = readfile(sys.argv[2])

    it = re.finditer("tvg-id\=\"(\w+.+?)\".+tvg-name=\"(\w+.+?)\"", m3uContent)
    for m in it:
        playlist.setdefault(m.group(1),[]).append(re.sub("\W+"," ", m.group(2)).lower())

    it = re.finditer("channel id=\"(\w+.+?)\"", guideContent)
    for m in it:
        guide[m.group(1)] = re.sub("\W+"," ", m.group(1).lower())

    for pid in playlist:
        for playlistName in playlist[pid]:
            playlistTokens = playlistName.split()
            for gid in guide:
                guideTokens = guide[gid].split()
                found = len(playlistTokens)
                for pToken in playlistTokens:
                    if pToken in guideTokens:
                        found -= 1

                if found == 0:
                    if pid in playlistToGuide:
                        if len(guideTokens) < len(guide[playlistToGuide[pid]].split()):
                            playlistToGuide[pid] = gid
                            print(pid,playlistTokens,"\t",gid,guideTokens,"BETTER MATCH",file = sys.stderr)
                    else:
                        playlistToGuide[pid] = gid 
                        print(pid,playlistTokens,"\t",gid,guideTokens,file = sys.stderr)

    #invert the dictionary for 2way lookup
    invert_playlistToGuide = {v: k for k, v in playlistToGuide.items()}

    for k in sorted(playlistToGuide):
        print(k,"->",playlistToGuide[k], file=sys.stderr)
    
    
    print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
    print("<tv generator-info-name=\"none\" generator-info-url=\"none\">")

    #walk the guide and replace ids. throw out things that are unmapped
    for event, element in xml.etree.ElementTree.iterparse(sys.argv[2], events=("start","end")):
        if element.tag == "programme" and event == "start":
            if element.get("channel") in invert_playlistToGuide:
                print(xml.etree.ElementTree.tostring(element).decode().replace(element.get("channel"),invert_playlistToGuide[element.get("channel")]))

        elif  element.tag == "channel" and event == "start":
           if element.get("id") in invert_playlistToGuide:
                print(xml.etree.ElementTree.tostring(element).decode().replace(element.get("id"),invert_playlistToGuide[element.get("id")])) 
        element.clear()

    print("</tv>")

    return 0

if __name__ == '__main__':
    sys.exit(main()) 


