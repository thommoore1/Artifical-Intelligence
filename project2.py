import random
import matplotlib.pyplot as plt

target = "Hello CPSC 390!"
string_length = len(target)
population_size = 128
max_generations = 1000
crossover_rate = 0.85
mutation_rate = 0.1
selection_size = 3
number_of_keeps = 3
low, high = 32, 122
nudge_prob = .7

def random_char():
    return chr(random.randint(low, high))

#Creates a random individual string of the same length as the target, made up of the chars that we are given
def random_individual():
    return "".join(random_char() for _ in range(string_length))

#Checks the fitness, adds one for each character that matches the target
def fitness(individual):
    return sum(1 for a, b in zip(individual, target) if a == b)

#Fitness based on closeness and correctness of each character. 
def fitness2(individual):
    range = high - low + 1
    total = 0
    for a, b in zip(individual, target):
        closeness = 1 - abs(ord(a) - ord(b)) / range
        total += closeness + (1 if a == b else 0)
    return total

#Selects a few random individuals, returns the fittest one
def select(population, fitnesses):
    contenders = random.sample(range(len(population)), selection_size)
    winner = max(contenders, key=lambda i: fitnesses[i])
    return population[winner]


#Crossover, where probability is crossover_rate. Each position has a 50% chance of coming from either parent. Other child gets the reamaining genes. Otherwise children are direct copies
def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        child1, child2 = [], []
        for a, b in zip(parent1, parent2):
            if random.random() < 0.5:
                child1.append(a)
                child2.append(b)
            else:
                child1.append(b)
                child2.append(a)
        return "".join(child1), "".join(child2)
    return parent1, parent2

#Mutates an individual, using mutation_rate as the chance to replace a char with any other random char
def mutate(individual):
    """Per-character mutation: with prob mutation_rate replace with a random char."""
    chars = list(individual)
    for i in range(len(chars)):
        if random.random() < mutation_rate:
            chars[i] = random_char()
    return "".join(chars)

#Starts off same as previous mutation, however, after determining a mutation, it will determine if there is a nude mutation.
#If there isn't do a normal random mutation. If there is, perform a nudged mutation.
#Nudge mutation will adjust the character by a small amount, keeping it within the valid range.
def mutate2(individual):
    chars = list(individual)
    for i in range(len(chars)):
        if random.random() < mutation_rate:
            if random.random() < nudge_prob:
                new = ord(chars[i]) + random.choice([-3, -2, -1, 1, 2, 3])
                if new < low:
                    new = high - (low - new) + 1
                elif new > high:
                    new = low + (new - high)
                chars[i] = chr(new)
            else:
                chars[i] = random_char()
    return "".join(chars)

def simulate():
    population = [random_individual() for _ in range(population_size)]
    fitnesses = [fitness(ind) for ind in population]
    best_history = [] # best fitness at every generation (index = generation)

    generation = 0
    while True:
        #Finds the best individual, creates a tuple of its string and its fitness, adds it to history
        best_idx = max(range(population_size), key=lambda i: fitnesses[i])
        best, best_fit = population[best_idx], fitnesses[best_idx]
        best_history.append(best_fit)

        #Print progress every 10 generations
        if generation % 10 == 0:
            print(f'Gen {generation:4d} | Fitness: {best_fit}/{string_length} | Best: "{best}"')

        # Stops if best is found or the generation limit has been reached
        if best == target or generation >= max_generations:
            break

        new_population = []

        # Fill the rest via selection, crossover, and mutation
        while len(new_population) < population_size:
            p1 = select(population, fitnesses)
            p2 = select(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            new_population.append(mutate(c1))
            if len(new_population) < population_size:
                new_population.append(mutate(c2))

        population = new_population
        fitnesses = [fitness(ind) for ind in population]
        generation += 1

    # Final report
    if best == target:
        print(f"Solution found in generation {generation}!")
    else:
        print(f"Generation limit reached ({max_generations}) without a perfect match.")
    print(f'Final best string: "{best}"')
    print(f"Fitness: {best_fit}/{string_length}")
    print(f"Total generations run: {generation}")
    return best_history

def simulate2():
    population = [random_individual() for _ in range(population_size)]
    fitnesses = [fitness2(ind) for ind in population]
    best_history = [] # best fitness at every generation (index = generation)

    generation = 0
    while True:
        #Finds the best individual, creates a tuple of its string and its fitness, adds it to history
        best_idx = max(range(population_size), key=lambda i: fitnesses[i])
        best = population[best_idx]
        best_fit = fitness(best)
        best_history.append(best_fit)

        #Print progress every 10 generations
        if generation % 10 == 0:
            print(f'Gen {generation:4d} | Fitness: {best_fit}/{string_length} | Best: "{best}"')

        # Stops if best is found or the generation limit has been reached
        if best == target or generation >= max_generations:
            break

        # Keep the best individuals unchanged
        ranked = sorted(range(population_size), key=lambda i: fitnesses[i], reverse=True)
        new_population = [population[i] for i in ranked[:number_of_keeps]]

        # Fill the rest via selection, crossover, and mutation
        while len(new_population) < population_size:
            p1 = select(population, fitnesses)
            p2 = select(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            new_population.append(mutate2(c1))
            if len(new_population) < population_size:
                new_population.append(mutate2(c2))

        population = new_population
        fitnesses = [fitness2(ind) for ind in population]
        generation += 1

    # Final report
    if best == target:
        print(f"Solution found in generation {generation}!")
    else:
        print(f"Generation limit reached ({max_generations}) without a perfect match.")
    print(f'Final best string: "{best}"')
    print(f"Fitness: {best_fit}/{string_length}")
    print(f"Total generations run: {generation}")
    return best_history



def plot_history(history):
    gens = list(range(1, len(history)))
    plt.figure(figsize=(8, 5))
    plt.plot(gens, history[1:], linewidth=1.5)
    plt.xscale("log")
    plt.xlabel("Generation (log scale)")
    plt.ylabel("Best Fitness")
    plt.title("Best Fitness vs. Generation")
    plt.ylim(0, string_length + 1)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig("fitness_plot.png", dpi=150)

def plot_history2(history):
    gens = list(range(1, len(history)))
    plt.figure(figsize=(8, 5))
    plt.plot(gens, history[1:], linewidth=1.5)
    plt.xscale("log")
    plt.xlabel("Generation (log scale)")
    plt.ylabel("Best Fitness")
    plt.title("Best Fitness vs. Generation")
    plt.ylim(0, string_length + 1)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig("fitness_plot2.png", dpi=150)

if __name__ == "__main__":
    history = simulate()
    plot_history(history)

    history2 = simulate2()
    plot_history2(history2)