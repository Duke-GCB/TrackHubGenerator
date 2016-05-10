# Makefile for generating track hub directory
# Requires setting BIGBEDS to a directory of .bb files with hg19/hg38 somewhere in the filename

HUBROOT=./hubroot
YAMLROOT=./yaml
PYTHON=python

.PHONY: hubroot

all: hubroot hub genomes tracks bigbeds

hubroot:
	mkdir -p $(HUBROOT)
	mkdir -p $(HUBROOT)/hg19
	mkdir -p $(HUBROOT)/hg38

hub: hubroot $(HUBROOT)/hub.txt
genomes: hubroot $(HUBROOT)/genomes.txt
tracks: hubroot $(HUBROOT)/hg19/trackDb.txt $(HUBROOT)/hg38/trackDb.txt

# Writing explicit rules here since make < 3.81 can't figure out which to use

$(HUBROOT)/hub.txt:
	$(PYTHON) python/render/render.py $(YAMLROOT)/hub/hub.yaml hub > $@

$(HUBROOT)/genomes.txt:
	$(PYTHON) python/render/render.py $(YAMLROOT)/genomes/genomes.yaml genomes > $@

$(HUBROOT)/%/trackDb.txt:
	$(PYTHON) python/render/render_tracks.py --assembly $* $(YAMLROOT)/tracks/tracks.yaml > $@

bigbeds:
	cp $(BIGBEDS)/*hg19*.bb $(HUBROOT)/hg19
	cp $(BIGBEDS)/*hg38*.bb $(HUBROOT)/hg38

clean:
	rm -rf $(HUBROOT)
