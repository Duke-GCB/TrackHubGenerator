__author__ = 'dcl9'
from jinja2 import Environment, PackageLoader
from render import render_template
import argparse
import yaml

def generate_track_dict(protein, assembly, site_width):
    env = Environment(loader=PackageLoader(package_name='render'))
    template = env.get_template('tracks.yaml.j2')
    vals = { 'protein' : protein, 'assembly': assembly, 'site_width' : site_width}
    yaml_str = template.render(vals)
    return yaml.load(yaml_str)


def render_track_variants(proteins, assembly, site_width):
    tracks = []
    for protein in proteins:
        tracks = tracks + generate_track_dict(protein, assembly, site_width)
    trackdb = {'tracks': tracks}
    render_template(trackdb, 'trackDb')


def main():
    parser = argparse.ArgumentParser(description='Render trackDb.txt')
    parser.add_argument('--proteins', nargs='+')
    parser.add_argument('--assembly')
    parser.add_argument('--site_width')
    args = parser.parse_args()
    render_track_variants(args.proteins, args.assembly, args.site_width)


if __name__ == '__main__':
    main()
