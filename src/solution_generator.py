
from typing import List, Tuple, Dict
from providers.openai_provider import generate_response_openai
from providers.anthropic_provider import generate_response_anthropic
from problem_parser import load_problem_by_id, evaluate_problem_solution

class SolutionGenerator:
    def __init__(self, problem_id: str, agents: List[Tuple[str, str]]):
        self.problem = load_problem_by_id('data/problems.json', problem_id)
        self.agents = agents
        self.best_solution = None
        self.best_performance = None
        self.previous_attempts = []

    def generate_solutions(self, iteration: int = 0) -> List[str]:
        solutions = []
        for provider, model in self.agents:
            solution = self._generate_solution(provider, model, iteration)
            solutions.append(solution)
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
        
        Please provide a Python function that solves this problem efficiently.
        Your solution should be optimized for {self.problem['evaluation_type']}.
        """

        if iteration == 0:
            return base_prompt
        else:
            previous_attempts_info = self._summarize_previous_attempts()
            return f"{base_prompt}\n\nPrevious attempts summary:\n{previous_attempts_info}\n\nBased on these previous attempts, please provide an improved solution."

    def _summarize_previous_attempts(self) -> str:
        summary = []
        for i, attempt in enumerate(self.previous_attempts):
            summary.append(f"Attempt {i+1}:")
            summary.append(f"Performance: {attempt['performance']}")
            summary.append(f"Key ideas: {attempt['key_ideas']}")
            summary.append("")
        return "\n".join(summary)

    def evaluate_solutions(self, solutions: List[str]) -> List[Dict]:
        results = []
        for solution in solutions:
            try:
                solution_func = eval(f"lambda x: {solution}")
                result = evaluate_problem_solution(self.problem['id'], solution_func)
                results.append({"solution": solution, "performance": result})
                
                if self.best_performance is None or result['runtime'] < self.best_performance['runtime']:
                    self.best_solution = solution
                    self.best_performance = result
                
                # Add to previous attempts (you may want to add a method to extract key ideas)
                self.previous_attempts.append({
                    "solution": solution,
                    "performance": result,
                    "key_ideas": "Extract key ideas from the solution"  # This needs to be implemented
                })
            except Exception as e:
                print(f"Error evaluating solution: {e}")
        return results

    def get_best_solution(self) -> Tuple[str, Dict]:
        return self.best_solution, self.best_performance

def main():
    agents = [
        ('openai', 'gpt-4'),
        ('anthropic', 'claude-2'),
        ('openai', 'gpt-3.5-turbo'),
    ]
    generator = SolutionGenerator("problem_1", agents)
    
    for iteration in range(3):  # Run for 3 iterations
        print(f"\nIteration {iteration + 1}")
        solutions = generator.generate_solutions(iteration)
        results = generator.evaluate_solutions(solutions)
        
        print("Evaluation results:")
        for i, result in enumerate(results):
            print(f"Agent {i + 1} ({agents[i][0]}, {agents[i][1]}):")
            print(f"Solution: {result['solution'][:50]}...")
            print(f"Performance: {result['performance']}")
            print()
    
    best_solution, best_performance = generator.get_best_solution()
    print("Best overall solution:")
    print(best_solution)
    print("Best performance:")
    print(best_performance)

if __name__ == "__main__":