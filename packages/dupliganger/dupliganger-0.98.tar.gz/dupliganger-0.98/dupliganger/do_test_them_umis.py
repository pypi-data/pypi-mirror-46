"""

Basically, generate all possible combinations of 8nts.  For each sequence,
figure out closest UMIs, and count them.  For example, a sequence may have no
UMIs closer then 2 nts; that seq may be 2 nts away from 3 UMIs, and 3nts away
from 10 UMIs, and 4nts away from 44 UMIs, and so on...  Only count / report
that that sequence is 2 nts away from 3 UMIs.



include
Format:
    u1,u2   u1 is the closest away, and it has 

u1 exact, u2 exact                                          --> ACCEPTED                                        0,0 0,0
u1 exact, u2 is 1nt away from 1 UMI                         --> ACCEPTED                                        0,1 0,1
u1 exact, u2 is 1nt away from 2-4 UMIs                      --> ACCEPT and ITERATE over all combos              0,1 0,2-4
u1 exact, u2 is 2nt away from 1 UMI                         --> ACCEPTED                                        0,2 0,1
u1 exact, u2 is 2nt away from 2-8 UMIs                      --> ACCEPT and ITERATE over all combos              0,2 0,2-8
u1 exact, u2 is 3nt away from 1 UMI                         --> NOT SURE                                        0,3 0,1
u1 exact, u2 is 3nt away from 2-11 UMIs                     --> NOT SURE                                        0,3 0,2-11
u1 exact, u2 is 4nt away from 1-8 UMIs                      --> REJECT                                          0,4 0,1-8

u1 is 1nt away from 1 UMI, u2 is 1nt away from 1 UMI        --> ACCEPTED                                        1,1 1,1
u1 is 1nt away from 1 UMI, u2 is 1nt away from 2-4 UMIs     --> ACCEPT and ITERATE over all combos              1,1 1,2-4
u1 is 1nt away from 2-4 UMIs, u2 is 1nt away from 2-4 UMIs  --> ACCEPT and ITERATE over all combos              1,1 2-4,2-4

u1 is 1nt away from 1 UMI, u2 is 2nt away from 1 UMI        --> ACCEPTED                                        1,2 1,1
u1 is 1nt away from 1 UMI, u2 is 2nt away from 2-8 UMIs     --> ACCEPT and ITERATE over all combos              1,2 1,2-8
u1 is 1nt away from 2-4 UMIs, u2 is 2nt away from 2-8 UMIs  --> ACCEPT and ITERATE over all combos              1,2 2-4,2-8

u1 is 2nt away from 1 UMI, u2 is 2nt away from 1 UMI        --> ACCEPTED (probably)                             2,2 1,1
u1 is 2nt away from 1 UMI, u2 is 2nt away from 2-8 UMIs     --> ACCEPT and ITERATE over all combos              2,2 1,2-8
u1 is 2nt away from 2-8 UMIs, u2 is 2nt away from 2-8 UMIs  --> ACCEPT and ITERATE over all combos              2,2 2-8,2-8

Reject the case where none of the UMIs is at least 2nt away.



USE THIS TO SORT!!!
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892



0,0 0,0
0,1 0,1
0,1 0,2-4
0,2 0,1
0,2 0,2-8
0,3 0,1
0,3 0,2-11
0,4 0,1-8

1,1 1,1
1,1 1,2-4
1,1 2-4,2-4

1,2 1,1
1,2 1,2-8
1,2 2-4,2-8

2,2 1,1
2,2 1,2-8
2,2 2-8,2-8









raw report
{0: 96, 1: {1: 2038, 2: 110, 3: 14, 4: 1}, 2: {1: 15280, 2: 3060, 3: 474, 4: 104, 5: 25, 6: 4, 7: 1, 8: 1}, 3: {1: 10252, 2: 11496, 3: 8625, 4: 4774, 5: 2166, 6: 860, 7: 325, 8: 72, 9: 20, 10: 6, 11: 1}, 4: {1: 8, 2: 52, 3: 162, 4: 324, 5: 541, 6: 691, 7: 792, 8: 780, 9: 728, 10: 593, 11: 424, 12: 263, 13: 179, 14: 94, 15: 45, 16: 35, 17: 8, 18: 3, 19: 3, 20: 1, 24: 1}, 5: {24: 1, 18: 1, 28: 1, 21: 1}, 6: {}, 7: {}, 8: {}}



96 exact matches

distance == 0
	Number of sequences that have ** 1 ** closest UMIs: 96

distance == 1
	Number of sequences that have ** 1 ** closest UMIs: 2038
	Number of sequences that have ** 2 ** closest UMIs: 110
	Number of sequences that have ** 3 ** closest UMIs: 14
	Number of sequences that have ** 4 ** closest UMIs: 1

distance == 2
	Number of sequences that have ** 1 ** closest UMIs: 15280
	Number of sequences that have ** 2 ** closest UMIs: 3060
	Number of sequences that have ** 3 ** closest UMIs: 474
	Number of sequences that have ** 4 ** closest UMIs: 104
	Number of sequences that have ** 5 ** closest UMIs: 25
	Number of sequences that have ** 6 ** closest UMIs: 4
	Number of sequences that have ** 7 ** closest UMIs: 1
	Number of sequences that have ** 8 ** closest UMIs: 1

distance == 3
	Number of sequences that have ** 1 ** closest UMIs: 10252
	Number of sequences that have ** 2 ** closest UMIs: 11496
	Number of sequences that have ** 3 ** closest UMIs: 8625
	Number of sequences that have ** 4 ** closest UMIs: 4774
	Number of sequences that have ** 5 ** closest UMIs: 2166
	Number of sequences that have ** 6 ** closest UMIs: 860
	Number of sequences that have ** 7 ** closest UMIs: 325
	Number of sequences that have ** 8 ** closest UMIs: 72
	Number of sequences that have ** 9 ** closest UMIs: 20
	Number of sequences that have ** 10 ** closest UMIs: 6
	Number of sequences that have ** 11 ** closest UMIs: 1

distance == 4
	Number of sequences that have ** 1 ** closest UMIs: 8
	Number of sequences that have ** 2 ** closest UMIs: 52
	Number of sequences that have ** 3 ** closest UMIs: 162
	Number of sequences that have ** 4 ** closest UMIs: 324
	Number of sequences that have ** 5 ** closest UMIs: 541
	Number of sequences that have ** 6 ** closest UMIs: 691
	Number of sequences that have ** 7 ** closest UMIs: 792
	Number of sequences that have ** 8 ** closest UMIs: 780
	Number of sequences that have ** 9 ** closest UMIs: 728
	Number of sequences that have ** 10 ** closest UMIs: 593
	Number of sequences that have ** 11 ** closest UMIs: 424
	Number of sequences that have ** 12 ** closest UMIs: 263
	Number of sequences that have ** 13 ** closest UMIs: 179
	Number of sequences that have ** 14 ** closest UMIs: 94
	Number of sequences that have ** 15 ** closest UMIs: 45
	Number of sequences that have ** 16 ** closest UMIs: 35
	Number of sequences that have ** 17 ** closest UMIs: 8
	Number of sequences that have ** 18 ** closest UMIs: 3
	Number of sequences that have ** 19 ** closest UMIs: 3
	Number of sequences that have ** 20 ** closest UMIs: 1
	Number of sequences that have ** 24 ** closest UMIs: 1

distance == 5
	Number of sequences that have ** 18 ** closest UMIs: 1
	Number of sequences that have ** 21 ** closest UMIs: 1
	Number of sequences that have ** 24 ** closest UMIs: 1
	Number of sequences that have ** 28 ** closest UMIs: 1

distance == 6

distance == 7

distance == 8

"""
from __future__ import print_function





















import distance

UMIS_BIOO = ['AACGCCAT', 'AAGGTACG', 'AATTCCGG', 'ACACAGAG', 'ACACTCAG',
        'ACACTGTG', 'ACAGGACA', 'ACCTGTAG', 'ACGAAGGT', 'ACGACTTG', 'ACGTCAAC',
        'ACGTCATG', 'ACTGTCAG', 'ACTGTGAC', 'AGACACTC', 'AGAGGAGA', 'AGCATCGT',
        'AGCATGGA', 'AGCTACCA', 'AGCTCTAG', 'AGGACAAC', 'AGGACATG', 'AGGTTGCT',
        'AGTCGAGA', 'AGTGCTGT', 'ATAAGCGG', 'ATCCATGG', 'ATCGAACC', 'ATCGCGTA',
        'ATCGTTGG', 'CAACGATC', 'CAACGTTG', 'CAACTGGT', 'CAAGTCGT', 'CACACACA',
        'CAGTACTG', 'CATCAGCA', 'CATCGTTC', 'CCAAGGTT', 'CCTAGCTT', 'CGATTACG',
        'CGCCTATT', 'CGTTCCAT', 'CGTTGGAT', 'CTACGTTC', 'CTACTCGT', 'CTAGAGGA',
        'CTAGGAAG', 'CTAGGTAC', 'CTCAGTCT', 'CTGACTGA', 'CTGAGTGT', 'CTGATGTG',
        'CTGTTCAC', 'CTTCGTTG', 'GAACAGGT', 'GAAGACCA', 'GAAGTGCA', 'GACATGAG',
        'GAGAAGAG', 'GAGAAGTC', 'GATCCTAG', 'GATGTCGT', 'GCCGATAT', 'GCCGATTA',
        'GCGGTATT', 'GGAATTGG', 'GGATAACG', 'GGCCTAAT', 'GGCGTATT', 'GTCTTGTC',
        'GTGATGAG', 'GTGATGTC', 'GTGTACTG', 'GTGTAGTC', 'GTTCACCT', 'GTTCTGCT',
        'GTTGTCGA', 'TACGAACC', 'TAGCAAGG', 'TAGCTAGC', 'TAGGTTCG', 'TATAGCGC',
        'TCAGGACT', 'TCCACATC', 'TCGACTTC', 'TCGTAGGT', 'TCGTCATC', 'TGAGACTC',
        'TGAGAGTG', 'TGAGTGAG', 'TGCTTGGA', 'TGGAGTAG', 'TGTGTGTG', 'TTCGCCTA',
        'TTCGTTCG']


report = {}
# Set frequently accessed ones...
report[0] = 0
report[1] = {}
report[2] = {}
report[3] = {}
report[4] = {}
report[5] = {}
report[6] = {}
report[7] = {}
report[8] = {}


for i1 in 'ACGT':
# for i1 in 'A':
    print()
    print()
    print()
    print("i1 = {}".format(i1))
    for i2 in 'ACGT':
    # for i2 in 'A':
        print("i2 = {}".format(i2))
        for i3 in 'ACGT':
            for i4 in 'ACGT':
                for i5 in 'ACGT':
                    for i6 in 'ACGT':
                        for i7 in 'ACGT':
                            for i8 in 'ACGT':
                                seq_umi = "{}{}{}{}{}{}{}{}".format(
                                        i1, i2, i3, i4, i5, i6, i7, i8)
                                max_dist = 9999
                                d = 9999
                                found_umis = []
                                for umi in UMIS_BIOO:
                                    d = distance.hamming(umi, seq_umi)
                                    if d == max_dist:
                                        found_umis.append(umi)
                                    elif d < max_dist:
                                        # reset found_umis
                                        found_umis = [umi]
                                        max_dist = d
                                    if max_dist == 0:
                                        break
                                
                                # report
                                if max_dist == 0:
                                    report[0] += 1
                                else:
                                    # report[5][3] += 1
                                    # report.setdefault(max_dist, {})
                                    report[max_dist].setdefault(len(found_umis), 0)
                                    report[max_dist][len(found_umis)] += 1


print()
print()
print("raw report")
print(report)
print()

print("{} exact matches".format(report[0]))
for dist in [1, 2, 3, 4, 5, 6, 7, 8]:
    print()
    print("distance == {}".format(dist))
    for num_found_umis in sorted(report[dist].keys()):
        print("\tNumber of sequences that have ** {} ** closest UMIs: {}".format( num_found_umis, report[dist][num_found_umis]  ))

