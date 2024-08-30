import json
import jsonschema
from problem_evaluator import evaluate_solution

def load_problems(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def validate_problems(problems, schema_path):
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    jsonschema.validate(instance=problems, schema=schema)

def get_problem_by_id(problems, problem_id):
    return next((p for p in problems if p['id'] == problem_id), None)

def evaluate_problem_solution(problem_id, solution_func):
    return evaluate_solution(problem_id, solution_func)

if __name__ == "__main__":
    problems = load_problems('data/problems.json')
    validate_problems(problems, 'problem_schema.json')
    print("Problems loaded and validated successfully.")
    
    # Example usage
    problem = get_problem_by_id(problems, 'problem_1')
    if problem:
        print(f"Problem: {problem['name']}")
        print(f"Description: {problem['description']}")
        print(f"Evaluation type: {problem['evaluation_type']}")
    else:
        print("Problem not found.")