# MIT License
#
# Copyright (c) 2016-2018 Matthias Rost, Elias Doehne
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import matplotlib
matplotlib.use('Agg')

import os
import sys
import logging

import click
from . import treewidth_computation_experiments
from . import treewidth_computation_plots
from . import runtime_comparison_separation_dynvmp_vs_lp as sep_dynvmp_vs_lp
from . import plot_data, algorithm_heatmap_plots, runtime_evaluation
from alib import util
from alib import datamodel

try:
    import pickle as pickle
except ImportError:
    import pickle


def initialize_logger(filename, log_level_print, log_level_file, allow_override=False):
    log_level_print = logging.getLevelName(log_level_print.upper())
    log_level_file = logging.getLevelName(log_level_file.upper())
    util.initialize_root_logger(filename, log_level_print, log_level_file, allow_override=allow_override)

@click.group()
def cli():
    """
    This command-line interface allows you to access major parts of the VNEP-Approx framework
    developed by Matthias Rost, Elias Döhne, Alexander Elvers, and Tom Koch.
    In particular, it allows to reproduce the results presented in the paper:

    "Parametrized Complexity of Virtual Network Embeddings: Dynamic & Linear Programming Approximations": Matthias Rost, Elias Döhne, Stefan Schmid. ACM CCR January 2019

    Note that each commands provides a help page. To access the help, simply type the commmand and --help.

    """
    pass

@cli.command(short_help="Extracts data to be plotted for the latency evaluation of the randomized rounding algorithms")
@click.argument('input_pickle_file', type=click.Path())
@click.option('--output_pickle_file', type=click.Path(), default=None, help="file to write to")
@click.option('--log_level_print', type=click.STRING, default="info", help="log level for stdout")
@click.option('--log_level_file', type=click.STRING, default="debug", help="log level for log file")
def reduce_to_plotdata_rr_seplp_optdynvmp(input_pickle_file, output_pickle_file, log_level_print, log_level_file):
    """ Given a scenario solution pickle (input_pickle_file) this function extracts data
        to be plotted and writes it to --output_pickle_file. If --output_pickle_file is not
        given, a default name (derived from the input's basename) is derived.

        The input_file must be contained in ALIB_EXPERIMENT_HOME/input and the output
        will be written to ALIB_EXPERIMENT_HOME/output while the log is saved in
        ALIB_EXPERIMENT_HOME/log.
    """
    util.ExperimentPathHandler.initialize(check_emptiness_log=False, check_emptiness_output=False)
    log_file = os.path.join(util.ExperimentPathHandler.LOG_DIR,
                            "reduce_{}.log".format(os.path.basename(input_pickle_file)))
    initialize_logger(log_file, log_level_print, log_level_file)
    reducer = plot_data.RandRoundSepLPOptDynVMPCollectionResultReducer()
    reducer.reduce_randround_result_collection(input_pickle_file, output_pickle_file)




@cli.command(short_help="Create plots comparing the DynVMP runtime with and without considering latencies")
@click.argument('baseline_reduced_pickle', type=click.Path())       #pickle in ALIB_EXPERIMENT_HOME/input storing baseline results
@click.argument('with_latencies_reduced_pickle', type=click.Path())     #pickle in ALIB_EXPERIMENT_HOME/input storing randround results
@click.argument('output_directory', type=click.Path())          #path to which the result will be written
@click.option('--exclude_generation_parameters', type=click.STRING, default=None, help="generation parameters that shall be excluded. "
                                                                                       "Must ge given as python evaluable list of dicts. "
                                                                                       "Example format: \"{'number_of_requests': [20]}\"")
@click.option('--filter_parameter_keys', type=click.STRING, default=None, help="generation parameters whose values will represent filters. "
                                                                               "Must be given as string detailing a python list containing strings."
                                                                               "Example: \"['number_of_requests', 'edge_resource_factor', 'node_resource_factor']\"")
@click.option('--filter_exec_params', type=click.STRING, default=None, help="execution parameters that shall be used, dropping other options. "
                                                                                       "Must ge given as python evaluable list of dicts. "
                                                                                       "Example format: \"{'latency_approximation_type': ['flex']}\"")
@click.option('--overwrite/--no_overwrite', default=True, help="overwrite existing files?")
@click.option('--papermode/--non-papermode', default=True, help="output 'paper-ready' figures or figures containing additional statistical data?")
@click.option('--output_filetype', type=click.Choice(['png', 'pdf', 'eps', "svg"]), default="png", help="the filetype which shall be created")
@click.option('--filter_type', type=click.Choice(['strict', 'flex', 'no latencies']), default=None, help="If the solutions should be filtered for one type")
@click.option('--log_level_print', type=click.STRING, default="info", help="log level for stdout")
@click.option('--log_level_file', type=click.STRING, default="debug", help="log level for stdout")
def evaluate_separation_with_latencies( baseline_reduced_pickle,
                                         with_latencies_reduced_pickle,
                                          output_directory,
                                          exclude_generation_parameters,
                                          filter_parameter_keys,
                                          filter_exec_params,
                                          overwrite,
                                          papermode,
                                          output_filetype,
                                          filter_type,
                                          log_level_print,
                                          log_level_file):

    util.ExperimentPathHandler.initialize(check_emptiness_log=False, check_emptiness_output=False)
    log_file = os.path.join(util.ExperimentPathHandler.LOG_DIR,
                            "evaluate_pickles_{}_{}.log".format(os.path.basename(with_latencies_reduced_pickle),
                                                                os.path.basename(baseline_reduced_pickle)))
    initialize_logger(log_file, log_level_print, log_level_file, allow_override=True)

    baseline_pickle_path = os.path.join(util.ExperimentPathHandler.INPUT_DIR, baseline_reduced_pickle)
    with_lat_pickle_path = os.path.join(util.ExperimentPathHandler.INPUT_DIR, with_latencies_reduced_pickle)

    #get root logger
    logger = logging.getLogger()

    logger.info("Reading reduced baseline pickle at {}".format(baseline_pickle_path))
    baseline_results = None
    with open(baseline_pickle_path, "rb") as f:
        baseline_results = pickle.load(f, encoding='latin1')

    logger.info("Reading reduced with_latencies pickle at {}".format(with_latencies_reduced_pickle))
    with_latencies_results = None
    with open(with_lat_pickle_path, "rb") as f:
        with_latencies_results = pickle.load(f, encoding='latin1')

    logger.info("Loading algorithm identifiers and execution ids..")

    algorithm_id = "RandRoundSepLPOptDynVMPCollection"

    output_directory = os.path.normpath(output_directory)

    logger.info("Setting output path to {}".format(output_directory))

    if exclude_generation_parameters is not None:
        exclude_generation_parameters = eval(exclude_generation_parameters)

    if filter_parameter_keys is not None:
        filter_parameter_keys = eval(filter_parameter_keys)

    logger.info("Starting evaluation...")

    if exclude_generation_parameters is not None:
        exclude_generation_parameters = eval(exclude_generation_parameters)

    if filter_exec_params is not None:
        filter_exec_params = eval(filter_exec_params)


    algorithm_heatmap_plots.evaluate_latency_and_baseline (
        dc_baseline=baseline_results,
        dc_with_latencies=with_latencies_results,
        algorithm_id=algorithm_id,
        exclude_generation_parameters=exclude_generation_parameters,
        parameter_filter_keys=filter_parameter_keys,
        show_plot=False,
        save_plot=True,
        overwrite_existing_files=overwrite,
        forbidden_scenario_ids=None,
        papermode=papermode,
        maxdepthfilter=10,
        output_path=output_directory,
        output_filetype=output_filetype,
        filter_exec_params=filter_exec_params,
    )

    runtime_evaluation.evaluate_randround_runtimes_latency_study(
        dc_randround_seplp_dynvmp=with_latencies_results,
        dc_baseline=baseline_results,
        randround_seplp_algorithm_id=algorithm_id,
        exclude_generation_parameters=exclude_generation_parameters,
        parameter_filter_keys=filter_parameter_keys,
        show_plot=False,
        save_plot=True,
        overwrite_existing_files=overwrite,
        forbidden_scenario_ids=None,
        papermode=papermode,
        maxdepthfilter=2,
        output_path=output_directory,
        output_filetype=output_filetype,
        filter_exec_params=filter_exec_params,
    )

# --------------------------------------------- END ---------------------------------------------


if __name__ == '__main__':
    cli()
