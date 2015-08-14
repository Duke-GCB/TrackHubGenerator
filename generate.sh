#!/bin/bash

# Render hub
python python/render/render.py yaml/hub/hub.yaml hub

# Render genomes
python python/render/render.py yaml/genomes/genomes.yaml genomes

# Render trackDbs
python python/render/render.py yaml/tracks/trackDb.yaml trackDb #hg19
python python/render/render.py yaml/tracks/trackDb.yaml trackDb #hg38
