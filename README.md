# COPV-Tank-Solver
A Python script to calculate parameters for the design and manufacture of a Type 3 COPV (Composite Overwrapped Pressure Vessel) based on some inputs.

The code consists of two main scripts - one for the nitrous oxide tank and one for the nitrogen tank.

The goal of the individial modules are -

1. main.py:
    Run the required modules in order and provide an output text file.

2. Inputs.py:
    Accepts the needed inputs.

3. Nitrous_Tank.py:
    Calculate the length and outer diameter of the tank.

4. Nitrogen_Script.py:
    Calculate how much nitrogen is needed for pressurisation and the tank dimensions required to store it.

5. Geodesic_Dome.py:
    Create the geodesic dome shape for the domes on both tanks. A geodesic shape is required to ensure that the carbon fibre wrapping does not slip and natural alignment of fibres.

6. COPV_Netting_Analysis.py:
    Determines important parameters for winding of the liner with carbon fibre (wind angle, hoop and longitudinal wind fractions, total wind thickness)

7. Total_System_Dimensions.py:
    Calculates the total length of the tank system (nitrous tank + nitrogen tank + plumbing)

8. Plotting.py:
    Plots the geodesic dome geometry and exports it.

9. DXF_Export.py:
    Exports the geodesic dome spline as a DXF for import into CAD.

10. Working_Memory.py:
    Stores values from the nitrous and nitrogen tank scripts for use in other scripts.

When run from main.py, the script takes in input parameters for BOTH nitrous and nitrogen tanks and calculates the relevant parameters and outputs them in a .txt file.

The nitrogen and nitrous tank modules can be run individually to provide the values for the respective tank.

**IMPORTANT**
To receive the DXF file for dome geometry for import into CAD, the Geodesic_Dome.py needs to be run individually with inputs in 'General Tank Properties' in Inputs.py.

To run the geodesic dome solver, first add an environment variable specifying the directory to save the exported CSV and plot in.