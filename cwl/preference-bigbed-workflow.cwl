#!/usr/bin/env cwl-runner
requirements:
- class: ScatterFeatureRequirement

class: Workflow
inputs:
  - id: "#tf1"
    type: string
  - id: "#tf1_bed_files"
    type:
      type: array
      items: File
  - id: "#tf1_threshold"
    type: float
  - id: "#tf2"
    type: string
  - id: "#tf2_threshold"
    type: float
  - id: "#tf2_bed_files"
    type:
      type: array
      items: File
  - id: "#intermediate_output_file_name"
    type: string
    default: 'combined-intermediate.bed'
#   - id: "#output_bigbed_file_name"
#     type: string

outputs:
  - id: "#preferences_output_file"
    type:
      type: array
      items: File
    source: "#preferences.output_bed_file"
  - id: "#thresholded_output_file"
    type:
      type: array
      items: File
    source: "#threshold.output_bed_file"

steps:
  - id: "#preferences"
    run: { import: predict-tf-preference.cwl }
    scatter:
      - "#preferences.tf1_bed_file"
      - "#preferences.tf2_bed_file"
    scatterMethod: dotproduct
    inputs:
    - { id: "#preferences.tf1", source: "#tf1" }
    - { id: "#preferences.tf2", source: "#tf2" }
    - { id: "#preferences.tf1_bed_file", source: "#tf1_bed_files" }
    - { id: "#preferences.tf2_bed_file", source: "#tf2_bed_files" }
    - { id: "#preferences.output_bed_file_name", source: "#intermediate_output_file_name" }
    outputs:
    - { id: "#preferences.output_bed_file" }
  - id: "#threshold"
    run: { import: filter-tf-preference-threshold.cwl }
    scatter:
      - "#threshold.tf1_bed_file"
      - "#threshold.tf2_bed_file"
      - "#threshold.prefs_bed_file"
    scatterMethod: dotproduct
    inputs:
    - { id: "#threshold.tf1_bed_file", source: "#tf1_bed_files" }
    - { id: "#threshold.tf2_bed_file", source: "#tf2_bed_files" }
    - { id: "#threshold.prefs_bed_file", source: "#preferences.output_bed_file" }
    - { id: "#threshold.tf1_threshold", source: "#tf1_threshold" }
    - { id: "#threshold.tf2_threshold", source: "#tf2_threshold" }
    - { id: "#threshold.output_bed_file_name", source: "#intermediate_output_file_name" }
    outputs:
    - { id: "#threshold.output_bed_file" }
