#!/usr/bin/env cwl-runner

class: CommandLineTool
inputs:
  - id: "#assembly"
    type: string
    inputBinding:
      position: 1

outputs:
  - id: "#output_file"
    type: File
    outputBinding:
      glob: $(inputs.assembly + '.chrom.sizes')

baseCommand: fetchChromSizes
stdout: $(inputs.assembly + '.chrom.sizes')
