# What is CoCo?

CoCo ("Complementary Coordinates") is a method for testing and potentially enriching the the variety of conformations within an ensemble of molecular structures. It was originally developed with NMR datasets in mind and the background and this application is described in:

[Laughton C.A., Orozco M. and Vranken W., COCO: A simple tool to enrich the representation of conformational variability in NMR structures, PROTEINS, 75, 206-216 (2009)](http://onlinelibrary.wiley.com/doi/10.1002/prot.22235/abstract)

CoCo, which is based on principal component analysis, analyses the distribution of an ensemble of structures in conformational space, and generates a new ensemble that fills gaps in the distribution. These new structures are not guaranteed to be valid members of the ensemble, but should be treated as possible, approximate, new solutions for refinement against the original data.
Though developed with protein NMR data in mind, the method is quite general – the initial structures do not have to come from NMR data, and can be of nucleic acids, carbohydrates, etc.

The outline of the CoCo method is as follows:

![COCO method2.gif](https://bitbucket.org/repo/bAGR4M/images/1692328909-COCO%20method2.gif)
Step 1: The input ensemble is subjected to Principal Component Analysis and the position of each structure in a low dimensional subspace identified.

Step 2: New points are placed to fill gaps in the distribution.

Step 3: The new points are converted back into new structures, which are returned to the user.


This package provides a python-based command line tool that implements the CoCo method.

Recently we have shown how CoCo can be used within an iterative simulation/analysis workflow as a very
effective enhanced sampling method:

[Shkurti A, Styliari I.D., Balasubramanian V., Bethune, I., Pedebos, C., Jha, S., and Laughton C.A. CoCo-MD: A simple and effective method for the 
enhanced sampling of conformational space. J. Comp. Chem. 2019](https://pubs.acs.org/doi/10.1021/acs.jctc.8b00657)

Python scripts that exemplify this workflow are available in the examples folder.

------

# Installation

## ... Linux (Desktop)

CoCo depends on `numpy`, `scipy`, and [pyPcazip](https://bitbucket.org/ramonbsc/pypcazip). With a bit of luck all these will be resolved automatically if CoCo is installed with pip:

```
pip install extasy.coco --user
```

If you prefer/require to install from source, the procedure is:

```
git clone https://bitbucket.org/extasy-project/coco.git
cd coco
python setup.py install --user
```

# Using the Command Line Tool "pyCoCo"

In the ./example subdirectory is a test script to run a simple CoCo analysis. Four short trajectory files (AMBER .ncdf format) and an associated topology file for penta-alanine (penta.top) are provided. The test script analyses the ensemble and generates eight new structures, in PDB format, that represent apparent gaps in the sampling of conformational space. To run the test example type:

```
./test.sh
```
When the job completes (less than a minute), you should see eight new pdb files (Ala5coco0.pdb - Ala5coco7.pdb), and a log file (test.log).
The log file should look like this:
```
*** pyCoCo ***

Trajectory files to be analysed:
md0.dcd: frames: 10 
md1.dcd: frames: 10 
md2.dcd: frames: 10 
md3.dcd: frames: 10 

Total variance in trajectory data: 106.58

Conformational sampling map will be generated in
3 dimensions at a resolution of 30 points
in each dimension.

8 complementary structures will be generated.

Sampled volume: 27000.0 Ang.^3.

Coordinates of new structures in PC space:
   0  11.43   9.32  -7.34
   1 -15.97   6.44  -7.34
   2 -15.97   9.32   5.20
   3  -2.74  -7.35   8.47
   4 -15.97  -7.35  -7.34
   5  11.43   9.32   8.47
   6  -3.69   9.32   8.47
   7  11.43  -7.35  -7.34

RMSD matrix for new structures:
  0.00  2.65  3.15  3.46  3.35  2.16  2.95  2.12
  2.65  0.00  1.74  2.81  1.71  3.37  2.70  3.61
  3.15  1.74  0.00  2.60  2.87  3.64  1.89  3.20
  3.46  2.81  2.60  0.00  2.46  2.82  2.44  2.88
  3.35  1.71  2.87  2.46  0.00  3.22  3.45  3.64
  2.16  3.37  3.64  2.82  3.22  0.00  2.16  3.19
  2.95  2.70  1.89  2.44  3.45  2.16  0.00  3.57
  2.12  3.61  3.20  2.88  3.64  3.19  3.57  0.00
```

pyCoCo accepts most of the most widely-used trajectory and topology file formats (AMBER, CHARMM, GROMACS, NAMD, etc.). For a full guide to pyCoCo see [here](http://bitbucket.org/extasy-project/coco/wiki/Home).


# Running the CoCo-MD Example
The examples/CoCo-MD directory illustrates how pyCoCo can be used as part of workflow to perform enhanced sampling. In this case, we begin by running eight independent short MD simulations on alanine pentapeptide. The combined trajectory data is fed into a CoCo analysis to identify poorly sampled regions and generate eight new starting structures that populate these. These structures are then used in a new cycle of eight MD simulations, the new trajectory data is combined with the old data for a second CoCo analysis, etc. In this case ten cycles of MD/CoCo are run.

**NOTE:** This workflow requires you to have AMBER (or AMBERTOOLS) installed on your machine and have the commands *tleap* and *sander* in your path. In addition it requires the [Crossflow](https://github.com/ChrisSuess/Project-Xbow/tree/master/xbowflow) python package ('pip install xbowflow --user')


## Sequentially / Locally 

Change into the examples directory:
```
cd examples/workflow
```

Then run the example:

```
python penta_coco.py
```

The output should look like this:

```
running md cycle 0
Running CoCo...
creating new crd files...
running md cycle 1
[...]
```
After the job has completed you will see that many files have been created. In the current directory 
you will see a series of files *coco_cycle\*.log*; these are the log files from each CoCo run. In the individual rep0?/ directories are the input and
output files from each cycle of MD. The growing ensemble of structures is thus the growing set of trajectory
files (\*.ncdf).

To see how the CoCo process has performed, you can type:
```
% grep Total coco_cycle*.log
coco_cycle1.log:Total variance in trajectory data: 91.16
coco_cycle2.log:Total variance in trajectory data: 129.50
coco_cycle3.log:Total variance in trajectory data: 178.80
coco_cycle4.log:Total variance in trajectory data: 219.20
coco_cycle5.log:Total variance in trajectory data: 241.58
coco_cycle6.log:Total variance in trajectory data: 256.77
coco_cycle7.log:Total variance in trajectory data: 267.05
coco_cycle8.log:Total variance in trajectory data: 280.75
coco_cycle9.log:Total variance in trajectory data: 291.82
```
Note that the exact numbers you see will be different from these, due to variability in the MD.

To see how CoCo improves the rate of sampling, you can run the script 'penta_nococo.py'.
This runs the same workflow, but at the end of each MD cycle, instead of generating new start points by CoCo, the next MD runs just start from the final points from the last cycle:

```
% python penta_nococo.py
running md cycle 0
creating new crd files...
running md cycle 1
creating new crd files...
running md cycle 2
[...]
```
If you then run that 'grep' command again you should get
something like:
```
% grep Total nococo_cycle*.log
nococo_cycle1.log:Total variance in trajectory data: 130.92
nococo_cycle2.log:Total variance in trajectory data: 131.31
nococo_cycle3.log:Total variance in trajectory data: 130.82
nococo_cycle4.log:Total variance in trajectory data: 134.61
nococo_cycle5.log:Total variance in trajectory data: 143.01
nococo_cycle6.log:Total variance in trajectory data: 144.25
nococo_cycle7.log:Total variance in trajectory data: 156.13
nococo_cycle8.log:Total variance in trajectory data: 168.07
nococo_cycle9.log:Total variance in trajectory data: 174.18
```

Illustrating how CoCo enhances the rate at which conformational space is sampled.

## In Parallel
(coming soon)


