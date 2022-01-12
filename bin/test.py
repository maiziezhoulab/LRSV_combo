import numpy as np

#print(np.round(1.7263427645,4))
#print(np.round(float("1.0")/0.1-1).astype(int))

import re

line = 'chr1	2897592	cuteSV.DEL.45	AGGAGGTCTGGTAACAGGAGGTCTGGTAACA	A	93.2	PASS	PRECISE;SVTYPE=DEL;SVLEN=-30;END=2897622;CIPOS=-1,1;CILEN=-0,0;RE=21;RNAMES=NULL;STRAND=+-	GT:DR:DV:PL:GQ	0/1:21:21:93,0,93:90'

line_list = line.rstrip("\n").split("\t")
print(re.findall("SVLEN=(-?\d+)",line)[0])
print(re.findall("SVLEN=-?(\d+)",line)[0])
print(re.findall("SVLEN=-?\d+",line)[0])
print(re.findall("SVTYPE=\w+",line)[0])
print(re.findall("SVTYPE=(\w+)",line)[0])
print(re.findall("END=\d+",line)[0])
print(re.findall("CIPOS=-?([\d,]+)",line)[0].split(',')[0])
print(re.findall("CIPOS=([^;\t]+)",line)[0])



a = [0]*10
a[1] = 1
print(a)

b = np.inf
print(50<b)

#ax = df.plot(x="X", y="A", kind="bar")
#df.plot(x="X", y="B", kind="bar", ax=ax, color="C2")
#df.plot(x="X", y="C", kind="bar", ax=ax, color="C3")
#df.plot(x="X", y=["A", "B", "C"], kind="bar")

print('GT'.split(','))
print('SC='.replace('SC=', 'SC=,'))
print('SC'.replace('SC=', 'SC=,'))
print('SC' in 'SC=')