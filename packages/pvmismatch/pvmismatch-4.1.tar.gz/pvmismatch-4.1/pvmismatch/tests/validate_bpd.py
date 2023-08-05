
from nose.tools import ok_
from pvmismatch.pvmismatch_lib.pvmodule import PVmodule, TCT492, PCT492
import numpy as np
from matplotlib import pyplot as plt

pvm_list = []

pvm = PVmodule(Vbypass = [None, None, None])
ok_(np.isclose(pvm.Vmod.min(), -530.6169665707829))
pvm_list.append(pvm)

# only one cell string has a bypass diode
pvm = PVmodule(Vbypass = [None, None,-0.5])
ok_(np.isclose(pvm.Vmod.min(), -398.46272492808714))
pvm_list.append(pvm)

# two bypass diodes (middle removed)
pvm = PVmodule(Vbypass = [-0.5, None,-0.5])
ok_(np.isclose(pvm.Vmod.min(), -266.30848328539145))
pvm_list.append(pvm)

# all bypass diodes - same values
pvm = PVmodule(Vbypass = -0.2)
ok_(np.isclose(pvm.Vmod.min(), -0.6))
pvm_list.append(pvm)

# one bypass diode across the module
pvm = PVmodule(Vbypass = [-0.7])
ok_(np.isclose(pvm.Vmod.min(), -0.7))
pvm_list.append(pvm)

# default case
pvm = PVmodule()
ok_(np.isclose(pvm.Vmod.min(), pvm.Vbypass * 3))

plt.figure()
for pvm in pvm_list:
	plt.plot(pvm.Vmod, pvm.Imod)
plt.grid()
plt.legend(['No diodes', 'One diode two missing', 'two diodes, center missing', 'all diodes','module bypass'])
plt.show()
plt.xlabel('Voltage')
plt.ylabel('Current')