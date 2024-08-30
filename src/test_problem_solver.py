from problem_parser import load_problems, validate_problems, get_problem_by_id, evaluate_problem_solution
import numpy as np

def test_matrix_inversion():
    # Load and validate problems
    problems = load_problems('data/problems.json')
    validate_problems(problems, 'schemas/problem_schema.json')

    # Get the matrix inversion problem
    problem = get_problem_by_id(problems, 'problem_1')
    
    if not problem:
        print("Problem not found.")
        return

    print(f"Testing problem: {problem['name']}")

    # Implement a simple solution function
    def simple_matrix_inversion(matrix):
        return np.linalg.inv(matrix)

    # Evaluate the solution
    result = evaluate_problem_solution('problem_1', simple_matrix_inversion)

    print(f"Evaluation result:")
    print(f"Runtime: {result['runtime']:.4f} seconds")
    print(f"Accuracy: {result['accuracy']:.2e}")
    print(f"Passed: {result['passed']}")

if __name__ == "__main__":
    test_matrix_inversion()