import glob
import argparse
from bins_from_bedfile import bins_from_bed, format_for_imads_config
import yaml
import os
import subprocess

BIGBED_TO_BED_BIN='/Users/dcl9/bin/bigBedToBed'

def make_bedfile_name(bigbed_filename):
    return bigbed_filename.replace('.bb','.bed')

def main(bigbeds_dir):
    results = list()
    bigbed_filenames = glob.glob(os.path.join(bigbeds_dir, '*.bb'))
    for bigbed in bigbed_filenames:
        # convert to bed in /tmp
        bed = make_bedfile_name(bigbed)
        subprocess.call([BIGBED_TO_BED_BIN, bigbed, bed])
        pos_bins, neg_bins = bins_from_bed(bed, 9, 9)
        result = format_for_imads_config(os.path.basename(bed), pos_bins, neg_bins)
        results.append(result)
        # delete the file
        os.remove(bed)
    print yaml.dump(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bigbeds_dir', help='directory of bigbed files')
    args = parser.parse_args()
    main(args.bigbeds_dir)
