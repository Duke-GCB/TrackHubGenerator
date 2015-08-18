.PHONY: check-env
TMPDIR=./tmp

all: check-env $(TMPDIR)/combined-hg19.bed $(TMPDIR)/combined-hg38.bed

$(TMPDIR)/combined-hg19.bed:
	scripts/combine_bed_and_sort.sh $(DATA_DIR)/*.bed > $(TMPDIR)/combined-hg19.bed

$(TMPDIR)/combined-hg38.bed:
	liftOver $(TMPDIR)/combined-hg19.bed hg19ToHg38.over.chain.gz $(TMPDIR)/combined-hg38.bed $(TMPDIR)/unmapped.bed

check-env:
  ifndef DATA_DIR
	  $(error DATA_DIR is undefined)
  endif
