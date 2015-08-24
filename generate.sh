#!/bin/bash

# Render hub
python python/render/render.py yaml/hub/hub.yaml hub

# Render genomes
python python/render/render.py yaml/genomes/genomes.yaml genomes

# Render trackDbs
python python/render/render_tracks.py --prefixes E2F1 --genome hg19 --variants 1w maxprob
python python/render/render_tracks.py --prefixes E2F1 --genome hg38 --variants 1w maxprob
