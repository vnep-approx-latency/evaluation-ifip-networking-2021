
# Overview

This repository contains the evaluation code.

The implementation of the respective algorithms can be found in our separate python packages: 
- **[alib](https://github.com/vnep-approx/alib)**, providing for example the data model and the Mixed-Integer Program for the classic multi-commodity formulation, as well as
- **[vnep_approx](https://github.com/vnep-approx/vnep_approx)**, providing novel Linear Programming formulations, specifically the one based on the Dyn-VMP algorithm, as well as our proposed Randomized Rounding algorithms.
- **[evaluation-ifip-networking-2021](https://github.com/vnep-approx-latency/evaluation-ifip-networking-2021)**, providing the base line LP solutions for our runtime comparison.

## Contents

- The folder **[evaluation-ifip-networking-2021](evaluation-ifip-networking-2021)** contains the actual python package, which can be easily installed using the provided setup.py. A more detailed explanation of the provided functionality can be found below.


## Papers



# Dependencies and Requirements

The **vnep_approx** library requires Python 2.7. Required python libraries: gurobipy, numpy, cPickle, networkx , matplotlib, **[alib](https://github.com/vnep-approx/alib)**, **[vnep-approx](https://github.com/vnep-approx/vnep-approx)**, and **[evaluation-ifip-networking-2018](https://github.com/vnep-approx/evaluation-ifip-networking-2018)**.  

Gurobi must be installed and the .../gurobi64/lib directory added to the environment variable LD_LIBRARY_PATH.

Furthermore, we use Tamaki's algorithm presented in his [paper at ESA 2017](http://drops.dagstuhl.de/opus/volltexte/2017/7880/pdf/LIPIcs-ESA-2017-68.pdf) to compute tree decompositions (efficiently). The corresponding GitHub repository [TCS-Meiji/PACE2017-TrackA](https://github.com/TCS-Meiji/PACE2017-TrackA) must be cloned locally and the environment variable **PACE_TD_ALGORITHM_PATH** must be set to point the location of the repository: PACE_TD_ALGORITHM_PATH="$PATH_TO_PACE/PACE2017-TrackA".

For generating and executing (etc.) experiments, the environment variable ALIB_EXPERIMENT_HOME must be set to a path, such that the subfolders input/ output/ and log/ exist.

**Note**: Our source was only tested on Linux (specifically Ubuntu 14/16).  

# Installation

To install the package, we provide a setup script. Simply execute from within evaluation_acm_ccr_2019's root directory: 

```
pip install .
```

Furthermore, if the code base will be edited by you, we propose to install it as editable:
```
pip install -e .
```
When choosing this option, sources are not copied during the installation but the local sources are used: changes to
the sources are directly reflected in the installed package.

We generally propose to install our libraries (i.e. **alib**, **vnep_approx**, **evaluation_ifip_networking_2018**) into a virtual environment.

# Usage

You may either use our code via our API by importing the library or via our command line interface:

```
python -m evaluation_acm_ccr_2019.cli --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  This command-line interface allows you to access major parts of the VNEP-
  Approx framework developed by Matthias Rost, Elias Döhne, Alexander
  Elvers, and Tom Koch. In particular, it allows to reproduce the results
  presented in the paper:

  "Parametrized Complexity of Virtual Network Embeddings: Dynamic & Linear
  Programming Approximations": Matthias Rost, Elias Döhne, Stefan Schmid.
  ACM CCR January 2019

  Note that each commands provides a help page. To access the help, simply
  type the commmand and --help.

Options:
  --help  Show this message and exit.

Commands:
  evaluate_separation_with_latencies
                                  Creates plots for the latency evaluation
  reduce_to_plotdata_rr_seplp_optdynvmp
                                  Extracts data to be plotted for the
                                  randomized rounding algorithms (using the
                                  separation LP and DynVMP)
  									
```

# Step-by-Step Manual to Reproduce Results

The following worked on Ubuntu 16.04, but depending on the operating system or Linux variant,
some minor changes might be necessary. In the following, we outline the general idea of our framework
based on the examples provided in the **[sample](sample)** folder. In fact, the steps discussed below
can all be found in the respective bash-scripts **run_sample.sh**, which can be executed after having created
the virtual environment for the project and having installed all required dependencies.


## Creating a Virtual Environment and Installing Packages

First, create and activate a novel virtual environment for python2.7. 

```
virtualenv --python=python2.7 venv  #create new virtual environment in folder venv 
source venv/bin/activate            #activate the virtual environment
```

With the virtual environment still active, install the python extensions of [Gurobi](http://www.gurobi.com/) within the
virtual environment. Note that you need to first download and install a license of Gurobi (which is free for academic use). 
```
cd ~/programs/gurobi811/linux64/    #change to the directory of gurobi
python setup.py install             #install gurobipy within (!) the virtual environment
```

Then, assuming that all packages, i.e. **alib, vnep_approx**,  and **evaluation-ifip-networking-2021** are downloaded / cloned to the same directory, simply execute the following within each of the packages' root directories:

```
pip install -e .
```


# Contact

If you have any questions, simply write a mail to robin.muenk@tum.de

