import numpy as np
import matplotlib.pyplot as plt
import requests
from StringIO import StringIO
'''
Changelog
I basically just changed the datatypes of all your xray lines to dictionaries.
'''
onestopshop = 'http://physics.nist.gov/cgi-bin/XrayTrans/search.pl?download=column&sorttype=transition&element=All&trans=All&lower=1000&upper=30000&units=eV'
response = requests.get(onestopshop)

Ka1 = {}
Ka2 = {}
Ka = {}
Kb1 = {}
La1 = {}
La2 = {}
La = {}
Lb1 = {}
#Extract experimental data for line
content = StringIO(response.content).read()
linecount = 0
for line in content.splitlines():
    if linecount < 23:
        if "Direct (eV)       =" in line: #Why is this section here?
            startXray = int(line[22:24])-1
            endXray = int(line[27:29])-1
        if "Trans.              =" in line:
            startTrans = int(line[22:24])-1
            endTrans = int(line[27:29])-1
    else:
        if "KL2" in line[startTrans:endTrans]:
            #print line[0:4],line[startTrans:endTrans],line[startXray:endXray]
            #Not all elements have a given xray line
            if line[startXray:endXray] != (endXray-startXray)*' ':
                Ka2["'" + line[0:2] + "'"]=float(line[startXray:endXray])*1.e-3
        if "KL3" in line[startTrans:endTrans]:
            #print line[0:4],line[startTrans:endTrans],line[startXray:endXray]
            #Not all elements have a given xray line
            if line[startXray:endXray] != (endXray-startXray)*' ':
                Ka1["'" + line[0:2] + "'"]=float(line[startXray:endXray])*1.e-3
        if "KM3" in line[startTrans:endTrans]:
            #print line[0:4],line[startTrans:endTrans],line[startXray:endXray]
            #Not all elements have a given xray line
            if line[startXray:endXray] != (endXray-startXray)*' ':
                Kb1["'" + line[0:2] + "'"]=float(line[startXray:endXray])*1.e-3
        if "L3M5" in line[startTrans:endTrans]:
            #print line[0:4],line[startTrans:endTrans]
            #Not all elements have a given xray line
            if line[startXray:endXray] != (endXray-startXray)*' ':
                La1["'" + line[0:2] + "'"]=float(line[startXray:endXray])*1.e-3
        if "L3M4" in line[startTrans:endTrans]:
            #print line[0:4],line[startTrans:endTrans]
            #Not all elements have a given xray line
            if line[startXray:endXray] != (endXray-startXray)*' ':
                La2["'" + line[0:2] + "'"]=float(line[startXray:endXray])*1.e-3
        if "L2M4" in line[startTrans:endTrans]:
            #print line[0:4],line[startTrans:endTrans]
            #Not all elements have a given xray line
            if line[startXray:endXray] != (endXray-startXray)*' ':
               Lb1["'" + line[0:2] + "'"]=float(line[startXray:endXray])*1.e-3
    linecount += 1
    '''
	Here I average the K alpha and L alpha lines
	But some L-lines have no pair, this is why the key error is there.
	'''
for key in Ka1.keys():
    Ka[key] = (Ka1[key]+Ka2[key])/2.
for key in La1.keys():
	try:
		La[key] = (La1[key]+La2[key])/2.
	except KeyError:
		print "These are not the L-lines you are looking for"
