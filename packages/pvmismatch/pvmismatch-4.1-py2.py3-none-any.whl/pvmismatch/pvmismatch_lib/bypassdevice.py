#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:46:31 2018

@author: cchaudhari
"""
import numpy as np
from matplotlib import pyplot as plt

def get_max_num_cells_per_bypass_diode(Vrbd=5, Vbypass=0.5, Voc_cell=0.67, ncellperstr=24):
    """
    reuturns max num of cells per bypass diode to be used - conventional design
    """
    return np.floor(((Vrbd-Vbypass)/Voc_cell) + 1)
    
def get_min_shaded_cells_for_bypass(Vrbd=5, Vbypass=0.5, Voc_cell=0.67, ncellperstr=24):
    """
    returns minimum number cells to be shaded in a cell string for bypass condition to 
    be met.
    """
    for nshaded in range(ncellperstr):
        if ( (ncellperstr - nshaded) * Voc_cell + Vbypass) - nshaded * Vrbd < 0:
            return nshaded
        else:
            pass
    
Vrbd=5
Vbypass=0.5
Voc_cell=0.67
ncellperstr=24

print(get_max_num_cells_per_bypass_diode(Vrbd, Vbypass, Voc_cell, ncellperstr))

r = []
for ncellperstr in [12, 24, 48, 96]:
    r.append(get_min_shaded_cells_for_bypass(Vrbd, Vbypass, Voc_cell, ncellperstr))
plt.figure()
plt.plot([12, 24, 48, 96], r, '-o')
plt.xlabel('number of cells per cell string')
plt.ylabel('min number of cells shaded required for bypass diode to activate')
plt.grid(True)
plt.show()

##
from pvmismatch import *
from matplotlib import pyplot as plt
plt.ion()
pvsys = pvsystem.PVsystem()
pvsys.setSuns({1: {pvmod: 0.01 for pvmod in range(10)}})
pvsys.pvstrs[1].plotStr()
plt.tight_layout()
pvsys.plotSys()
plt.tight_layout()
pvsys.Pmp
##



pvm1 = pvmodule.PVmodule(Vbypass='None')
pvm1.setSuns( Ee = [200/1000.0 * j for j in [0.2] * 24 + [1.] * 48 + [1.] * 24])

pvm2 = pvmodule.PVmodule()
pvm2.setSuns( Ee = [200/1000.0 * j for j in [0.2] * 24 + [1.] * 48 + [1.] * 24])

plt.figure()
plt.plot(pvm1.Vmod, pvm1.Pmod)
plt.plot(pvm2.Vmod, pvm2.Pmod)
plt.xlabel('Voltage')
plt.ylabel('Power')
plt.xlim([0,70])
plt.ylim([0,300])
plt.grid(True)

plt.figure()
plt.plot(pvm1.Vmod, pvm1.Imod)
plt.plot(pvm2.Vmod, pvm2.Imod)
plt.xlabel('Voltage')
plt.ylabel('Current')
plt.xlim([0,70])
plt.ylim([0,10])
plt.grid(True)


import numpy as np
from matplotlib import patches
import matplotlib.pyplot as plt

cm = 1

xcenter, ycenter = 0.38*cm, 0.52*cm
width, height = 1e-1*cm, 3e-1*cm
angle = -30

theta = np.deg2rad(np.arange(0.0, 360.0, 1.0))
x = 0.5 * width * np.cos(theta)
y = 0.5 * height * np.sin(theta)

rtheta = np.radians(angle)
R = np.array([
    [np.cos(rtheta), -np.sin(rtheta)],
    [np.sin(rtheta),  np.cos(rtheta)],
])


x, y = np.dot(R, np.array([x, y]))
x += xcenter
y += ycenter

fig = plt.figure()
for aa in range(100):
    ax = fig.add_subplot(211, aspect='auto')
    ax.fill(x, y, alpha=0.2)
    e1 = patches.Ellipse( (aa* (xcenter), aa * np.cos(ycenter)), width, height, angle=angle, linewidth=2, fill=False, zorder=2)
    ax.add_patch(e1)
fig.show()

