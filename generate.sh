#!/bin/bash

# Render hub
python render/render.py yaml/hub/hub.yaml hub

# Render genomes
python render/render.py yaml/genomes/genomes.yaml genomes

# Render trackDbs
python render/render.py yaml/tracks/hg19.yaml trackDb
python render/render.py yaml/tracks/hg38.yaml trackDb
