# Makefile for generating bigwig tracks from directories of bedfiles

TMPDIR=./tmp
OUTDIR=./out

all: tempdir outdir bigwigs

bigwigs: $(OUTDIR)/$(FILE_PREFIX)-hg19-combined-1w-sorted.bw $(OUTDIR)/$(FILE_PREFIX)-hg38-combined-1w-sorted.bw

tempdir:
	mkdir -p $(TMPDIR)

outdir:
	mkdir -p $(OUTDIR)

# 1 - combine the per-chrom bed files in the data directory and remove the label column
$(TMPDIR)/$(FILE_PREFIX)-hg19-combined.bed:
	scripts/combine_bed.sh $(BEDFILES_DIR)/*.bed | scripts/remove_label_column.sh > $@

# 2 - process to single-base width
$(TMPDIR)/$(FILE_PREFIX)-hg19-combined-1w.bed: $(TMPDIR)/$(FILE_PREFIX)-hg19-combined.bed
	python python/bedgraph_utils/slice.py $< > $@

# 3 - generate an hg38-compatible version using liftOver
# 3.1 download chain
$(TMPDIR)/hg19ToHg38.over.chain.gz:
	curl -sLo $@ http://hgdownload.cse.ucsc.edu/gbdb/hg19/liftOver/hg19ToHg38.over.chain.gz

# 3.2 liftOver
$(TMPDIR)/$(FILE_PREFIX)-hg38-combined-1w.bed: $(TMPDIR)/$(FILE_PREFIX)-hg19-combined-1w.bed $(TMPDIR)/hg19ToHg38.over.chain.gz
	liftOver $^ $@ $(TMPDIR)/$(FILE_PREFIX)-unmapped.bed

# 4 - sort and uniq the files. Liftover may change the order, so we sort after liftover
$(TMPDIR)/$(FILE_PREFIX)-%-combined-1w-sorted.bed: $(TMPDIR)/$(FILE_PREFIX)-%-combined-1w.bed
	scripts/sort_uniq_bed.sh $< > $@

# 5 - Convert to bigWig
# 5.1 chrom sizes
$(TMPDIR)/%.sizes:
	fetchChromSizes $* > $@

# 5.2 bigwig
$(OUTDIR)/$(FILE_PREFIX)-%-combined-1w-sorted.bw: $(TMPDIR)/$(FILE_PREFIX)-%-combined-1w-sorted.bed $(TMPDIR)/%.sizes
	bedGraphToBigWig $^ $@

ifndef BEDFILES_DIR
$(error BEDFILES_DIR is undefined)
endif
ifndef FILE_PREFIX
$(error FILE_PREFIX is undefined)
endif

clean:
	rm -rf $(TMPDIR)
