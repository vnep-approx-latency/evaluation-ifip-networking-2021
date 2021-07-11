# Overview

This **Python 3** repository contains the code used in our paper **[1], [2]** to evaluate our approximation algorithm for the **Virtual Network Embedding Algorithm (VNEP) with Latency Constraints**. The implementation of our novel algorithm **FLEX** can be found in the **[vnep-approx](https://github.com/vnep-approx-latency/vnep-approx)** repository, while the theoretical results are thoroughly laid out in our Technical Report **[1]** and our shortened paper **[2]**, as published in IFIP Networking 2021 Poster Session.  

### Structure

This GitHub Organization contains three repositories which contain the functionality for solving the VNEP with latency constraints and evaluating the results: 

- **[alib](https://github.com/vnep-approx/alib)**: A library providing the basic data model and the Mixed-Integer Program for the classic multi-commodity formulation.
- **[vnep_approx](https://github.com/vnep-approx/vnep_approx)**: Provides Linear Programming formulations, specifically the one based on the DynVMP algorithm, as well as Randomized Rounding algorithms to solve the VNEP.
- **[evaluation-ifip-networking-2021](https://github.com/vnep-approx-latency/evaluation-ifip-networking-2021)**: Provides functionality for evaluating experiment artifacts to create plots to compare runtime, profits and other algorithm parameters.

### Papers

**[1]** R. Münk, M. Rost, S. Schmid, and H. Räcke. It’s Good to Relax: Fast Profit Approximation for Virtual Networks with Latency Constraints. [Technical Report arXiv:2104.09249 [cs.NI]](https://arxiv.org/abs/2104.09249), April 2021.

**[1]** R. Münk, M. Rost, H. Räcke and S. Schmid, It's Good to Relax: Fast Profit Approximation for Virtual Networks with Latency Constraints, *2021 IFIP Networking Conference (IFIP Networking)*, 2021, pp. 1-3, doi: [10.23919/IFIPNetworking52078.2021.9472197](https://ieeexplore.ieee.org/document/9472197).

# Dependencies and Requirements

The **vnep_approx** library requires Python 3.7.

The Gurobi Solver must be installed and the .../gurobi64/lib directory added to the environment variable LD_LIBRARY_PATH.

Furthermore, we use Tamaki's algorithm presented in his [paper at ESA 2017](http://drops.dagstuhl.de/opus/volltexte/2017/7880/pdf/LIPIcs-ESA-2017-68.pdf) to compute tree decompositions (efficiently). The corresponding GitHub repository [TCS-Meiji/PACE2017-TrackA](https://github.com/TCS-Meiji/PACE2017-TrackA) must be cloned locally and the environment variable **PACE_TD_ALGORITHM_PATH** must be set to point the location of the repository: PACE_TD_ALGORITHM_PATH="$PATH_TO_PACE/PACE2017-TrackA".

For generating and executing (etc.) experiments, the environment variable ALIB_EXPERIMENT_HOME must be set to a path, such that the subfolders input/ output/ and log/ exist.

**Note**: Our source was only tested on Linux (specifically Ubuntu 14/16).  

# Installation

Install each of the **[alib](https://github.com/vnep-approx/alib)**, **[vnep_approx](https://github.com/vnep-approx/vnep_approx)** and **evaluation-ifip-networking-2021** packages using the setup script we provide. Simply execute from within each of the packages root directories: 

```
pip install -e .
```
When choosing the `-e` option, sources are not copied during the installation but the local sources are used: changes to the sources are directly reflected in the installed package.

We generally recommend installing our libraries in a virtual environment.

# Usage

It is recommended to use the given `run_samples.sh` file to execute the experiments with the necessary configuration YAML files.

```
python -m evaluation_acm_ccr_2019.cli --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...  									
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

