from matplotlib import pyplot as plt
from pvmismatch.pvmismatch_lib.pvmodule import STD96
from pvmismatch import PVsystem, PVmodule, PVcell, PVconstants
from pvmismatch import *

def get_pvs(irr,temp,tech='E'):
	pvconstants = PVconstants(npts=10001)
	modules = {'E':{'Rs':0.0047299749332989785,'Rsh':11.288205142648826,'Isat1':1.9007562365404928e-11,'Isat2':1.044218374554042e-06,'Isc0_T0':6.549045},
	           'X':{'Rs':0.0022904553199000655,'Rsh':5.524413919705285,'Isat1':2.6951679883577537e-12,'Isat2':9.078875806333005e-07,'Isc0_T0':6.590375}}

	pvc = pvcell.PVcell(Rs=modules[tech]['Rs'],Rsh=modules[tech]['Rsh'],Isat1_T0=modules[tech]['Isat1'],Isat2_T0=modules[tech]['Isat2'],
	                    Isc0_T0=modules[tech]['Isc0_T0'],Ee=irr/1000.,Tcell=temp+273.15,pvconst=pvconstants)
	pvm = pvmodule.PVmodule(cell_pos=pvmodule.standard_cellpos_pat(1,[8]), pvcells=pvc, Vbypass=-0.5, pvconst=pvconstants)
	pvs = pvsystem.PVsystem(pvconst=pvconstants, pvmods=pvm, numberStrs=1, numberMods=1)
	return pvs

if __name__ == "__main__":
	pvconstants = PVconstants(npts=10001)
	modules = {'E':{'Rs':0.0047299749332989785,'Rsh':11.288205142648826,'Isat1':1.9007562365404928e-11,'Isat2':1.044218374554042e-06,'Isc0_T0':6.549045},
	           'X':{'Rs':0.0022904553199000655,'Rsh':5.524413919705285,'Isat1':2.6951679883577537e-12,'Isat2':9.078875806333005e-07,'Isc0_T0':6.590375}}

	tech = 'X'
	irr = 1000
	temp = 25

	pvc = pvcell.PVcell(Rs=modules[tech]['Rs'],Rsh=modules[tech]['Rsh'],Isat1_T0=modules[tech]['Isat1'],
	                    Isat2_T0=modules[tech]['Isat2'], Isc0_T0=modules[tech]['Isc0_T0'],
	                    Ee=irr/1000.,Tcell=temp+273.15,pvconst=pvconstants)
	pvm = pvmodule.PVmodule(cell_pos=pvmodule.standard_cellpos_pat(8,[1]), pvcells=pvc, Vbypass=-0.5, pvconst=pvconstants)
	
	pvs = pvsystem.PVsystem(pvconst=pvconstants, pvmods=[pvm], numberStrs=1, numberMods=1)

	pvs.setSuns(1)
	Pmp_0 = pvs.Pmp
	Vmp_0 = pvs.Vmp
	Imp_0 = pvs.Imp
	print Pmp_0, pvs.pvmods[0][0].Pmod.max(), Vmp_0, Imp_0

	plt.figure()
	plt.plot(pvs.Vstring, pvs.Istring)
	plt.plot(pvm.Vmod, pvm.Imod)