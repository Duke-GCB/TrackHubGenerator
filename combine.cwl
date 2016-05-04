#!/usr/bin/env cwl-runner

class: CommandLineTool
inputs:
  - id: "#input_files"
    type:
      type: array
      items: File
    inputBinding:
      position: 1
  - id: "#output_file_name"
    type: string
outputs:
  - id: "#output_file"
    type: File
    outputBinding:
      glob: $(inputs.output_file_name)

baseCommand: combine_bed.sh
stdout:  $(inputs.output_file_name)
