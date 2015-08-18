.PHONY: check-env
TMPDIR=./tmp

all: check-env $(TMPDIR)/combined-hg19.bed $(TMPDIR)/combined-hg38.bed $(TMPDIR)/combined-hg19.bw

# Step 1 - combine the per-chrom bed files in the data directory and remove the label column
$(TMPDIR)/combined-hg19.bed:
	scripts/combine_bed_and_sort.sh $(DATA_DIR)/*.bed | scripts/remove_label_column.sh > $(TMPDIR)/combined-hg19.bed

# Step 2 - generate an hg38-compatible version using liftOver
$(TMPDIR)/combined-hg38.bed:
	liftOver $(TMPDIR)/combined-hg19.bed hg19ToHg38.over.chain.gz $(TMPDIR)/combined-hg38.bed $(TMPDIR)/unmapped.bed

# Step 3 - Convert to bigWig
hg19.sizes:
	fetchChromSizes hg19 > hg19.sizes

$(TMPDIR)/combined-hg19.bw: hg19.sizes
	bedGraphToBigWig $(TMPDIR)/combined-hg19.bed hg19.sizes $(TMPDIR)/combined-hg19.bw

check-env:
  ifndef DATA_DIR
	  $(error DATA_DIR is undefined)
  endif
