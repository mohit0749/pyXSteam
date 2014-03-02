# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as pyplot
import numpy as np
from pyXSteam.XSteam import XSteam
# import time

def demo_simpel_Values():
    steamTable = XSteam(mksSystem = True)
    print steamTable.hL_p(220.0)  # get saturated liquid enthalpy for a preasure of 220 bar
    print steamTable.hV_p(220.0)  # get saturated vapour enthalpy for a preasure of 220 bar

def demo_generate_ph_Diagramm(path = None, precision = 1.0):
    '''Generate a p(h) Diagramm showing the Saturation Line'''
    steamTable = XSteam(mksSystem = True)
    p_krit = steamTable.criticalPressure() - 0.0001  # minus 0.0001 or else hL_V return NaN
    h_krit = steamTable.hL_p(p_krit)

    p = np.arange(0.0, 1000, precision)
    p2 = np.arange(0.5, p_krit, precision)
    vaporFrac = np.arange(0.1, 1.0, 0.1)
    h = np.arange(500.0, 4500.0, 100.0)
    rho = np.arange(1, 100.0, precision * 10)

    nph_px = np.frompyfunc(steamTable.h_px, 2, 1)
    nph_pt = np.frompyfunc(steamTable.h_pt, 2, 1)
    nphL_p = np.frompyfunc(steamTable.hL_p, 1, 1)
    nphV_p = np.frompyfunc(steamTable.hV_p, 1, 1)
    npp_hrho = np.frompyfunc(steamTable.p_hrho, 2, 1)

    # Siede und Taulinie
    hL = nphL_p(p)
    hV = nphV_p(p)

    # Dampfgehalt
    for vf in vaporFrac:
        h_px = nph_px(p2, vf)
        line, = pyplot.plot(h_px, p2)
        pyplot.setp(line, linewidth = 1, color = 'g')

    # Temperatur
    for temp in range(0, 900, 50):
        h_pt = nph_pt(p, temp)
        line, = pyplot.plot(h_pt, p)
        pyplot.setp(line, linewidth = 1, color = 'r')

    # Dichte
    for r in rho:
        p_hrho = npp_hrho(h, r)
        line, = pyplot.plot(h, p_hrho)
        pyplot.setp(line, linewidth = 1, color = 'y')

    # Kritischer Punkt
    pyplot.plot([h_krit], [ p_krit], marker = 's', mfc = 'k', ms = 8)

    line1, = pyplot.plot(hL, p)
    line2, = pyplot.plot(hV, p)
    pyplot.xlabel("h in [kJ/kg]")
    pyplot.ylabel("p in [bar]")
    pyplot.setp(line1, linewidth = 2, color = 'b')
    pyplot.setp(line2, linewidth = 2, color = 'r')
    # pyplot.yscale('log')
    pyplot.grid()

    if path == None:
        pyplot.show()
    else:
        pyplot.savefig(path, bbox_inches = 'tight')


def demo_generate_Tp_Diagramm():
    '''Generate a T(p) Diagramm showing the Saturation Curve'''
    steamTable = XSteam(mksSystem = True)
    p = np.arange(-100.0, 250.0, 1.0)
    ntsat_p = np.frompyfunc(steamTable.tsat_p, 1, 1)
    tsat = ntsat_p(p)

#    p_tripel = steamTable.triplePointPreasure()
#    t_tripel = steamTable.triplePointTemperatur()
#    print p_tripel, t_tripel
#    pyplot.plot([t_tripel], [ p_tripel], marker = 's', mfc = 'k', ms = 8)

    line1, = pyplot.plot(tsat, p)
    pyplot.xlabel("t")
    pyplot.ylabel("p")
    pyplot.setp(line1, linewidth = 1, color = 'b')
    pyplot.show()

def demo_generate_pvT_Diagramm():
    steamTable = XSteam(mksSystem = True)
    fig = pyplot.figure()
    ax = Axes3D(fig)

    p = np.arange(-10.0, 300.0, 5.0)
    t = np.arange(-50.0, 400.0, 5.0)
    p, t = np.meshgrid(p, t)

    npv_pt = np.frompyfunc(steamTable.v_pt, 2, 1)
    v = npv_pt(p, t)

    ax.plot_surface(v, p, t, rstride = 1, cstride = 1, linewidth = 0, shade = True)
    ax.set_xlabel("v")
    ax.set_ylabel("p")
    ax.set_zlabel("t")
    pyplot.show()

def demo_Moillier_Diagramm():
    steamTable = XSteam(mksSystem = True)
    s = np.arange(2.0 , 10.0, 0.01)
    # h = np.arange(1800 , 4200, 50)

    pSteps = [0.006117, 0.01, 0.02, 1.0, 2.0, 3.0, 10, 100, 1000]

    nph_ps = np.frompyfunc(steamTable.h_ps, 2, 1)

    # Preasure
    for pstep in pSteps:
        h = nph_ps(pstep, s)
        hline, = pyplot.plot(s, h)
        pyplot.setp(hline, linewidth = 1, color = 'b')

    pyplot.xlabel("s in [kJ/(kg K)]")
    pyplot.ylabel("h in [kJ/kg]")
    pyplot.show()

if __name__ == '__main__':
    # start = time.clock()
    # demo_simpel_Values()
    demo_generate_ph_Diagramm()
    # demo_generate_Tp_Diagramm()
    # demo_generate_pvT_Diagramm()
    # demo_Moillier_Diagramm()
    # print time.clock() - start, 'Seconds'

