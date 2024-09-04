import json
import jsonschema
from problem_evaluator import evaluate_solution

def load_problems(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def load_problem_by_id(file_path, problem_id):
    with open(file_path, 'r') as f:
        problems = json.load(f)
        return next((p for p in problems if p['id'] == problem_id), None)
    

def validate_problem(problem, schema_path):
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    try:
        jsonschema.validate(instance=problem, schema=schema)
        print(f"Validation successful for problem {problem['id']}: {problem['name']}.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation error for problem {problem['id']} - {problem['name']}: {e.message}")
        raise
    except jsonschema.exceptions.SchemaError as e:
        print(f"Schema error for problem {problem['id']} - {problem['name']}: {e.message}")
        raise
    except Exception as e:
        print(f"Unexpected error during validation of problem {problem['id']} - {problem['name']}: {e}")
        raise

def evaluate_problem_solution(problem_id, solution_func):
    return evaluate_solution(problem_id, solution_func)

if __name__ == "__main__":
    problem_id = 'problem_1'
    problem = load_problem_by_id('data/problems.json', problem_id)
    
    if problem:
        validate_problem(problem, 'schemas/problem_schema.json')
        print("Problem loaded and validated successfully.")
        print(f"Problem: {problem['name']}")
        print(f"Description: {problem['description']}")
        print(f"Evaluation type: {problem['evaluation_type']}")
    else:
        print("Problem not found.")