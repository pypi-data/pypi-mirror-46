
"""
Usage:
    dupliganger prep [options] <input.fastq>
    dupliganger prep [options] <in1.fastq> <in2.fastq>
    dupliganger prep [options] <input.bam>

Global Options:
    -h, --help
    -v, --verbose         Be verbose
    -k KIT, --kit KIT     The kit used [default: bioo].
    -o OUT_DIR            Place results in directory OUT_DIR.
    --compress            Compress (gzip) output files.
    -t N, --threads N     Number of threads to run with [default: 1].

Pipeline Options:
    --retain-intermediates      Do not delete intermediate files.
    --compress-intermediates    Compress intermediate files.
    --pipeline-names            Retain pipeline filenames.

remove-umi Options:
    --force-paired        Do not autodetect whether paired-end vs single-end,
                          instead force paired-end. Helpful fail safe if you
                          believe you have paired end data.

remove-adapter Options:
    -C S, --cutadapt S  Pass 'S' as arguments to Cutadapt. Don't forget to put quotes
                        around S if passing in more than one argument.
                        [default: '-n 3 -O 1 -m 30']
    -1 A, --adapter1    First (Illumina) adapter [default: GATCGGAAGAGCACACG]
    -2 A, --adapter2    Second (Illumina) adapter [default: AGATCGGAAGAGCGTCG]

qtrim Options:
    -T S, --trimmomatic S   Pass 'S' as arguments to Trimmomatic. Don't forget to put quotes
                            around S if passing in more than one argument.
                            [default: 'LEADING:10 TRAILING:10 SLIDINGWINDOW:5:10 MINLEN:30']
    -p P, --phred P         Set P to 33 for phred33 encoded files, or 64 for
                            phred 64 encoded FASTQ files [default: 33].

annotate-qtrim Options:
    -l TRIMLOG            Optionally specify trimlog.

-----

New Options Ideas:
    --restart       Restart the prep pipeline.
    --tmpdir        Temporary directory.


























































    dupliganger remove-umi [options] <input.bam>
Options:
    -h, --help
    -v, --verbose         Be verbose
    -k KIT, --kit KIT     The kit used [default: bioo].
    -o OUT_DIR            Place results in directory OUT_DIR.
    --compress            Compress (gzip) output files.
    --force-paired        Do not autodetect whether paired-end vs single-end,
                          instead force paired-end. Helpful fail safe if you
                          believe you have paired end data.
    -t N, --threads N     EXPERIMENTAL: If pigz is installed and --threads is
                          specified, output FASTQ files will be compressed with
                          pigz -p <n>; otherwise, they will be left
                          uncompressed (as it simply takes too long to compress
                          with just gzip).



    dupliganger remove-adapter [options] <in1.fastq> <in2.fastq>
Options:
    -C S, --cutadapt S  Pass 'S' as arguments to Cutadapt. Don't forget to put quotes
                        around S if passing in more than one argument.
                        [default: '-n 3 -O 1 -m 30']
    -1 A, --adapter1    First (Illumina) adapter [default: GATCGGAAGAGCACACG]
    -2 A, --adapter2    Second (Illumina) adapter [default: AGATCGGAAGAGCGTCG]



    dupliganger qtrim [options] <in1.fastq> <in2.fastq>
Options:
    -h, --help
    -v, --verbose           Be verbose.
    -o OUT_DIR              Place results in directory OUT_DIR.
    --compress              Compress (gzip) output files.
    -t N, --threads N       Number of threads to run with [default: 1].
    -T S, --trimmomatic S   Pass 'S' as arguments to Trimmomatic. Don't forget to put quotes
                            around S if passing in more than one argument.
                            [default: 'LEADING:10 TRAILING:10 SLIDINGWINDOW:5:10 MINLEN:30']
    -p P, --phred P         Set P to 33 for phred33 encoded files, or 64 for
                            phred 64 encoded FASTQ files [default: 33].





    dupliganger annotate-qtrim [options] <in1.fastq> <in2.fastq>
Options:
    -l TRIMLOG            Optionally specify trimlog.

"""



"""Annotates read names with UMIs and clips inline UMIs if needed.

Usage:
    dupliganger remove-umi [options] <input.fastq>
    dupliganger remove-umi [options] <in1.fastq> <in2.fastq>
    dupliganger remove-umi [options] <input.bam>


Note:
    Dupliganger supports (and autodetects) input FASTQ files that are gzipped.

Note:
    If passing a paired-end BAM file, it needs to be sorted by read name
    (if not sorted, dupliganger will exit out when it detects mismatching
    adjacent records).

Options:
    -h, --help
    -v, --verbose         Be verbose
    -k KIT, --kit KIT     The kit used [default: bioo].
    -o OUT_DIR            Place results in directory OUT_DIR.
    --compress            Compress (gzip) output files.
    --force-paired        Do not autodetect whether paired-end vs single-end,
                          instead force paired-end. Helpful fail safe if you
                          believe you have paired end data.
    -t N, --threads N     EXPERIMENTAL: If pigz is installed and --threads is
                          specified, output FASTQ files will be compressed with
                          pigz -p <n>; otherwise, they will be left
                          uncompressed (as it simply takes too long to compress
                          with just gzip).
"""
from __future__ import print_function




import docopt

def main():
    args = docopt(__doc__)
    print(args)
    exit()

