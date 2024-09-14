"""
Class for running optimization experiments using Random Hill Climbing (RHC), including grid search functionality.

Example usage:

    experiment_name = 'example_experiment'
    problem = TSPGenerator.generate(seed=SEED, number_of_cities=22)

    rhc = RHCRunner(problem=problem,
                    experiment_name=experiment_name,
                    output_directory=OUTPUT_DIRECTORY,
                    seed=SEED,
                    iteration_list=2 ** np.arange(10),
                    max_attempts=5000,
                    restart_list=[25, 75, 100])

    df_run_stats, df_run_curves = rhc.run()
"""

# Authors: Andrew Rollings (modified by Kyle Nakamura)
# License: BSD 3-clause

from typing import Any

import pandas as pd

import mlrose_ky
from mlrose_ky.decorators import short_name
from mlrose_ky.runners._runner_base import _RunnerBase


@short_name("rhc")
class RHCRunner(_RunnerBase):
    """
    A runner for performing optimization experiments using Random Hill Climbing (RHC).

    This class extends _RunnerBase and provides functionality for running experiments with the RHC algorithm,
    including grid search over hyperparameters such as the number of restarts.

    Attributes
    ----------
    restart_list : list[int]
        List of restart values to test in the grid search.
    """

    def __init__(
        self,
        problem: Any,
        experiment_name: str,
        seed: int,
        iteration_list: list[int],
        restart_list: list[int],
        max_attempts: int = 500,
        generate_curves: bool = True,
        **kwargs: Any,
    ):
        """
        Initialize the RHCRunner class with problem data and various experiment parameters.

        Parameters
        ----------
        problem : Any
            The optimization problem to be solved.
        experiment_name : str
            Name of the experiment.
        seed : int
            Random seed for reproducibility.
        iteration_list : list of int
            List of iterations for the experiment.
        restart_list : list of int
            List of restart values to test in the grid search.
        max_attempts : int, optional
            Maximum number of attempts without improvement before stopping.
        generate_curves : bool, optional
            Whether to generate learning curves.
        """
        super().__init__(
            problem=problem,
            experiment_name=experiment_name,
            seed=seed,
            iteration_list=iteration_list,
            max_attempts=max_attempts,
            generate_curves=generate_curves,
            **kwargs,
        )
        self.restart_list: list[int] = restart_list

    def run(self) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
        """
        Run the Random Hill Climbing (RHC) experiment.

        This method performs grid search over the provided restart values and
        returns the statistics and curves generated by the experiment.

        Returns
        -------
        tuple
            A tuple containing two DataFrames: run statistics and run curves.
        """
        return super().run_experiment_(algorithm=mlrose_ky.random_hill_climb, restarts=("Restarts", self.restart_list))
