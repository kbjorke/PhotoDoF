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
    
    dist_array2D = np.array([
        [0.5, 1, 1.5, 2, 2.5, 3, 5, 8],
        [0.5, 1, 1.5, 2, 3, 5, 8, 10],
        [0.5, 1, 1.5, 2, 3, 5, 10, 20],
        [0.5, 1, 1.5, 2, 3, 5, 10, 30],
        [1.0, 2, 3, 5, 10, 20, 30, 50],
        [1.0, 2, 5, 10, 20, 50, 100, 200],
        [2, 5, 10, 50, 100, 200, 500, 1000]
        ])
    
    F_array2D = np.array([
        [1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22],
        [1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22],
        [1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22],
        [4, 5.6, 8, 11, 16, 22, 32],
        [4, 5.6, 8, 11, 16, 22, 32],
        [5.6, 8, 11, 16, 22, 32],
        [5.6, 8, 11, 16, 22, 32],
        ])

    dof_zrange_array = np.array([
        (0.01, 30.0),
        (0.01, 30.0),
        (0.01, 30.0),
        (0.005, 40.0),
        (0.005, 40.0),
        (0.001, 200.0),
        (0.001, 200.0),
        ])

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

    canvas1.SaveAs("pdf/img/hyperfocal-distance.eps")

    #focl = 30
    #l = 2
    for l in range(nfocl):
        focl = focl_array[l]
        nF = len(F_array2D[l])

        h_dof = TH2D("hist_dof_focl%d" %focl, "hist_dof_focl%d" %focl, ndist, 0, ndist, nF, 0, nF) 
        h_fnrat = TH2D("hist_fnrat_focl%d" %focl, "hist_fnrat_focl%d" %focl, ndist, 0, ndist, nF, 0, nF) 

        for i in range(ndist):
            dist = dist_array2D[l][i]
            for j in range(nF):
                F = F_array[j]
                dof_ = dof(focl,F,dist)
                if dof_ > 0:
                    h_dof.SetBinContent(i+1,nF-j,dof_)
                    h_fnrat.SetBinContent(i+1,nF-j,dof2(focl,F,dist)/dof1(focl,F,dist))

        for i in range(ndist):
            h_dof.GetXaxis().SetBinLabel(i+1, "%3.1f m" % dist_array2D[l][i])
            h_fnrat.GetXaxis().SetBinLabel(i+1, "%3.1f m" % dist_array2D[l][i])
        for j in range(nF):
            h_dof.GetYaxis().SetBinLabel(nF-j, "f/%3.1f" % F_array2D[l][j])
            h_fnrat.GetYaxis().SetBinLabel(nF-j, "f/%3.1f" % F_array2D[l][j])

        canvas2 = TCanvas("canvas2", "canvas2", 1500, 900)
        canvas2.SetLogz()
        canvas2.SetGrid()
        canvas2.SetLeftMargin(0.10)
        canvas2.SetRightMargin(0.16)
        canvas2.SetTopMargin(0.11)
        canvas2.SetBottomMargin(0.10)
        gStyle.SetOptStat(0)
        gStyle.SetPaintTextFormat(".2f m")
        gStyle.SetTextFont(40)
        h_dof.SetTitle("")
        h_dof.GetXaxis().SetTitle("Focus distance")
        h_dof.GetXaxis().CenterTitle()
        h_dof.GetXaxis().SetTitleSize(0.05)
        h_dof.GetXaxis().SetTitleOffset(0.9)
        h_dof.GetXaxis().SetLabelSize(0.05)
        h_dof.GetYaxis().SetTitle("Aperture")
        h_dof.GetYaxis().SetTitleSize(0.05)
        h_dof.GetYaxis().SetTitleOffset(0.9)
        h_dof.GetYaxis().SetLabelSize(0.05)
        h_dof.GetYaxis().CenterTitle()
        #h_dof.GetZaxis().SetRangeUser(0.01, 30.0)
        h_dof.GetZaxis().SetRangeUser(dof_zrange_array[l][0], dof_zrange_array[l][1])
        h_dof.GetZaxis().SetNoExponent()
        h_dof.GetZaxis().SetTitle("Depth of field [m]")
        h_dof.GetZaxis().SetTitleSize(0.05)
        h_dof.GetZaxis().SetTitleOffset(0.9)
        h_dof.GetZaxis().CenterTitle()
        h_dof.SetMarkerSize(1.4)
        h_dof.Draw("COLZ X+")
        h_dof.Draw("TEXT same")
        
        canvas2.SaveAs("pdf/img/depth-of-field_focl%d.eps" %focl)

        canvas3 = TCanvas("canvas3", "canvas3", 1500, 900)
        canvas3.SetLogz()
        canvas3.SetGrid()
        canvas3.SetLeftMargin(0.10)
        canvas3.SetRightMargin(0.16)
        canvas3.SetTopMargin(0.11)
        canvas3.SetBottomMargin(0.10)
        gStyle.SetOptStat(0)
        gStyle.SetPaintTextFormat(".2f")
        gStyle.SetTextFont(40)
        h_fnrat.SetTitle("")
        h_fnrat.GetXaxis().SetTitle("Focus distance")
        h_fnrat.GetXaxis().CenterTitle()
        h_fnrat.GetXaxis().SetTitleSize(0.05)
        h_fnrat.GetXaxis().SetTitleOffset(0.9)
        h_fnrat.GetXaxis().SetLabelSize(0.05)
        h_fnrat.GetYaxis().SetTitle("Aperture")
        h_fnrat.GetYaxis().SetTitleSize(0.05)
        h_fnrat.GetYaxis().SetTitleOffset(0.9)
        h_fnrat.GetYaxis().SetLabelSize(0.05)
        h_fnrat.GetYaxis().CenterTitle()
        h_fnrat.GetZaxis().SetRangeUser(1.00, 5.00)
        h_fnrat.GetZaxis().SetNoExponent()
        h_fnrat.GetZaxis().SetMoreLogLabels()
        h_fnrat.GetZaxis().SetTitle("Far-near ratio")
        h_fnrat.GetZaxis().SetTitleSize(0.05)
        h_fnrat.GetZaxis().SetTitleOffset(0.7)
        h_fnrat.GetZaxis().CenterTitle()
        h_fnrat.SetMarkerSize(1.4)
        h_fnrat.Draw("COLZ X+")
        h_fnrat.Draw("TEXT same")
        
        canvas3.SaveAs("pdf/img/far-near-ratio_focl%d.eps" %focl)

        #raw_input("")

