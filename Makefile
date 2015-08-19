.PHONY: check-env
TMPDIR=./tmp

all: check-env tempdir $(TMPDIR)/combined-hg19.bw $(TMPDIR)/combined-hg38.bw

tempdir:
	mkdir -p $(TMPDIR)

# Step 1 - combine the per-chrom bed files in the data directory and remove the label column
$(TMPDIR)/combined-hg19.bed:
	scripts/combine_bed_and_sort.sh $(DATA_DIR)/*.bed | scripts/remove_label_column.sh > $(TMPDIR)/combined-hg19.bed

# Step 2 - generate an hg38-compatible version using liftOver
# TODO: download the chain if needed
$(TMPDIR)/combined-hg38.bed: $(TMPDIR)/combined-hg19.bed
	liftOver $(TMPDIR)/combined-hg19.bed hg19ToHg38.over.chain.gz $(TMPDIR)/combined-hg38-liftover.bed $(TMPDIR)/unmapped.bed
	scripts/combine_bed_and_sort.sh $(TMPDIR)/combined-hg38-liftover.bed > $(TMPDIR)/combined-hg38.bed

# Step 3 - process to single width, hopefully avoiding overlapping regions
$(TMPDIR)/combined-hg19-1w.bed:  $(TMPDIR)/combined-hg19.bed
	python python/bedgraph_utils/slice.py $(TMPDIR)/combined-hg19.bed > $(TMPDIR)/combined-hg19-1w.bed

$(TMPDIR)/combined-hg38-1w.bed: $(TMPDIR)/combined-hg38.bed
	python python/bedgraph_utils/slice.py $(TMPDIR)/combined-hg38.bed > $(TMPDIR)/combined-hg38-1w.bed
# Step 4 - Convert to bigWig
$(TMPDIR)/hg19.sizes:
	fetchChromSizes hg19 > $(TMPDIR)/hg19.sizes

$(TMPDIR)/hg38.sizes:
	fetchChromSizes hg38 > $(TMPDIR)/hg38.sizes

$(TMPDIR)/combined-hg19.bw: $(TMPDIR)/hg19.sizes $(TMPDIR)/combined-hg19-1w.bed
	bedGraphToBigWig $(TMPDIR)/combined-hg19-1w.bed $(TMPDIR)/hg19.sizes $(TMPDIR)/combined-hg19.bw

# the liftover-converted file has overlapping regions
$(TMPDIR)/combined-hg38.bw: $(TMPDIR)/hg38.sizes $(TMPDIR)/combined-hg38-1w.bed
	bedGraphToBigWig $(TMPDIR)/combined-hg38-1w.bed $(TMPDIR)/hg38.sizes $(TMPDIR)/combined-hg38.bw

check-env:
  ifndef DATA_DIR
	  $(error DATA_DIR is undefined)
  endif

clean:
	rm -rf $(TMPDIR)
