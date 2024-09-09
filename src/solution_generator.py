
from typing import List, Tuple, Dict
from providers.openai_provider import generate_response_openai
from providers.anthropic_provider import generate_response_anthropic
from problem_parser import load_problem_by_id, evaluate_problem_solution
from problem_evaluator import evaluate_solution
import json
import ast
import re
class SolutionGenerator:
    def __init__(self, problem_id: str, agents: List[Tuple[str, str]]):
        self.problem = load_problem_by_id('../data/problems.json', problem_id)
        self.agents = agents
        self.best_solution = None
        self.best_performance = None
        self.previous_attempts = []
        
    def extract_json(self, text: str) -> Dict:
        try:
            # Find the outermost curly braces
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                json_str = match.group(0)
                # Replace newlines in the code block with escaped newlines
                json_str = re.sub(r'"""([\s\S]*?)"""', lambda m: '"{}"'.format(m.group(1).replace('\n', '\\n')), json_str)
                return json.loads(json_str)
            else:
                return None
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Error parsing JSON: {e}")
            return None

    def generate_solutions(self, iteration: int = 0) -> List[Dict]:
        solutions = []
        for provider, model in self.agents:
            
            if provider == 'openai':
                response = generate_response_openai(model, 1000, self._create_prompt(iteration))
                raw_solution = response.choices[0].message.content
            elif provider == 'anthropic':
                response = generate_response_anthropic(model, 1000, self._create_prompt(iteration))
                raw_solution = response.content[0].text  # Extract text from TextBlock
            else:
                raise ValueError(f"Unknown provider: {provider}")
                
            # Save the raw solution to a text file
            with open(f"solution_{provider}_{model}_{iteration}.txt", "w") as f:
                f.write(str(raw_solution))
            
            # Extract and parse the JSON
            try:
                # Find the JSON object in the raw text
                if isinstance(raw_solution, str):
                    json_data = self.extract_json(raw_solution)
                    if json_data:
                        solutions.append(json_data)
                    else:
                        print(f"No JSON object found in {provider} {model} solution")
                else:
                    print(f"Expected raw_solution to be a string but got {type(raw_solution)}")
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from {provider} {model} solution")
        
        return solutions

    def _generate_solution(self, provider: str, model: str, iteration: int) -> str:
        prompt = self._create_prompt(iteration)
        if provider == 'openai':
            response = generate_response_openai(model, 1000, prompt)
            return response.choices[0].message.content
        elif provider == 'anthropic':
            response = generate_response_anthropic(model, 1000, prompt)
            return response.content
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _create_prompt(self, iteration: int) -> str:
        base_prompt = f"""
        Problem: {self.problem['name']}
        Description: {self.problem['description']}
        Input format: {self.problem['input_format']}
        Output format: {self.problem['output_format']}
        Constraints: {', '.join(self.problem['constraints'])}
        Evaluation criteria: {', '.join(self.problem['evaluation_criteria'])}
        Time limit: {self.problem['time_limit']} seconds
        
        Please provide a Python function named 'solution' that solves this problem efficiently.
        Your solution should be optimized for {self.problem['evaluation_type']}.
        
        Format your response as a JSON object with the following structure:
        {{
            "imports": ["List of import statements used by the solution"],
            "code": "Your Python function code here, with the main function named 'solution'",
            "explanation": "A brief explanation of the methods used",
        }}
        
        Ensure that the "code" field contains only the function definition, without any imports or additional code.
        
    The function must be named 'solution'.
        The "explanation" should be a concise summary of the approach and key algorithms used in your solution.
        The "imports" field should be a list of strings, each representing an import statement required by your solution.
        IN THIS SPECIFIC EXAMPLE; NO IMPORTS ARE ALLOWED.
        """

        if iteration == 0:
            return base_prompt
        else:
            previous_attempts_info = self._summarize_previous_attempts()
            return f"{base_prompt}\n\nPrevious attempts summary:\n{previous_attempts_info}\n\nBased on these previous attempts, please provide an improved solution."
        
    def evaluate_solutions(self, solutions: List[str]) -> List[Dict]:
        results = []
        for solution in solutions:
            try:
                parsed_solution = json.loads(solution)
                function_code = parsed_solution['code']
                # Parse the AST to check for potentially unsafe operations
                tree = ast.parse(function_code)
                if not self._is_safe_ast(tree):
                    raise ValueError("Unsafe code detected")

                # Create a temporary file to execute the code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                    temp_file.write(function_code)
                    temp_file_path = temp_file.name

                # Execute the code in a subprocess with resource limits
                result = self._execute_in_subprocess(temp_file_path, parsed_solution['imports'])

                results.append({
                    'solution': solution,
                    'performance': result,
                    'key_ideas': parsed_solution['explanation']
                })

                # Update best solution if necessary
                if self.best_performance is None or result['runtime'] < self.best_performance['runtime']:
                    self.best_solution = solution
                    self.best_performance = result

            except Exception as e:
                results.append({
                    'solution': solution,
                    'performance': {'error': str(e)},
                    'key_ideas': 'Error in execution'
                })

        self.previous_attempts.extend(results)
        return results

    def _is_safe_ast(self, tree):
        # Implement AST checking logic here
        # For example, disallow certain function calls, imports, etc.
        return True  # Placeholder implementation

    def _execute_in_subprocess(self, file_path, imports):
        allowed_modules = {'numpy', 'pandas', 'scipy'}  # Add more as needed
        for imp in imports:
            module = imp.split()[1]
            if module not in allowed_modules:
                raise ValueError(f"Import of {module} is not allowed")

        cmd = [
            'python', '-c',
            f"import sys; sys.path.append('{os.path.dirname(file_path)}'); "
            f"from {os.path.basename(file_path)[:-3]} import solution; "
            f"import json; "
            f"from problem_evaluator import evaluate_solution; "
            f"result = evaluate_solution('{self.problem['id']}', solution); "
            f"print(json.dumps(result))"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.problem['time_limit'],
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            return {'error': 'Execution timed out'}
        except subprocess.CalledProcessError as e:
            return {'error': f'Execution failed: {e.stderr}'}