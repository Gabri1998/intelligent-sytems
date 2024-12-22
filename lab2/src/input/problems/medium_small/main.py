from utilities.Problem import Problem
from RS import RandomSearch
from GA import GeneticAlgorithm
import os
if __name__ == "__main__":
    # Specify the path to the JSON file
    data_dir = "./data/"  # Adjust if needed based on your structure
    json_files = [
        "calle_condesa_de_trifaldi_albacete_500_0_candidates_18_ns_3.json",
        "calle_agustina_aroca_albacete_250_0_candidates_75_ns_7.json",
        "calle_herreros_albacete_250_1_candidates_25_ns_5.json",
        "calle_ínsula_barataria_albacete_500_0_candidates_140_ns_34.json",
        "calle_franciscanos_albacete_500_3_candidates_107_ns_8.json",
        "calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json",
        "calle_palmas_de_gran_canaria_albacete_500_2_candidates_167_ns_23.json",
        "calle_antonio_gotor_albacete_500_4_candidates_118_ns_13.json",
        "camino_de_alto_los_chorlitos_albacete_2000_4_candidates_121_ns_28.json",
        "calle_f_albacete_2000_0_candidates_25_ns_4.json"]

    # Initialize the problem
    problem = Problem(json_files)

    # Debug: Print the problem details
    print(f"Candidate intersections: {problem.candidate_intersections}")
    print(f"Number of stations: {problem.num_stations}")

    # Test Random Search
    print("\nTesting Random Search...")
    rs = RandomSearch(problem, num_iterations=1000)
    best_config_rs, best_score_rs = rs.search()
    print("Random Search Results:")
    print(f"Best Configuration: {best_config_rs}")
    print(f"Best Score: {best_score_rs}")

    # Test Genetic Algorithm
    print("\nTesting Genetic Algorithm...")
    ga = GeneticAlgorithm(problem, population_size=200, generations=50, mutation_rate=0.2, crossover_rate=0.8)
    best_config_ga, best_score_ga = ga.search()
    print("Genetic Algorithm Results:")
    print(f"Best Configuration: {best_config_ga}")
    print(f"Best Score: {best_score_ga}")