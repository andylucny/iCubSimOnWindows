# iCubSimOnWindows
iCubSim simulator, its Python bindings and demos

Download the simulator from www.agentspace.org/download/iCubSim.zip
and unpack it into the iCubSimOnWindows directory. 

Run init-bindings.bat or copy bindings manualy to have appropriate _yarp.pyd 
and yarp.py in the working directory. 

Start iCubSim\run-iCubSim.bat and wait until it is fully running.
Confirm each firewall permission.

Run a demo based on the pyicubsim library, which simplifies the work with iCubSim a lot.

if yarpserver is not starting, change line

start yarpserver.exe

to

start yarpserver.exe --write

for the next start
