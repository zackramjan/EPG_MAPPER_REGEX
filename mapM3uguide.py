#!/usr/bin/env python3
import sys
import re


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
        #print(m.group(1),playlist[m.group(1)])

    it = re.finditer("channel id=\"(\w+.+?)\"", guideContent)
    for m in it:
        guide[m.group(1)] = re.sub("\W+"," ", m.group(1).lower())
        #print(m.group(1),guide[m.group(1)])

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

    
    for pid in playlistToGuide:
        guideContent = guideContent.replace(playlistToGuide[pid],pid)
        print(pid," -> ", playlistToGuide[pid], file = sys.stderr)
    return 0

if __name__ == '__main__':
    sys.exit(main()) 

