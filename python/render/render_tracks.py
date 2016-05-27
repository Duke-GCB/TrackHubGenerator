__author__ = 'dcl9'
from render import render_template
import argparse
import yaml


def generate_track_dict(metadata):
    d = dict()
    d['track_name'] = '{}_{}({})'.format(metadata['protein'], metadata['serial_number'], metadata['author_identifier'])
    d['bigbed_url'] = metadata['track_filename']
    d['short_label'] = '{}_{} binding sites'.format(metadata['protein'], metadata['serial_number'])
    d['long_label'] = 'Predicted {} binding sites (site width = {}, model identifier {}({}))'.format(metadata['protein'], metadata['width'], metadata['serial_number'], metadata['author_identifier'])
    return d

def render_tracks(assembly, metadata_file):
    obj = yaml.load(metadata_file)
    # Just pull out the assembly ones
    tracks = [generate_track_dict(x) for x in obj if x['assembly'] == assembly]
    trackdb = {'tracks': tracks}
    render_template(trackdb, 'trackDb')


def main():
    parser = argparse.ArgumentParser(description='Render trackDb.txt')
    parser.add_argument('--assembly')
    parser.add_argument('metadata_file', type=argparse.FileType('r'))
    args = parser.parse_args()
    render_tracks(args.assembly, args.metadata_file)


if __name__ == '__main__':
    main()
