import argparse
from src.GerrymanderingMCMC import GerrymanderingMCMC
from mpi4py import MPI
import numpy as np

default_file = "./src/data/iowa.json"

def main():
    parser = argparse.ArgumentParser(description='Use MCMC Simulation to generate districting plans and plot relevant key statistics to illustrate the possibility that a source plan was gerrymandered')
    parser.add_argument("-g", "--graph_file", default=default_file, help="A path to a potential districting plan specified in this projects proprietary json schema; defaults to ./src/data/iowa.json")
    parser.add_argument("-i", "--cooling_period", type=int, default=50, help="The number of plans you'd like to generate _before_ counting them towards your ensemble; defaults to 50")
    parser.add_argument("-r", "--rounds", type=int, default=200, help="The number of plans you'd like to generate and include in your ensemble; defaults to 200")
    parser.add_argument("-v", "--verbose", action="store_true", help="Include this flag if you'd like real-time output_json to the console")
    args = parser.parse_args()

    graph_file = args.graph_file
    cooling_period = args.cooling_period
    rounds = args.rounds
    verbose = args.verbose

    comm = MPI.COMM_WORLD
    nprocs = comm.Get_size()
    rank = comm.Get_rank()

    # Build the gerrymandering MCMC using the variables you've been provided
    mcmc = GerrymanderingMCMC(graph_file, 1, cooling_period=cooling_period, verbose=verbose)

    # Generate alternative plans
    mcmc.generate_alternative_plans(rounds)

    # Plot the data for the results of the recombinations
    mcmc.plot_data()

    # Save the data
if __name__ == "__main__":
    main()

