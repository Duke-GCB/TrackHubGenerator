import sys
import yaml


def render_trackdb(track_dicts):
    for t in track_dicts['tracks']:
        print "track {}".format(t['track_name'])
        print "bigDataUrl {}".format(t['bigwig_url'])
        print "shortLabel {}".format(t['short_label'])
        print "longLabel {}".format(t['long_label'])
        print "type bigWig"
        print "visibility full"
        print "color 200,100,0"
        print "altColor 0,100,200"
        print "priority 20"
        print ""


with open(sys.argv[1]) as tracks_yaml:
    tracks = yaml.load(tracks_yaml)
    render_trackdb(tracks)
