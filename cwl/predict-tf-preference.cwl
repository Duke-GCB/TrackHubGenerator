#!/usr/bin/env cwl-runner
class: CommandLineTool
inputs:
  - id: "#tf1"
    type: string
    inputBinding:
      position: 1
  - id: "#tf2"
    type: string
    inputBinding:
      position: 2
  - id: "#tf1_bed_file"
    type: File
    inputBinding:
      position: 3
  - id: "#tf2_bed_file"
    type: File
    inputBinding:
      position: 4
  - id: "#output_bed_file_name"
    type: string
    default: "preferences.bed"
    inputBinding:
      position: 5

outputs:
  - id: "#output_file"
    type: File
    outputBinding:
      glob: $(inputs.output_bed_file_name)

baseCommand: predict-tf-preference.R
