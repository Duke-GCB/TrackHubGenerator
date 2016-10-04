__author__ = 'dcl9'
from render import render_template
import argparse
import yaml

def generate_preferences_track_dict(metadata):
    d = dict()
    d['track_name'] = metadata['track_name']
    d['bigbed_url'] = metadata['track_filename']
    d['short_label'] = '{} vs. {}'.format(metadata['proteins'][0], metadata['proteins'][1])
    d['long_label'] = 'Binding site preferences of {}(Red) vs. {}(Blue); iMADS models {} and {}'.format(
      metadata['proteins'][0], metadata['proteins'][1], metadata['serial_numbers'][0], metadata['serial_numbers'][1]
    )
    d['type'] = 'bigBed 9 .'
    d['spectrum'] = 'off'
    d['itemRgb'] = 'on'
    return d

def generate_predictions_track_dict(metadata):
    d = dict()
    d['track_name'] = metadata['track_name']
    d['bigbed_url'] = metadata['track_filename']
    d['short_label'] = metadata['protein']
    d['long_label'] = 'Predicted {} binding sites (site width = {}); iMADS model {}'.format(metadata['protein'], metadata['width'], metadata['serial_number'])
    d['type'] = 'bigBed 5 .'
    d['spectrum'] = 'on'
    d['itemRgb'] = 'off'
    return d

def render_tracks(assembly, mode, metadata_file):
    obj = yaml.load(metadata_file)
    # Just pull out the assembly ones
    if mode == 'preferences':
      generate_track_dict = generate_preferences_track_dict
    else:
      generate_track_dict = generate_predictions_track_dict
    tracks = [generate_track_dict(x) for x in obj if x['assembly'] == assembly]
    trackdb = {'tracks': tracks}
    render_template(trackdb, 'trackDb')


def main():
    parser = argparse.ArgumentParser(description='Render trackDb.txt')
    parser.add_argument('--assembly')
    parser.add_argument('--mode')
    parser.add_argument('metadata_file', type=argparse.FileType('r'))
    args = parser.parse_args()
    render_tracks(args.assembly, args.mode, args.metadata_file)


if __name__ == '__main__':
    main()
