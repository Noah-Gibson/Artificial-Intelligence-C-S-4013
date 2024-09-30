import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = load_csv('./hw2/CreditCard.csv')
    df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'M' else 0)
    df['CarOwner'] = df['CarOwner'].apply(lambda x: 1 if x == 'Y' else 0)
    df['PropertyOwner'] = df['PropertyOwner'].apply(lambda x: 1 if x == 'Y' else 0)

    x = df[['Gender', 'CarOwner', 'PropertyOwner', '#Children', 'WorkPhone', 'Email_ID']].values
    y = df['CreditApprove'].values

    population_size = 10
    generations = 50
    mutation_rate = 0.1

    best_error, best_weights, errors = genetic_algorithm(x, y, population_size, generations, mutation_rate)

    plt.plot(range(len(errors)), errors, marker='o')
    plt.title('Errors vs Generations')
    plt.xlabel('Generation')
    plt.ylabel('er(w)')
    plt.grid(True)
    plt.show()

    print('Best error:')
    print(best_error)
    print('Best weights:')
    print(best_weights)


def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def initialize_population(population_size):
    return [np.random.choice([-1, 1], size=6) for _ in range(population_size)]

def estimation(x, weights):
    return np.dot(x, weights)

def error_func(x, y, weights):
    estimations = estimation(x, weights)
    return np.mean((estimations - y) ** 2)

def fitness_function(error):
    return np.exp(-error)

def select_parents(population, errors):
    fitness_scores = [fitness_function(e) for e in errors]
    fitness_sum = sum(fitness_scores)

    probabilities = [f / fitness_sum for f in fitness_scores]

    parents_idx = np.random.choice(len(population), size=2, p=probabilities)
    return population[parents_idx[0]], population[parents_idx[1]]

def crossover(parent1, parent2):
    crossover_point = len(parent1) // 2
    child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
    child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
    return child1, child2

def mutate(weights, mutation_rate):
    for i in range(len(weights)):
        if np.random.rand() < mutation_rate:
            weights[i] *= -1
    return weights

def genetic_algorithm(x, y, population_size, generations, mutation_rate):
    population = initialize_population(population_size)
    
    best_error = float('inf')
    best_weights = None
    errors = []

    for generation in range(generations):
        population_errors = [error_func(x, y, individual) for individual in population]

        min_error = min(population_errors)
        min_error_idx = population_errors.index(min_error)
        
        if min_error < best_error:
            best_error = min_error
            best_weights = population[min_error_idx]

        errors.append(best_error)

        next_population = []
        while len(next_population) < population_size:
            parent1, parent2 = select_parents(population, population_errors)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            next_population.extend([child1, child2])

        population = next_population[:population_size]

    return best_error, best_weights, errors

if __name__ == "__main__":
    main()
