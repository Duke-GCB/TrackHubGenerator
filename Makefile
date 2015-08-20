.PHONY: check-env
TMPDIR=./tmp

all: check-env tempdir $(TMPDIR)/combined-hg19-1w-sorted.bw $(TMPDIR)/combined-hg38-1w-sorted.bw

tempdir:
	mkdir -p $(TMPDIR)

# 1 - combine the per-chrom bed files in the data directory and remove the label column
$(TMPDIR)/combined-hg19.bed:
	scripts/combine_bed.sh $(DATA_DIR)/*.bed | scripts/remove_label_column.sh > $(TMPDIR)/combined-hg19.bed

# 2 - process to single-base width
$(TMPDIR)/combined-hg19-1w.bed: $(TMPDIR)/combined-hg19.bed
	python python/bedgraph_utils/slice.py $(TMPDIR)/combined-hg19.bed > $(TMPDIR)/combined-hg19-1w.bed

# 3 - generate an hg38-compatible version using liftOver
# TODO: download the chain if needed
$(TMPDIR)/combined-hg38-1w.bed: $(TMPDIR)/combined-hg19-1w.bed
	liftOver $(TMPDIR)/combined-hg19-1w.bed hg19ToHg38.over.chain.gz $(TMPDIR)/combined-hg38-1w.bed $(TMPDIR)/unmapped.bed

# 4 - sort and uniq the files. Liftover may change the order, so we sort after liftover
# 4.1 hg19
$(TMPDIR)/combined-hg19-1w-sorted.bed: $(TMPDIR)/combined-hg19-1w.bed
	scripts/sort_uniq_bed.sh $(TMPDIR)/combined-hg19-1w.bed > $(TMPDIR)/combined-hg19-1w-sorted.bed

# 4.2 hg38
$(TMPDIR)/combined-hg38-1w-sorted.bed: $(TMPDIR)/combined-hg38-1w.bed
	scripts/sort_uniq_bed.sh $(TMPDIR)/combined-hg38-1w.bed > $(TMPDIR)/combined-hg38-1w-sorted.bed

# 5 - Convert to bigWig
# 5.1 hg19 chrom sizes
$(TMPDIR)/hg19.sizes:
	fetchChromSizes hg19 > $(TMPDIR)/hg19.sizes

# 5.2 hg19 bigwig
$(TMPDIR)/combined-hg19-1w-sorted.bw: $(TMPDIR)/hg19.sizes $(TMPDIR)/combined-hg19-1w-sorted.bed
	bedGraphToBigWig $(TMPDIR)/combined-hg19-1w-sorted.bed $(TMPDIR)/hg19.sizes $(TMPDIR)/combined-hg19-1w-sorted.bw

# 5.1 hg38 chrom sizes
$(TMPDIR)/hg38.sizes:
	fetchChromSizes hg38 > $(TMPDIR)/hg38.sizes

# 5.2 hg38 bigwig
$(TMPDIR)/combined-hg38-1w-sorted.bw: $(TMPDIR)/hg38.sizes $(TMPDIR)/combined-hg38-1w-sorted.bed
	bedGraphToBigWig $(TMPDIR)/combined-hg38-1w-sorted.bed $(TMPDIR)/hg38.sizes $(TMPDIR)/combined-hg38-1w-sorted.bw

check-env:
  ifndef DATA_DIR
	  $(error DATA_DIR is undefined)
  endif

clean:
	rm -rf $(TMPDIR)
