#!/usr/bin/env python

import ROOT 
import os 
import sys 
from scan import scanEFT
import argparse

def getLabel():

    tex = ROOT.TLatex  (0.55, .92, "AnalyticAnomalousCoupling")
    tex.SetNDC()
    tex.SetTextSize(0.76 * 0.05)
    tex.SetTextFont(52)
    tex.SetTextColor(ROOT.kBlack)
    tex.SetTextAlign(31)

    return tex


def getLumi(lumi, energy=13):

    tex = ROOT.TLatex(0.88,.92,"{} ".format(lumi) +  "fb^{-1}" +  " ({} TeV)".format(energy))
    tex.SetNDC()
    tex.SetTextAlign(31)
    tex.SetTextFont(42)
    tex.SetTextSize(0.04)
    tex.SetLineWidth(2)

    return tex

def getCMS():

    tex = ROOT.TLatex(0.22,.92,"CMS")
    tex.SetNDC()
    tex.SetTextFont(61)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.SetTextAlign(31)

    return tex

def getPreliminary():

    tex = ROOT.TLatex  (0.42, .92, "Preliminary")
    tex.SetNDC()
    tex.SetTextSize(0.76 * 0.05)
    tex.SetTextFont(52)
    tex.SetTextColor(ROOT.kBlack)
    tex.SetTextAlign(31)

    return tex

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This script allows to draw different gif plots for profiled EFT Fits using AnalyticalAnomalousCoupling')
    parser.add_argument('-p', '--POI',   dest='POI',     help='POIs to be plotted, default is \"r\"', required = False, default = "r", type=str, nargs="+")
    parser.add_argument('-maxNLL', '--maxNLL',   dest='maxNLL',     help='Set the maximum of the NLL to be plotted, default is 5 (-2deltaNLL=10)', required = False, default = 5, type=float)
    parser.add_argument('-o', '--output',   dest='output',     help='Path + filename + filetype for output. Default is scan.pdf', required = False, default = "scan.pdf", type=str)
    parser.add_argument('-lumi', '--lumi',   dest='lumi',     help='Draw this luminosity on the pad', required = False, default = "", type=str)
    parser.add_argument('-xlabel', '--xlabel',   dest='xlabel',     help='Fancy xlabel for the scan', required = False, default = "", type=str)
    parser.add_argument('-ylabel', '--ylabel',   dest='ylabel',     help='Fancy ylabel for the scan', required = False, default = "", type=str)
    parser.add_argument('-energy', '--energy',   dest='energy',     help='Draw this energy on the pad, default 13 TeV', required = False, default = 13, type=float)
    parser.add_argument('-cms', '--cms',   dest='cms',     help='Add cms label on top left', required = False, default = False, action="store_true")
    parser.add_argument('-preliminary', '--preliminary',   dest='preliminary',     help='Add preliminary label on top left', required = False, default = False, action="store_true")
    parser.add_argument('-isNuis', '--isNuis',   dest='isNuis',     help='Option for a 3d draw with 2 POI on x-y and -2DeltaNLL on z. Useful if x is POI and y is a nuisance', required = False, default = False, action="store_true")
    args, _ = parser.parse_known_args()

    if len(sys.argv) < 2:
        print("[ERROR] Usage python mkEFTScan.py <path_to_scan> -maxNLL (5) -lumi (\"\") -energy (13) -cms (False) -preliminary (False)")
        sys.exit(0)

    if len(args.POI) > 2:
        print("[ERROR] Specified {} operators to be plotted but only 2 are supported for plotting purposes".format(len(args.pois))) 

    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptStat(0000)

    scan = sys.argv[1]

    if len(args.POI) == 1: pois = args.POI[0]
    else: pois = args.POI

    scanUtil = scanEFT()
    scanUtil.setFile(scan)
    scanUtil.setTree("limit")
    scanUtil.setPOI(pois)
    scanUtil.setupperNLLimit(args.maxNLL)
    scanUtil.setNuisanceStyle(args.isNuis)
    
    gs = scanUtil.getScan()

    margins = 0.11
    if args.xlabel: gs.GetXaxis().SetTitle(args.xlabel)
    if args.ylabel: gs.GetYaxis().SetTitle(args.ylabel)

    c = ROOT.TCanvas("c", "c", 1000, 1000)

    ROOT.gPad.SetFrameLineWidth(3)

    if len(args.POI) == 1: ROOT.gPad.SetRightMargin(margins)
    elif len(args.POI) == 2: ROOT.gPad.SetRightMargin(0.15)
    
    ROOT.gPad.SetLeftMargin(margins)

    ROOT.gPad.SetTicks()

    if len(args.POI) == 1:

        gs.SetLineWidth(4)
        gs.SetLineColor(ROOT.kBlack)

        if args.xlabel: gs.GetXaxis().SetTitle(args.xlabel)

        gs.Draw("AL")
        
        min_x, max_x = gs.GetXaxis().GetXmin(), gs.GetXaxis().GetXmax() 

        x_frac = min_x + abs(0.05*(max_x-min_x))

        o_sigma = ROOT.TLine(min_x, 1, max_x, 1)
        o_sigma.SetLineStyle(2)
        o_sigma.SetLineWidth(2)
        o_sigma.SetLineColor(ROOT.kGray+2)
        t_sigma = ROOT.TLine(min_x, 3.84, max_x, 3.84)
        t_sigma.SetLineStyle(2)
        t_sigma.SetLineWidth(2)
        t_sigma.SetLineColor(ROOT.kGray+2)

        o_sigma.Draw("L same")
        t_sigma.Draw("L same")

        ois = ROOT.TLatex()
        ois.SetTextFont(42)
        ois.SetTextSize(0.03)
        ois.DrawLatex( x_frac, 1.05, '68%' )
        tis = ROOT.TLatex()
        tis.SetTextFont(42)
        tis.SetTextSize(0.03)
        tis.DrawLatex( x_frac, 3.89, '95%' )


    elif len(args.POI) == 2:
        
        exp = ROOT.TGraph()
        exp.SetPoint(0, 0, 0)
        exp.SetMarkerStyle(34)
        exp.SetMarkerSize(2)
        exp.SetMarkerColor(ROOT.kRed)

        conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
        cont_graphs = [conts.At(i) for i in range(len(conts))]

        colors = [ROOT.kRed, ROOT.kRed]
        linestyle = [1, 7]
        

        gs.GetZaxis().SetTitle("-2 #Delta LL")

        if args.isNuis:
           gs.SetNpx(200)
           gs.SetNpy(200)

           hist = gs.GetHistogram().Clone("arb_hist")

           for i in range(hist.GetSize()):
              hist.SetBinContent(i+1, 0);

           for i in range(gs.GetN()):
              hist.Fill(gs.GetX()[i],  gs.GetY()[i],  gs.GetZ()[i] + 0.001)


           xl = pois[0]
           yl = pois[1]
           if args.xlabel: xl = args.xlabel
           if args.ylabel: yl = args.ylabel


           hist.GetXaxis().SetTitle(xl)
           hist.GetYaxis().SetTitle(yl)
           hist.GetZaxis().SetTitle("-2 #Delta LL")
           hist.GetYaxis().SetTitleOffset(1.4)
           hist.GetXaxis().SetTitleOffset(1.1)

           hist.GetZaxis().SetRangeUser(0, float(args.maxNLL))


           hist.SetTitle("")
           hist.Draw("colz")


        else:

           for i in range(gs.GetHistogram().GetSize()):
               if (gs.GetHistogram().GetBinContent(i+1) == 0):
                   gs.GetHistogram().SetBinContent(i+1, 100)


           xl = pois[0]
           yl = pois[1]
           if args.xlabel: xl = args.xlabel
           if args.ylabel: yl = args.ylabel 


           gs.GetXaxis().SetTitle(xl)
           gs.GetYaxis().SetTitle(yl)

           gs.GetYaxis().SetTitleOffset(1.4)
           gs.GetXaxis().SetTitleOffset(1.1)

           gs.GetZaxis().SetRangeUser(0, float(args.maxNLL))
           gs.GetHistogram().GetZaxis().SetRangeUser(0, float(args.maxNLL))


           gs.GetHistogram().SetTitle("")
           gs.GetHistogram().Draw("colz")
        


        c.Modified()
        c.Update()

        leg = ROOT.TLegend(0.82, 0.85, 0.67, 0.7)
        leg.AddEntry(exp, "Expected", "P")
        leg.SetBorderSize(0)
       
        if not args.isNuis:
           for i, item_ in enumerate(cont_graphs):
               # item_ here is a TList
               l = list(item_)
               for item in l:
                   try:
                       item.SetLineColor(colors[i])
                       item.SetLineStyle(linestyle[i])
                       item.SetLineWidth(2)
                       item.Draw("L same")
                   except:
                       continue
               #only add one legend entry, arbitrary
               if len(l) > 0:
                   leg.AddEntry(l[0], "#pm {}#sigma".format(i+1), "L")

           exp.Draw("P same")
           leg.Draw()


    if not args.cms:
        tex = getLabel()
        tex.Draw()
    else:
        tex = getCMS()
        tex.Draw()
        if args.preliminary:
            tex2 = getPreliminary()
            tex2.Draw()

    if args.lumi:
        tex3 = getLumi(args.lumi)
        tex3.Draw()

    c.Draw()
    c.Print(args.output)
