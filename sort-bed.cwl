#!/usr/bin/env cwl-runner

class: CommandLineTool
inputs:
  - id: "#input_file"
    type: File
    inputBinding:
      position: 1
outputs:
  - id: "#output_file"
    type: File
    outputBinding:
      glob: $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.sorted.bed')

baseCommand: sort_bed.sh
stdout:  $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.sorted.bed')
