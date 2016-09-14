#!/usr/bin/env cwl-runner
class: CommandLineTool
inputs:
  - id: "#tf1_bed_file"
    type: File
    inputBinding:
      position: 1
  - id: "#tf2_bed_file"
    type: File
    inputBinding:
      position: 2
  - id: "#prefs_bed_file"
    type: File
    inputBinding:
      position: 3
  - id: "#tf1_threshold"
    type: float
    inputBinding:
      position: 4
  - id: "#tf2_threshold"
    type: float
    inputBinding:
      position: 5
  - id: "#output_bed_file_name"
    type: string
    default: "preferences.bed"

outputs:
  - id: "#output_bed_file"
    type: File
    outputBinding:
      glob: $(inputs.output_bed_file_name)

stdout:  $(inputs.output_bed_file_name)

baseCommand: ['filter-preference-threshold.py','--spaces']
