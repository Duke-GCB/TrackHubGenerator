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
      glob: $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.with-score.bed')

baseCommand: add_score_column.py
stdout:  $(inputs.input_file.path.replace(/^.*[\\\/]/, '').replace(/\.[^/.]+$/, '') + '.with-score.bed')
