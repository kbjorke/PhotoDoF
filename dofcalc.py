#!/usr/bin/env python

# By: Kristian Bjoerke

import numpy as np
import matplotlib.pyplot as plt
    
focl = 30 # [mm] focal length
F = 1.4 # Aperature F-number
dist = 2.0 # m

crop = 1.53 # Crop factor of sensor (aps-c)

#CoC = 0.05e-3 # Circle of confusion
CoC = 0.036e-3 # Circle of confusion | 15x10cm print, 25cm distance |  https://www.photopills.com/calculators/coc 
#CoC = 0.020e-3 # Circle of confusion | default Sony a6000 | https://www.photopills.com/calculators/coc

def dof(focl, F, dist):
    f = focl*crop*1e-3
    N = F
    D = dist
    C = CoC
    return (2*N*C*D**2*f**2)/(f**4 - N**2*C**2*D**2)
    #return (2*N*C*D**2)/(f**2)

def dof1(focl, F, dist):
    f = focl*crop*1e-3
    N = F
    D = dist
    C = CoC
    return (N*C*D**2)/(f**2 + N*C*D)

def dof2(focl, F, dist):
    f = focl*crop*1e-3
    N = F
    D = dist
    C = CoC
    return (N*C*D**2)/(f**2 - N*C*D)

def H(focl, F):
    f = focl*crop*1e-3
    N = F
    C = CoC
    return (f**2)/(N*C) + f


if __name__=="__main__":

    from ROOT import gROOT, TCanvas, TH2D, gStyle

    #gStyle.SetPalette(85)
    gStyle.SetNumberContours(255)

    F_array = np.array([1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22])
    dist_array = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    focl_array = np.array([16, 20, 30, 40, 50, 100, 210])

    nF = len(F_array)
    ndist = len(dist_array)
    nfocl = len(focl_array)

    h_H = TH2D("hist_H", "hist_H", nfocl , 0, nfocl, nF, 0, nF) 
    h_H2 = TH2D("hist_H2", "hist_H2", nfocl , 0, nfocl, nF, -0.3, nF-0.3) 

    for i in range(nfocl):
        focl = focl_array[i]
        for j in range(nF):
            F = F_array[j]
            h_H.SetBinContent(i+1, nF-j, H(focl, F))
            h_H2.SetBinContent(i+1, nF-j, H(focl, F)/2.0)

    for i in range(nfocl):
        h_H.GetXaxis().SetBinLabel(i+1, "%3d mm" % focl_array[i])
    for j in range(nF):
        h_H.GetYaxis().SetBinLabel(nF-j, "f/%3.1f" % F_array[j])

    canvas1 = TCanvas("canvas1", "canvas1", 1500, 900)
    canvas1.SetLogz()
    canvas1.SetGrid()
    canvas1.SetLeftMargin(0.10)
    canvas1.SetRightMargin(0.16)
    canvas1.SetTopMargin(0.11)
    canvas1.SetBottomMargin(0.10)
    gStyle.SetOptStat(0)
    gStyle.SetPaintTextFormat(".2f m")
    gStyle.SetTextFont(40)
    h_H.SetTitle("")
    #h_H.SetTitle("Hyperfocal distance | Sony a6000 (aps-c) | CoC = %.03f mm" % (CoC*1e3))
    h_H.GetXaxis().SetTitle("Focal length")
    h_H.GetXaxis().CenterTitle()
    h_H.GetXaxis().SetTitleSize(0.05)
    h_H.GetXaxis().SetTitleOffset(0.9)
    h_H.GetXaxis().SetLabelSize(0.05)
    h_H.GetYaxis().SetTitle("Aperture")
    h_H.GetYaxis().SetTitleSize(0.05)
    h_H.GetYaxis().SetTitleOffset(0.9)
    h_H.GetYaxis().SetLabelSize(0.05)
    h_H.GetYaxis().CenterTitle()
    h_H.GetZaxis().SetRangeUser(0.1, 1000)
    h_H.GetZaxis().SetNoExponent()
    h_H.GetZaxis().SetTitle("Hyperfocal distance [m]")
    h_H.GetZaxis().SetTitleSize(0.05)
    h_H.GetZaxis().SetTitleOffset(0.9)
    h_H.GetZaxis().CenterTitle()
    h_H.SetMarkerSize(1.4)
    h_H.Draw("COLZ X+")
    h_H.Draw("TEXT same")
    h_H2.Draw("TEXT same")

    canvas1.SaveAs("hyperfocal-distance.eps")

    #focl = 30

    #h_dof = TH2D("hist_dof", "hist_dof", ndist, -0.5, ndist-0.5, nF, -0.5, nF-0.5) 
    #h_fnrat = TH2D("hist_fnrat", "hist_fnrat", ndist, -0.5, ndist-0.5, nF, -0.5, nF-0.5) 

    #for i in range(ndist):
    #    dist = dist_array[i]
    #    for j in range(nF):
    #        F = F_array[j]
    #        dof_ = dof(focl,F,dist)
    #        if dof_ > 0:
    #            h_dof.SetBinContent(i+1,nF-j,dof_)
    #            h_fnrat.SetBinContent(i+1,nF-j,dof2(focl,F,dist)/dof1(focl,F,dist))

    #for i in range(ndist):
    #    h_dof.GetXaxis().SetBinLabel(i+1, "%3.1f m" % dist_array[i])
    #    h_fnrat.GetXaxis().SetBinLabel(i+1, "%3.1f m" % dist_array[i])
    #for j in range(nF):
    #    h_dof.GetYaxis().SetBinLabel(nF-j, "f/%3.1f" % F_array[j])
    #    h_fnrat.GetYaxis().SetBinLabel(nF-j, "f/%3.1f" % F_array[j])

    #canvas2 = TCanvas("canvas2", "canvas2", 1400, 1200)
    #canvas2.SetLogz()
    #gStyle.SetOptStat(0)
    #gStyle.SetPaintTextFormat("4.3f")
    ##h_dof.GetZaxis().SetRangeUser(0.0, 3.0)
    #h_dof.GetZaxis().SetRangeUser(0.01, 30.0)
    #h_dof.Draw("COLZ")
    #h_dof.Draw("TEXT same")

    #canvas3 = TCanvas("canvas3", "canvas3", 1400, 1200)
    #canvas3.SetLogz()
    #gStyle.SetOptStat(0)
    #gStyle.SetPaintTextFormat("4.3f")
    #h_fnrat.GetZaxis().SetRangeUser(1.00, 5.00)
    #h_fnrat.Draw("COLZ")
    #h_fnrat.Draw("TEXT same")

    raw_input("")

