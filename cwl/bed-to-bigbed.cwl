#!/usr/bin/env cwl-runner

class: CommandLineTool
inputs:
  - id: "#input_file"
    type: File
    inputBinding:
      position: 1
  - id: "#chrom_sizes_file"
    type: File
    inputBinding:
      position: 2
  - id: "#output_file_name"
    type: string
    default: ''
    inputBinding:
      position: 3
outputs:
  - id: "#output_file"
    type: File
    outputBinding:
        glob: $(inputs.output_file_name)

baseCommand: bedToBigBed
