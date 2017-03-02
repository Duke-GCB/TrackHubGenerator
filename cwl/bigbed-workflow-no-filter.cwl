#!/usr/bin/env cwl-runner

class: Workflow
inputs:
  - id: "#input_files"
    type:
      type: array
      items: File
  - id: "#assembly"
    type: string
  - id: "#intermediate_output_file_name"
    type: string
    default: 'combined-intermediate.bed'
  - id: "#output_bigbed_file_name"
    type: string

outputs:
  - id: "#output_file"
    type: File
    source: "#bed_to_bigbed.output_file"

steps:
  - id: "#combine"
    run: { import: combine-bed.cwl }
    inputs:
    - { id: "#combine.input_files", source: "#input_files" }
    - { id: "#combine.output_file_name", source: "#intermediate_output_file_name" }
    outputs:
    - { id: "#combine.output_file" }
  - id: "#sort"
    run: { import: sort-bed.cwl }
    inputs:
    - { id: "#sort.input_file", source: "#combine.output_file" }
    outputs:
    - { id: "#sort.output_file" }
  - id: "change_precision"
    run: { import: change-precision.cwl }
    inputs:
    - { id: "#change_precision.input_file", source: "#sort.output_file" }
    outputs:
    - { id: "#change_precision.output_file" }
  - id: "#add_score_column"
    run: { import: add-score-column.cwl }
    inputs:
    - { id: "#add_score_column.input_file", source: "#change_precision.output_file" }
    outputs:
    - { id: "#add_score_column.output_file" }
  - id: "#fetch_chrom_sizes"
    run: { import: fetch-chrom-sizes.cwl }
    inputs:
    - { id: "#fetch_chrom_sizes.assembly", source: "#assembly" }
    outputs:
    - { id: "#fetch_chrom_sizes.output_file" }
  - id: "#bed_to_bigbed"
    run: { import: bed-to-bigbed.cwl }
    inputs:
    - { id: "#bed_to_bigbed.input_file", source: "#add_score_column.output_file" }
    - { id: "#bed_to_bigbed.chrom_sizes_file", source: "#fetch_chrom_sizes.output_file" }
    - { id: "#bed_to_bigbed.output_file_name", source: "#output_bigbed_file_name" }
    outputs:
    - { id: "#bed_to_bigbed.output_file" }

