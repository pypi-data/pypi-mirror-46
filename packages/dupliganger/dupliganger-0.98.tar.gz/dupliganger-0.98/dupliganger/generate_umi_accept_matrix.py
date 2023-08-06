from __future__ import print_function
from builtins import range




# Input Format is:
#   a,b c,d
# where
#   a and b are the number of nts away from a UMI for the first/second UMI
#   c and d are the number of UMIs that are a and b nts away from the first and second UMI respectively
# and always:
#   a <= b
# and sometimes:
#   c and d can be either an integer or a range.
#
# Output Format is as follows:
#   Given:
#       "a,b c,d"
#   Output:
#       (a,b,c,d), (b,a,d,c)
meta_format = """
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


USE THIS TO SORT!!!
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892
http://stackoverflow.com/a/673892


"""

#thing = set()
thing = []

for line in meta_format.split('\n'):
    line = line.strip()
    if line == '':
        continue
    if line[0] == '#':
        continue

    dists, num_umis = line.split()

    dist1, dist2 = dists.split(',')
    dist1 = int(dist1)
    dist2 = int(dist2)

    n_umis1, n_umis2 = num_umis.split(',')

    if '-' in n_umis1:
        s,e = n_umis1.split('-')
        s = int(s)
        e = int(e)
        n_umis1 = list(range(s, e+1))
    else:
        n_umis1 = [int(n_umis1)]

    if '-' in n_umis2:
        s,e = n_umis2.split('-')
        s = int(s)
        e = int(e)
        n_umis2 = list(range(s, e+1))
    else:
        n_umis2 = [int(n_umis2)]


    for n_umi1 in n_umis1:
        for n_umi2 in n_umis2:
            # thing.add((dist1, dist2, n_umi1, n_umi2))
            # thing.add((dist2, dist1, n_umi2, n_umi1))
            thing.append((dist1, dist2, n_umi1, n_umi2))
            thing.append((dist2, dist1, n_umi2, n_umi1))

print(thing)

