# Evolutionary-LLM-optimization

## Project Description

This project aims to leverage the knowledge and capabilities of large language models (LLMs) to solve complex optimization tasks using an evolutionary approach. By combining search-based methods, inter-agent communication, and learning, the search space can be explored to find optimal solutions.

## Key Features

* Utilizes multiple LLM instances with distinct random seeds to generate diverse solutions
* Evaluates and compiles the best solutions based on performance metrics
* Generates reports detailing the top solutions and their performance
* Reintegrates the insights and learnings into subsequent prompts for iterative optimization
* Supports various problem domains that are automatically verifiable and gradable

## Motivation

This project is inspired by the ideas outlined in the post [How Progress Is Made](https://instrumentalcomplexity.com/posts/how-progress-is-made-part-1/), which highlights the importance of combining search-based methods, generally intelligent agents, competition, collaboration, refinement, and tools in driving progress. By applying these concepts to LLMs and evolutionary algorithms, we aim to develop a powerful framework for solving complex optimization tasks efficiently.

## Code Overview

### `src/problem_parser.py`

This module is responsible for loading and validating problem definitions from a JSON file. It also provides functions to retrieve problems by ID and evaluate solutions.

### `src/problem_evaluator.py`

This module contains functions for evaluating solutions to specific problems. It includes evaluation metrics such as runtime and accuracy.

### `src/test_problem_solver.py`

This module contains test cases for the problem solver.

### `data/problems.json`

This file contains a list of problem definitions in JSON format.

### `schemas/problem_schema.json`

This file defines the JSON schema for problem definitions.

## Future Work

* Implement the core evolutionary algorithm logic.
* Integrate with LLMs for solution generation.
* Develop a reporting mechanism for tracking progress and results.
* Expand the problem domain coverage.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.