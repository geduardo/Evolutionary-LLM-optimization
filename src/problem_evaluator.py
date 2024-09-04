import numpy as np
import time

def evaluate_matrix_inversion(solution_func):
    # Generate a random 10000x10000 invertible matrix
    matrix = np.random.rand(1000, 1000)
    matrix = np.dot(matrix, matrix.transpose())  # Ensure it's invertible

    start_time = time.time()
    result = solution_func(matrix)
    end_time = time.time()

    runtime = end_time - start_time

    # Check accuracy
    true_inverse = np.linalg.inv(matrix)
    relative_error = np.max(np.abs((result - true_inverse) / true_inverse))

    return {
        "runtime": runtime,
        "accuracy": relative_error,
        "passed": relative_error <= 1e-6 and runtime <= 300
    }

def evaluate_integer_sorting(solution_func):
    # Generate 10 million random 64-bit integers
    arr = np.random.randint(np.iinfo(np.int64).min, np.iinfo(np.int64).max, size=10_000_000, dtype=np.int64)

    start_time = time.time()
    result = solution_func(arr)
    end_time = time.time()

    runtime = end_time - start_time

    # Check correctness
    is_sorted = np.all(result[:-1] <= result[1:])

    return {
        "runtime": runtime,
        "is_sorted": is_sorted,
        "passed": is_sorted and runtime <= 60
    }

def evaluate_solution(problem_id, solution_func):
    if problem_id == "problem_1":
        return evaluate_matrix_inversion(solution_func)
    elif problem_id == "problem_2":
        return evaluate_integer_sorting(solution_func)
    else:
        raise ValueError(f"Unknown problem ID: {problem_id}")