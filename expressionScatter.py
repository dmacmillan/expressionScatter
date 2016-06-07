from Stat import *
import argparse, os, sys

parser = argparse.ArgumentParser(description='')

parser.add_argument('stat', nargs='+', help='One or more stats files')
#parser.add_argument('',help='')
#parser.add_argument('',help='')
parser.add_argument('-std', action='store_true', help='Output to standard out instead of to file. Overrides -o and -n')
parser.add_argument('-n', '--name', default='result', help='Name for the file output. Default is "result"')
parser.add_argument('-o', '--outdir', default=os.getcwd(), help='Path to output to. Default is {}'.format(os.getcwd()))

args = parser.parse_args()

if not os.path.isdir(args.outdir):
    os.makedirs(args.outdir)

stats = []

for stat in args.stat:
    print 'loading {}'.format(stat)
    stats += Stat.parseStat(stat)

gstats = Stat.groupStat(stats)

genes = {k:{'x':[],'y':[]} for k in [x for c in gstats for x in gstats[c].keys()]}

for chrom in gstats:
    for gene in gstats[chrom]:
        num_regions = len(gstats[chrom][gene])
        if num_regions == 1:
            continue
        for i in range(num_regions-1,0,-1):
            coord = [gstats[chrom][gene][i].median,
                     gstats[chrom][gene][i-1].median]
            genes[gene]['x'].append(coord[0])
            genes[gene]['y'].append(coord[1])

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

for g in genes:
    print 'generating {} ...'.format(g + '.png')
    if not genes[g]['x']:
        continue
    colors = np.random.rand(len(genes[g]['x']))
    x = genes[g]['x']
    y = genes[g]['y']
    plt.figure()
    plt.xlabel('Short Median Expression')
    plt.ylabel('Long Median Expression')
    plt.plot(x, y, '.')
    #plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x))
    plt.savefig(g+'.png')
