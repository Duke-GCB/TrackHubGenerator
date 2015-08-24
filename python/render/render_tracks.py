__author__ = 'dcl9'
from render import render_template
import argparse


def generate_track_dict(prefix, variant, genome):
    track_dict = {'track_name': '{}_SVR-scores_{}'.format(prefix, variant),
                  'bigwig_url': '{}-{}-{}.bw'.format(prefix, genome, variant),
                  'short_label': '{}-{}-{}'.format(prefix, genome, variant),
                  'long_label': '{}_SVR-scores_{}'.format(prefix, variant)}
    return track_dict


def render_track_variants(genome, prefixes, variants):
    tracks = []
    for prefix in prefixes:
        for variant in variants:
            tracks.append(generate_track_dict(prefix, variant, genome))
    trackdb = {'tracks': tracks}
    render_template(trackdb, 'trackDb')


def main():
    parser = argparse.ArgumentParser(description='Render trackDb.txt')
    parser.add_argument('--prefixes', nargs='+')
    parser.add_argument('--genome')
    parser.add_argument('--variants', nargs='+')
    args = parser.parse_args()
    render_track_variants(args.genome, args.prefixes, args.variants)


if __name__ == '__main__':
    main()
