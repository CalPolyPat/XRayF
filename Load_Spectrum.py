#This file will open and read XRay Spectra from the .mca filetype.

import ROOT
from ROOT import TH1F, gROOT, TCanvas, SetOwnership
import rootnotes
import rootprint

gROOT.Reset()
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetFillColor(0)

def Load_Spectrum(filename, histname, normret=False):
    f = open(filename)
    workline = ""
    norm = 0;
    n=0
    data = []
    record = False
    getnorm = True

    for line in f:
        j=0
        workline = ""
        if getnorm == True:
            while line[j]!=chr(32):
                workline = workline+line[j]
                j+=1
            if workline == "LIVE_TIME":
                norm = line[-11:-1]
                getnorm = False
            print norm
        if str(line) == '<<END>>\n':
            record = False    
            print "Data feed end"
        if str(line).startswith('MCAC'):
            chan=line[5:8]
            print chan
        if record == True:
            data.append(int(line))
        if str(line) == "<<DATA>>\n":
            record = True
            print "Data feed start"
    for i in xrange(len(data)):
        data[i]=data[i]/float(norm)

    spect = ROOT.TH1F("spect", histname, int(chan), 0, float(chan))
    i = 1
    for d in data:
        spect.Fill(i, d)
        i=i+1
    normal = 1;
    n=spect.GetEntries()
    spect.Scale(normal/spect.Integral("width"))
    print("It is updating")
    if normret:
        return spect, n
    return spect