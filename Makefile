# Makefile for generating bigwig tracks from directories of bedfiles

.PHONY: check-env
TMPDIR=./tmp

all: check-env tempdir $(TMPDIR)/hg19-combined-1w-sorted.bw $(TMPDIR)/hg38-combined-1w-sorted.bw

tempdir:
	mkdir -p $(TMPDIR)

# 1 - combine the per-chrom bed files in the data directory and remove the label column
$(TMPDIR)/hg19-combined.bed:
	scripts/combine_bed.sh $(DATA_DIR)/*.bed | scripts/remove_label_column.sh > $@

# 2 - process to single-base width
$(TMPDIR)/hg19-combined-1w.bed: $(TMPDIR)/hg19-combined.bed
	python python/bedgraph_utils/slice.py $< > $@

# 3 - generate an hg38-compatible version using liftOver
# 3.1 download chain
$(TMPDIR)/hg19ToHg38.over.chain.gz:
	curl -sLo $(TMPDIR)/hg19ToHg38.over.chain.gz http://hgdownload.cse.ucsc.edu/gbdb/hg19/liftOver/hg19ToHg38.over.chain.gz

# 3.2 liftOver
$(TMPDIR)/hg38-combined-1w.bed: $(TMPDIR)/hg19-combined-1w.bed $(TMPDIR)/hg19ToHg38.over.chain.gz
	liftOver $^ $@ $(TMPDIR)/unmapped.bed

# 4 - sort and uniq the files. Liftover may change the order, so we sort after liftover
$(TMPDIR)/%-combined-1w-sorted.bed: $(TMPDIR)/%-combined-1w.bed
	scripts/sort_uniq_bed.sh $< > $@

# 5 - Convert to bigWig
# 5.1 chrom sizes
$(TMPDIR)/%.sizes:
	fetchChromSizes $* > $@

# 5.2 bigwig
$(TMPDIR)/%-combined-1w-sorted.bw: $(TMPDIR)/%-combined-1w-sorted.bed $(TMPDIR)/%.sizes
	bedGraphToBigWig $^ $@

check-env:
  ifndef DATA_DIR
	  $(error DATA_DIR is undefined)
  endif

clean:
	rm -rf $(TMPDIR)
