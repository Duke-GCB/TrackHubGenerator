# Makefile for generating bigwig tracks from directories of bedfiles

TMPDIR=./tmp
OUTDIR=./out

all: tempdir outdir bigwigs

bigwigs: $(OUTDIR)/$(PROTEIN_NAME)-hg19-combined-1w-sorted.bw $(OUTDIR)/$(PROTEIN_NAME)-hg38-combined-1w-sorted.bw

tempdir:
	mkdir -p $(TMPDIR)

outdir:
	mkdir -p $(OUTDIR)

# 1 - combine the per-chrom bed files in the data directory and remove the label column
$(TMPDIR)/$(PROTEIN_NAME)-hg19-combined.bed:
	scripts/combine_bed.sh $(DATA_DIR)/*.bed | scripts/remove_label_column.sh > $@

# 2 - process to single-base width
$(TMPDIR)/$(PROTEIN_NAME)-hg19-combined-1w.bed: $(TMPDIR)/$(PROTEIN_NAME)-hg19-combined.bed
	python python/bedgraph_utils/slice.py $< > $@

# 3 - generate an hg38-compatible version using liftOver
# 3.1 download chain
$(TMPDIR)/hg19ToHg38.over.chain.gz:
	curl -sLo $@ http://hgdownload.cse.ucsc.edu/gbdb/hg19/liftOver/hg19ToHg38.over.chain.gz

# 3.2 liftOver
$(TMPDIR)/$(PROTEIN_NAME)-hg38-combined-1w.bed: $(TMPDIR)/$(PROTEIN_NAME)-hg19-combined-1w.bed $(TMPDIR)/hg19ToHg38.over.chain.gz
	liftOver $^ $@ $(TMPDIR)/$(PROTEIN_NAME)-unmapped.bed

# 4 - sort and uniq the files. Liftover may change the order, so we sort after liftover
$(TMPDIR)/$(PROTEIN_NAME)-%-combined-1w-sorted.bed: $(TMPDIR)/$(PROTEIN_NAME)-%-combined-1w.bed
	scripts/sort_uniq_bed.sh $< > $@

# 5 - Convert to bigWig
# 5.1 chrom sizes
$(TMPDIR)/%.sizes:
	fetchChromSizes $* > $@

# 5.2 bigwig
$(OUTDIR)/$(PROTEIN_NAME)-%-combined-1w-sorted.bw: $(TMPDIR)/$(PROTEIN_NAME)-%-combined-1w-sorted.bed $(TMPDIR)/%.sizes
	bedGraphToBigWig $^ $@

ifndef DATA_DIR
$(error DATA_DIR is undefined)
endif
ifndef PROTEIN_NAME
$(error PROTEIN_NAME is undefined)
endif

clean:
	rm -rf $(TMPDIR)
