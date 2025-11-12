# Intelligent Systems Course Projects

This repository contains implementations of various search algorithms and optimization techniques for artificial intelligence applications.

## Lab 1: Search Algorithms

### Implemented Algorithms
- **A\*** (AStar) - Heuristic search with optimal path finding
- **A\* Geodesic** - Geographical pathfinding variant
- **BFS** (Breadth-First Search) - Complete uninformed search
- **DFS** (Depth-First Search) - Depth-oriented uninformed search
- **GBS** (Greedy Best-First Search) - Heuristic-driven search
- **UCS** (Uniform Cost Search) - Cost-optimal uninformed search

### Project Structure
lab1/
├── search_algorithms/ # All search algorithm implementations
├── utilities/ # Core AI components
│ ├── Action.py # Action representation
│ ├── Node.py # Search node structure
│ ├── Problem.py # Problem formulation
│ ├── State.py # State representation
│ └── RouteData.py # Path data handling
├── input/ # Problem instances
│ ├── huge/ # Large-scale problems
│ ├── large/ # Large problems
│ ├── medium/ # Medium problems
│ └── small/ # Small problems
└── output/ # Algorithm results


## Lab 2: Optimization Algorithms

### Implemented Algorithms
- **GA** (Genetic Algorithm) - Evolutionary optimization
- **HC** (Hill Climbing) - Local search optimization
- **ILS** (Iterated Local Search) - Metaheuristic optimization
- **RS** (Random Search) - Stochastic optimization

### Project Structure
lab2/
├── search_algorithms/ # Optimization algorithm implementations
├── input/problems/ # Optimization problem instances
├── utilities/ # Core AI components
│ ├── huge/ # Large-scale optimization
│ ├── large/ # Large problems
│ ├── medium_small/ # Medium to small problems
│ └── small/ # Small problems
├── output/ # Optimization results
└── results.txt # Performance analysis



## Technical Implementation

### Core AI Components
- **Problem Formulation**: State space, actions, and goal testing
- **Search Nodes**: Path cost, parent tracking, and state expansion
- **Heuristic Functions**: Admissible and consistent heuristics for informed search
- **Optimization Techniques**: Local search and evolutionary approaches

### Algorithm Features
- **Complete**: Guaranteed to find a solution if it exists (BFS, UCS, A*)
- **Optimal**: Guaranteed to find best solution (A*, UCS)
- **Informed**: Uses heuristic knowledge (A*, GBS)
- **Uninformed**: No domain knowledge (BFS, DFS, UCS)
- **Stochastic**: Random elements (GA, RS)
- **Deterministic**: Predictable behaviour (HC, ILS)

## Usage

### Running Search Algorithms (Lab 1)
```bash
cd lab1/src
python main.py [algorithm] [problem_file]

**### Running Search Algorithms (Lab 1)**
cd lab2/src
python main.py [algorithm] [problem_file]






**Results Analysis**
_The repository includes comprehensive testing across problem sizes:
_
Small: Basic functionality verification

Medium: Standard performance testing

Large: Scalability assessment

Huge: Stress testing and limits evaluation

_Performance metrics include:_

Solution quality (path cost, objective value)

Computational efficiency (time, memory)

Search completeness and optimality

**Academic Context**
_This work demonstrates fundamental AI concepts:
_
Problem-solving through search

Heuristic design and evaluation

Optimization in complex spaces

Algorithm analysis and comparison

Scalability and performance trade-offs

