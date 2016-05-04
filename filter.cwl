#!/usr/bin/env cwl-runner

class: CommandLineTool
inputs:
  - id: "#input_file"
    type: File
    inputBinding:
      position: 1
  - id: "#threshold"
    type: float
    inputBinding:
      position: 2

outputs:
  - id: "#output_file"
    type: File
    outputBinding:
      glob: $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.filtered')

baseCommand: filter.py
stdout:  $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.filtered.bed')
