import os
import json
import time
from utilities.RouteData import RouteData
from utilities.Problem import Problem
from GA import GeneticAlgorithm
from RS import RandomSearch
from HC import HillClimbing
from ILS import IteratedLocalSearch

def process_file(json_file_path: str, output_file_path: str):
    """
    Process a single JSON problem file, run all search algorithms, and log results.

    Args:
        json_file_path (str): Path to the input JSON file.
        output_file_path (str): Path to the output results file.
    """
    try:
        file_name = os.path.basename(json_file_path)
        with open(output_file_path, "a") as output_file:
            output_file.write(f"\n{'=' * 50}\n")
            output_file.write(f"Processing file: {file_name}\n")

            # Load and initialize RouteData and Problem
            with open(json_file_path, "r") as f:
                route_data_json = json.load(f)
            route_data = RouteData(json.dumps(route_data_json))
            problem = Problem(route_data)

            output_file.write(f"Candidate intersections: {problem.candidate_intersections}\n")
            output_file.write(f"Number of stations: {problem.number_stations}\n")

            # Run Genetic Algorithm
            output_file.write("\nTesting Genetic Algorithm...\n")
            ga_start_time = time.time()
            ga = GeneticAlgorithm(
                problem,
                population_size=200,
                generations=50,
                mutation_rate=0.2,
                crossover_rate=0.8,
                tournament_size=3
            )
            best_config_ga, best_score_ga = ga.search()
            ga_execution_time = time.time() - ga_start_time

            # Log GA Results
            output_file.write(f"GA Execution Time: {ga_execution_time:.6f} seconds\n")
            output_file.write(f"GA Best Fitness: {best_score_ga}\n")
            output_file.write(f"GA Best Solution: {best_config_ga}\n")

            # Run Random Search
            output_file.write("\nTesting Random Search...\n")
            rs_start_time = time.time()
            rs = RandomSearch(problem, num_iterations=1000)  # Fixed argument name
            best_config_rs, best_score_rs = rs.search()
            rs_execution_time = time.time() - rs_start_time

            # Log RS Results
            output_file.write(f"RS Execution Time: {rs_execution_time:.6f} seconds\n")
            output_file.write(f"RS Best Fitness: {best_score_rs}\n")
            output_file.write(f"RS Best Solution: {best_config_rs}\n")

            # Run Hill Climbing
            output_file.write("\nTesting Hill Climbing...\n")
            hc_start_time = time.time()
            hc = HillClimbing(problem)
            best_config_hc, best_score_hc = hc.search()
            hc_execution_time = time.time() - hc_start_time

            # Log HC Results
            output_file.write(f"HC Execution Time: {hc_execution_time:.6f} seconds\n")
            output_file.write(f"HC Best Fitness: {best_score_hc}\n")
            output_file.write(f"HC Best Solution: {best_config_hc}\n")

            # Run Iterated Local Search
            output_file.write("\nTesting Iterated Local Search...\n")
            ils_start_time = time.time()
            ils = IteratedLocalSearch(problem, max_iterations=50)
            best_config_ils, best_score_ils = ils.search()
            ils_execution_time = time.time() - ils_start_time

            # Log ILS Results
            output_file.write(f"ILS Execution Time: {ils_execution_time:.6f} seconds\n")
            output_file.write(f"ILS Best Fitness: {best_score_ils}\n")
            output_file.write(f"ILS Best Solution: {best_config_ils}\n")

    except Exception as e:
        with open(output_file_path, "a") as output_file:
            output_file.write(f"\nError processing file {json_file_path}: {e}\n")
        print(f"Error processing file {json_file_path}: {e}")

if __name__ == "__main__":
    # Input and Output Directories
    data_dir = "/home/gabri/Inteilligent Systems/lab2/src/input/problems/medium_small"
    json_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.json')]

    # Ensure output directory exists
    output_dir = "/home/gabri/Inteilligent Systems/lab2/src/output"
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, "lab2_results.txt")

    print(f"Found {len(json_files)} files to process.")
    print(f"Results will be written to {output_file_path}")

    # Parallel Processing of JSON Files
    use_parallel = True
    if use_parallel:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(process_file, json_file, output_file_path)
                for json_file in json_files
            ]
            for i, future in enumerate(futures):
                try:
                    future.result()
                    print(f"Processed {i + 1}/{len(json_files)} files.")
                except Exception as e:
                    print(f"Error in parallel execution for file {json_files[i]}: {e}")
    else:
        # Sequential Processing
        for index, json_file in enumerate(json_files):
            print(f"Processing {index + 1}/{len(json_files)}: {json_file}")
            process_file(json_file, output_file_path)

    print(f"All results have been written to {output_file_path}")
