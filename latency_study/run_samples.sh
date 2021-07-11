#!/bin/bash

set -e
shopt -s nullglob

# execute this script from within the virtual environment in which these packages were installed
# -------------------------------------------------------------------------
# ------------------- EDIT EXPERIMENT PARAMETERS HERE ---------------------
# -------------------------------------------------------------------------

# export ALIB_EXPERIMENT_HOME="."

# - - - SELECT TASK - - -
NEW_SCENARIOS=true
RUN_APPROX=false
RUN_BASELINE=false
EVAL=false

# ------------------------ FOR EVALUATION ONLY -----------------------------
# - - - SPECIFY EXECUTION LATENCY PARAMETER FILTERS - - -
# will select only scenarios and executions wit the given parameters
EXCLUDE_EXEC_PARAMS="None"
# for example:
#"{'latency_approximation_limit': 10, 'latency_approximation_factor': 0.1}"
#"{'latency_approximation_type': 'strict', 'latency_approximation_limit': 10, 'latency_approximation_factor': 0.1}"

# - - - SELECT FILTER - - -
# plots are split for each value of the listed parameters
FILTER_GENERATION_PARAMS="None"
# for example:
#"['number_of_requests', 'topology']"

# -------------------------------------------------------------------------
# --------------------------------- END -----------------------------------
# -------------------------------------------------------------------------

if [ -z "${ALIB_EXPERIMENT_HOME}" ];
then
  echo "The ALIB_EXPERIMENT_HOME environment variable is not set!"
  exit 0
fi

if [ -z "${LATENCY_FILES_HOME}" ];
then
  echo "The LATENCY_FILES_HOME environment variable is not set!"
  exit 0
fi

function deletelog() {
  rm -r $ALIB_EXPERIMENT_HOME/log
  mkdir $ALIB_EXPERIMENT_HOME/log
}

function move_logs_and_output() {
	mv $ALIB_EXPERIMENT_HOME/output/* $ALIB_EXPERIMENT_HOME/input/
	deletelog
}

echo "Using latency files from: $LATENCY_FILES_HOME"
echo "Using experiment directory: $ALIB_EXPERIMENT_HOME"

function new_scenarios() {
    if [ "$NEW_SCENARIOS" = true ]
    then
      echo "Generate Scenarios"
      clear_all
      cp $LATENCY_FILES_HOME/latency_scenarios.yml $ALIB_EXPERIMENT_HOME/input/latency_scenarios.yml
      python -m vnep_approx.cli generate-scenarios scenarios.pickle $LATENCY_FILES_HOME/latency_scenarios.yml
      move_logs_and_output
    else
      echo "Skipping Scenario Generation"
    fi
}

function run_baseline() {
    if [ "$RUN_BASELINE" = true ]
    then
      echo "Run Baseline"
      python -m vnep_approx.cli start-experiment $LATENCY_FILES_HOME/baseline_execution.yml 0 10000 --concurrent 2  --overwrite_existing_intermediate_solutions --remove_intermediate_solutions
      move_logs_and_output
    else
      echo "Skipping Baseline Execution"
    fi
}

function run_approx() {
    if [ "$RUN_APPROX" = true ]
    then
      echo "Run Approx"
      python -m vnep_approx.cli start-experiment $LATENCY_FILES_HOME/latency_execution.yml 0 10000 --concurrent 8 --overwrite_existing_intermediate_solutions --remove_intermediate_solutions
      move_logs_and_output
    else
      echo "Skipping Approx Execution"
    fi
}

function reduce_baseline() {
    if [ "$RUN_BASELINE" = true ]
    then
      echo "Reduce Baseline"
      python -m evaluation_acm_ccr_2019.cli reduce_to_plotdata_rr_seplp_optdynvmp baseline_results.pickle
      move_logs_and_output
    else
      echo "Skipping Baseline Reduction"
    fi
}
function reduce_approx() {
    if [ "$RUN_APPROX" = true ]
    then
      echo "Reduce Approx"
      python -m evaluation_acm_ccr_2019.cli reduce_to_plotdata_rr_seplp_optdynvmp latency_study_results.pickle
      move_logs_and_output
    else
      echo "Skipping Approx Reduction"
    fi
}
function eval() {
    if [ "$EVAL" = true ]
      then
        echo "Evaluate"
        python -m evaluation_acm_ccr_2019.cli evaluate_separation_with_latencies baseline_results_reduced.pickle latency_study_results_reduced.pickle ./plots/ --filter_parameter_keys "$FILTER_GENERATION_PARAMS" --filter_exec_params "$EXCLUDE_EXEC_PARAMS" --output_filetype svg
        move_logs_and_output
      else
        echo "Skipping Evaluation"
    fi
}

function clear_all() {
  rm -r $ALIB_EXPERIMENT_HOME/log
  rm -r $ALIB_EXPERIMENT_HOME/input
  rm -r $ALIB_EXPERIMENT_HOME/output
  mkdir -p $ALIB_EXPERIMENT_HOME/log $ALIB_EXPERIMENT_HOME/input $ALIB_EXPERIMENT_HOME/output
  cp $LATENCY_FILES_HOME/latency_scenarios.yml $ALIB_EXPERIMENT_HOME/input/latency_scenarios.yml
  cp $LATENCY_FILES_HOME/latency_execution.yml $ALIB_EXPERIMENT_HOME/input/latency_execution.yml
}

new_scenarios
run_approx
run_baseline
reduce_approx
reduce_baseline

rm gurobi.log