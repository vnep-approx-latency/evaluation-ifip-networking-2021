# Overview

This **Python 3** repository contains the code used in our paper **[1], [2]** to evaluate our approximation algorithm for the **Virtual Network Embedding Algorithm (VNEP) with Latency Constraints**. The implementation of our novel algorithm **FLEX** can be found in the **[vnep-approx](https://github.com/vnep-approx-latency/vnep-approx)** repository, while the theoretical results are thoroughly laid out in our Technical Report **[1]** and our shortened paper **[2]**, as published in IFIP Networking 2021 Poster Session.  

### Structure

This GitHub Organization contains three repositories which contain the functionality for solving the VNEP with latency constraints and evaluating the results: 

- **[alib](https://github.com/vnep-approx-latency/alib)**: A library providing the basic data model and the Mixed-Integer Program for the classic multi-commodity formulation.
- **[vnep_approx](https://github.com/vnep-approx-latency/vnep-approx)**: Provides Linear Programming formulations, specifically the one based on the DynVMP algorithm, as well as Randomized Rounding algorithms to solve the VNEP.
- **[evaluation-ifip-networking-2021](https://github.com/vnep-approx-latency/evaluation-ifip-networking-2021)**: Provides functionality for evaluating experiment artifacts to create plots to compare runtime, profits and other algorithm parameters.

### Papers

**[1]** R. Münk, M. Rost, S. Schmid, and H. Räcke. It’s Good to Relax: Fast Profit Approximation for Virtual Networks with Latency Constraints. [Technical Report arXiv:2104.09249 [cs.NI]](https://arxiv.org/abs/2104.09249), April 2021.

**[2]** R. Münk, M. Rost, H. Räcke and S. Schmid, It's Good to Relax: Fast Profit Approximation for Virtual Networks with Latency Constraints, *2021 IFIP Networking Conference (IFIP Networking)*, 2021, pp. 1-3, doi: [10.23919/IFIPNetworking52078.2021.9472197](https://ieeexplore.ieee.org/document/9472197).

# Dependencies and Requirements

The **vnep_approx** library requires Python 3.7.

The [Gurobi Solver](https://www.gurobi.com/) must be installed and the .../gurobi64/lib directory added to the environment variable LD_LIBRARY_PATH.

Furthermore, we use Tamaki's algorithm presented in his [paper at ESA 2017](http://drops.dagstuhl.de/opus/volltexte/2017/7880/pdf/LIPIcs-ESA-2017-68.pdf) to compute tree decompositions (efficiently). The corresponding GitHub repository [TCS-Meiji/PACE2017-TrackA](https://github.com/TCS-Meiji/PACE2017-TrackA) must be cloned locally and the environment variable **PACE_TD_ALGORITHM_PATH** must be set to point the location of the repository: PACE_TD_ALGORITHM_PATH="$PATH_TO_PACE/PACE2017-TrackA".

# Installation

Install each of the **[alib](https://github.com/vnep-approx-latency/alib)**, **[vnep_approx](https://github.com/vnep-approx-latency/vnep-approx)** and **evaluation-ifip-networking-2021** packages using the setup script we provide. Simply execute from within each of the packages root directories: 

```
pip install -e .
```
When choosing the `-e` option, sources are not copied during the installation but the local sources are used: changes to the sources are directly reflected in the installed package.

We generally recommend installing our libraries in a virtual environment.

# Usage

For generating and executing (etc.) experiments, the environment variable **ALIB_EXPERIMENT_HOME** should be set to a path, such that the subfolders input/ output/ and log/ exist. If this environment variable is not set, the current working directory is traversed upwards until a directory containing input/, output/, and log/ is found.

It is recommended to use the given `run_samples.sh` file to execute the experiments with the necessary configuration YAML files. Set the **LATENCY_FILES_HOME** environment variable to point to a folder that contains the files `latency_scenarios.yml` with the scenario configuration and `latency_execution.yml` with the execution configuration. For examples of these configuration files, see the latency_study/ folder. Then simply execute the `latency_study/run_samles.sh` script.

# Step-by-Step Manual to Reproduce Results

After having installed each of the **[alib](https://github.com/vnep-approx-latency/alib)**, **[vnep_approx](https://github.com/vnep-approx-latency/vnep-approx)** and **evaluation-ifip-networking-2021** packages, set the **ALIB_EXPERIMENT_HOME** environment variable to a folder containing the three empty folders input/, output/, and log/. Then set the **LATENCY_FILES_HOME** environment variable to point to the `/latency_study/main_evaluation` folder to reproduce the main results from **[1], [2]**. Or set it to point to `/latency_study/second_evaluation` for the second evaluation.

Then simply execute the `latency_study/run_samles.sh` script.


# Contact

If you have any questions, simply write a mail to robin.muenk@tum.de

