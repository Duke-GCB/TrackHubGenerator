# bin_from_bedscore
import pandas
import argparse
import os
import yaml

def bins_from_bed(bedfile, n_posbins, n_negbins):
    data = pandas.read_table(bedfile, delimiter='\t', header=None)
    score_column = 3
    pos_scores = data[data[score_column] > 0][3]
    neg_scores = data[data[score_column] < 0][3]
    pos_bins = pandas.qcut(pos_scores, n_posbins, retbins=True)[1]
    neg_bins = pandas.qcut(neg_scores, n_negbins, retbins=True)[1]
    return pos_bins.tolist(), neg_bins.tolist()

def format_for_imads_config(filename, pos_bins, neg_bins):
    # hg19_E2f1_0007_vs_E2f3_0008.bed
    genome = filename.split('_')[0]
    name = os.path.splitext(filename[len(genome) + 1:])[0]
    preference_bins = {'pos': pos_bins, 'neg': neg_bins}
    result = dict(genome=genome, name=name, preference_bins=preference_bins)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Output quantile distribution bins for scores in a bed file')
    parser.add_argument('inputfile', type=argparse.FileType('r'), help='Input tab-delimited bed file with score in col 3')
    parser.add_argument('--n_posbins', type=int, default=9, help='Number of bins on positive side (default 9)')
    parser.add_argument('--n_negbins', type=int, default=9, help='Number of bins on negative side (default 9)')
    parser.add_argument('--yaml', type=bool, default=True, help='output format, default yaml')
    args = parser.parse_args()
    pos_bins, neg_bins = bins_from_bed(args.inputfile, args.n_posbins, args.n_negbins)
    if args.yaml:
        filename = args.inputfile.name
        result = format_for_imads_config(os.path.basename(filename), pos_bins, neg_bins)
        result = yaml.dump(result)
    print result