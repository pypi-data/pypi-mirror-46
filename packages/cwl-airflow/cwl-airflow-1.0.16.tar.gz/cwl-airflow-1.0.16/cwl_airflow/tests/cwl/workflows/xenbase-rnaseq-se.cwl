cwlVersion: v1.0
class: Workflow


requirements:
  - class: SubworkflowFeatureRequirement
  - class: StepInputExpressionRequirement
  - class: MultipleInputFeatureRequirement
  - class: InlineJavascriptRequirement
    expressionLib:
    - var default_output_name = function(named_input, ext, segment) {
          ext = ext || "";
          segment = segment || 1;
          if (Array.isArray(named_input) && named_input.length > 0){
            return named_input[0].location.split('/').slice(-1)[0].split('.').slice(0,segment).join('.')+ext;
          } else {
            return named_input.location.split('/').slice(-1)[0].split('.').slice(0,segment).join('.')+ext;
          }
      };


inputs:

  fastq_file:
    type: File
    label: "FASTQ input file"
    format: "http://edamontology.org/format_1930"
    doc: "Reads data in a FASTQ format"

  fasta_file_adapters:
    type: File
    label: "Adapters FASTA file"
    format: "http://edamontology.org/format_1929"
    doc: "Adapters FASTA file to be used by Trimmomatic"

  rsem_indices_folder:
    type: Directory
    label: "RSEM indices folder"
    doc: "Path to RSEM indices generated with BowTie2"

  bowtie_indices_folder:
    type: Directory
    label: "BowTie Ribosomal Indices"
    doc: "Path to Bowtie generated indices for ribosomal FASTA"

  threads:
    type: int?
    default: 2
    label: "Number of threads"
    doc: "Number of threads for those steps that support multithreading"


outputs:

  rsem_isoforms_file:
    type: File
    format: "http://edamontology.org/format_3475"
    label: "RSEM isoforms expression file"
    doc: "RSEM isoforms expression file"
    outputSource: rename_rsem_isoforms_file/target_file

  biowardrobe_isoforms_file:
    type: File
    format: "http://edamontology.org/format_3752"
    label: "Biowardrobe compatible isoforms expression file"
    doc: "Biowardrobe compatible isoforms expression file"
    outputSource: make_biowardrobe_isoforms/biowardrobe_isoforms_file

  rsem_genes_file:
    type: File
    format: "http://edamontology.org/format_3475"
    label: "RSEM genes expression file"
    doc: "RSEM genes expression file"
    outputSource: rename_rsem_genes_file/target_file

  bambai_pair:
    type: File
    format: "http://edamontology.org/format_2572"
    label: "Coordinate sorted BAM alignment file (+index BAI)"
    doc: "Coordinate sorted BAM file and BAI index file"
    outputSource: rename_rsem_bambai_pair/target_file

  bigwig_file:
    type: File
    format: "http://edamontology.org/format_3006"
    label: "BigWig file"
    doc: "Generated BigWig file"
    outputSource: bam_to_bigwig/bigwig_file

  fastx_statistics:
    type: File
    format: "http://edamontology.org/format_2330"
    label: "FASTQ statistics"
    doc: "fastx_quality_stats generated quality statistics file"
    outputSource: fastx_quality_stats/statistics_file

  get_stat_log:
    type: File
    label: "RSEM & Bowtie combined log"
    format: "http://edamontology.org/format_2330"
    doc: "Mapping statistics from RSEM & Bowtie logs"
    outputSource: get_stat/output_file

  rsem_stat_folder:
    type: Directory
    label: "RSEM alignment statistics"
    doc: "RSEM generated statistics folder. Mostly for debug purposes"
    outputSource: rsem_calculate_expression/stat_folder

  bowtie_log:
    type: File
    format: "http://edamontology.org/format_2330"
    label: "Ribo Bowtie alignment log"
    doc: "Ribo Bowtie alignment log file. Mostly for debug purposes"
    outputSource: ribo_bowtie_aligner/log_file


steps:

  extract_fastq:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/extract-fastq.cwl
    in:
      compressed_file: fastq_file
    out: [fastq_file]

  fastx_quality_stats:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/fastx-quality-stats.cwl
    in:
      input_file: extract_fastq/fastq_file
    out: [statistics_file]

  fastqc_stats:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/fastqc.cwl
    in:
      fastq_file: extract_fastq/fastq_file
    out: [summary_file]

  fastqc_results_trigger:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/fastqc-results-trigger.cwl
    in:
      summary_file: fastqc_stats/summary_file
    out: [trigger]

  trim_adapters:
    hints:
      ResourceRequirement:
        coresMin: 2
        ramMin: 2048  
    run: ../tools/trimmomatic.cwl
    in:
      fastq_file_upstream: extract_fastq/fastq_file
      adapters_file: fasta_file_adapters
      trigger: fastqc_results_trigger/trigger
      lib_type:
        default: "SE"
      illuminaclip_step_param:
        default: '2:30:15'
      threads: threads
    out: [upstream_trimmed_file]

  rsem_calculate_expression:
    hints:
      ResourceRequirement:
        coresMin: 2
        ramMin: 2048  
    run: ../tools/rsem-calculate-expression.cwl
    in:
      upstream_read_file: trim_adapters/upstream_trimmed_file
      indices_folder: rsem_indices_folder
      bowtie2:
        default: true
      sort_bam_by_coordinate:
        default: true
      output_genome_bam:
        default: true
      threads: threads
    out:
      - isoform_results_file
      - gene_results_file
      - genome_sorted_bam_bai_pair
      - stat_folder
      - total_reads_number
      - mapped_reads_number
      - multimapped_reads_number

  rename_rsem_bambai_pair:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/rename.cwl
    in:
      source_file: rsem_calculate_expression/genome_sorted_bam_bai_pair
      target_filename:
        source: fastq_file
        valueFrom: $(default_output_name(self, ".bam"))
    out: [target_file]

  rename_rsem_isoforms_file:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/rename.cwl
    in:
      source_file: rsem_calculate_expression/isoform_results_file
      target_filename:
        source: fastq_file
        valueFrom: $(default_output_name(self, ".isoforms.tsv"))
    out: [target_file]

  rename_rsem_genes_file:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/rename.cwl
    in:
      source_file: rsem_calculate_expression/gene_results_file
      target_filename:
        source: fastq_file
        valueFrom: $(default_output_name(self, ".genes.tsv"))
    out: [target_file]

  get_chr_length_file:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/get-file-by-name.cwl
    in:
      input_files: rsem_indices_folder
      basename_regex:
        default: "chrlist$"
    out: [selected_file]

  bam_to_bigwig:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../subworkflows/bam-bedgraph-bigwig.cwl
    in:
      bam_file: rename_rsem_bambai_pair/target_file
      chrom_length_file: get_chr_length_file/selected_file
      mapped_reads_number: rsem_calculate_expression/mapped_reads_number
    out: [bigwig_file]

  ribo_bowtie_aligner:
    hints:
      ResourceRequirement:
        coresMin: 2
        ramMin: 2048  
    run: ../tools/bowtie-alignreads.cwl
    in:
      upstream_filelist: trim_adapters/upstream_trimmed_file
      indices_folder: bowtie_indices_folder
      output_filename:
        source: fastq_file
        valueFrom: $(default_output_name(self, ".txt"))
      v:
        default: 3
      best:
        default: true
      threads: threads
    out:
      - mapped_reads_number
      - log_file

  get_stat:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/custom-bash.cwl
    in:
      input_file: rsem_calculate_expression/isoform_results_file
      script:
        default: "echo -n $1 $2 $3 $4 `cat $0 | cut -f 5 | grep -v expected_count | awk '{sum+=$1} END {print int(sum)}'` > $5"
      param:
        source:
        - rsem_calculate_expression/total_reads_number
        - rsem_calculate_expression/mapped_reads_number
        - ribo_bowtie_aligner/mapped_reads_number
        - rsem_calculate_expression/multimapped_reads_number
        - fastq_file
        valueFrom: |
          ${
            self[4] = default_output_name(self[4], ".stat");
            return self.map(String);
          }
    out: [output_file]

  get_annotation_file:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/get-file-by-name.cwl
    in:
      input_files: rsem_indices_folder
      basename_regex:
        default: "ti$"
    out: [selected_file]

  make_biowardrobe_isoforms:
    hints:
      ResourceRequirement:
        coresMin: 1
        ramMin: 1024  
    run: ../tools/python-make-biowardrobe-isoforms.cwl
    in:
      rsem_isoforms_file: rename_rsem_isoforms_file/target_file
      rsem_annotation_file: get_annotation_file/selected_file
    out: [biowardrobe_isoforms_file]