#!/usr/bin/env python

from __future__ import print_function
import sys

"""
Usage:
        ~/code/uora/dupliganger/dupliganger/dupliganger/pipeline.py 4 outdir ACTTGATG_R1.3300 ACTTGATG_R2.3300
        ~/dupliganger/dupliganger/dupliganger/pipeline.py 4 outdir ACTTGATG_R1.3300 ACTTGATG_R2.3300

"""
# Usage:

num_threads = sys.argv[1]
outdir = sys.argv[2]
base = sys.argv[3]
base1 = sys.argv[4]
base2 = sys.argv[5]

obase1 = outdir + '/' + base1
obase2 = outdir + '/' + base2

print()
print("export PATH=/Users/jason/Library/Python/2.7/bin/:$PATH")
print()

cmd1 = "time dupliganger -o {} remove-umi -t {} --kit bioo {}.fq.gz {}.fq.gz".format(outdir, num_threads, base1, base2)
cmd2 = "time dupliganger -o {} remove-adapter {}.rmumi.fq {}.rmumi.fq".format(outdir, obase1, obase2)
cmd3 = "time dupliganger -o {} qtrim -t {} {}.rmumi.rmadapt.fq {}.rmumi.rmadapt.fq".format(outdir, num_threads, obase1, obase2)
# cmd4 = "dupliganger -o {} annotate-qtrim -t 2 {}.rmumi.rmadapt.fq {}.rmumi.rmadapt.fq {}.rmumi.rmadapt.qtrim.fq {}.rmumi.rmadapt.qtrim.fq".format(outdir, obase1, obase2, obase1, obase2)
cmd4 = "time dupliganger -o {} annotate-qtrim {}.rmumi.rmadapt.qtrim.fq {}.rmumi.rmadapt.qtrim.fq".format(outdir, obase1, obase2)
cmd5 = "mkdir -p {}/alignments".format(outdir)
cmd6 = "time gsnap -D ~/seq/gsnap/assemblies/zebrafish/Danio_rerio.GRCz10.dna.toplevel -d Danio_rerio.GRCz10.dna.toplevel -k 15 -B 5 -m 0.1 -t 30 -s ~/seq/gsnap/assemblies/zebrafish/Danio_rerio.GRCz10.dna.toplevel/Danio_rerio.GRCz10.dna.toplevel.maps/splicesitesfile.iit -A sam --split-output={}/alignments/{} -Q {}.rmumi.rmadapt.qtrim.anno.fq {}.rmumi.rmadapt.qtrim.anno.fq".format(outdir, base, obase1, obase2)

cmd = "{} && {} && {} && {} && {} && {} && echo && (echo Success && echo) || (echo Failure && echo)".format(cmd1, cmd2, cmd3, cmd4, cmd5, cmd6)
print("\t\t\t##### no-compress version #####")
print("  --- Commands ---")
print("1 - {}".format(cmd1))
print("2 - {}".format(cmd2))
print("3 - {}".format(cmd3))
print("4 - {}".format(cmd4))
print("5 - {}".format(cmd5))
print("6 - {}".format(cmd6))
print("  --- Copy-Paste ---")
print(cmd)

