import sys
import yaml
from jinja2 import Environment, PackageLoader

def render_trackdb(track_dicts):
    env = Environment(loader=PackageLoader('trackhub_generator', 'templates'))
    template = env.get_template('trackDb.j2')
    print template.render(track_dicts)


with open(sys.argv[1]) as tracks_yaml:
    tracks = yaml.load(tracks_yaml)
    render_trackdb(tracks)
