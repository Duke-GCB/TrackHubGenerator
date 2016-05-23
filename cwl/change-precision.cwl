#!/usr/bin/env cwl-runner

class: CommandLineTool
inputs:
  - id: "#input_file"
    type: File
    inputBinding:
      position: 1
  - id: "#precision"
    type: int
    default: 4
    inputBinding:
      position: 2

outputs:
  - id: "#output_file"
    type: File
    outputBinding:
      glob: $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.rounded.bed')

baseCommand: change_precision.py
stdout:  $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.rounded.bed')
