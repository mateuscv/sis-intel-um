from random import *

# Cria e retorna um cromossomo:
def chromosome(length):
    return [randint(0, 1) for x in range(length)]


# Cria e retorna uma população (conjunto de cromossomos):
def population(count_individual, length):
    pop = []
    for x in range(count_individual):
        pop.append(chromosome(length))
    return pop


# Avalia se o cromossomo se encaixa na mochila:
def fitness(chromosome, max_carry_weight, available_items_to_choose_from): 
    
    total_weight = 0
    total_value = 0
    enumerated_chromosomes = enumerate(chromosome)

    for index, value in enumerated_chromosomes:
        total_value += (chromosome[index] * available_items_to_choose_from[index][0])
        total_weight += (chromosome[index] * available_items_to_choose_from[index][1])

    if check_weight(max_carry_weight, total_weight):
        return total_value
    else:
        return False


# Helper da função fitness, verifica se a mochila suporta o peso do cromossomo:
def check_weight(max_carry_weight, total_weight):
    if (max_carry_weight - total_weight) < 0:
        return False
    else:
        return True


# Função que realiza a seleção em roleta, selecionando dois pais para a reprodução:
def roulette_wheel(parents):

    separated_fitness_chromosomes = zip(*parents)
    sfc_list = list(separated_fitness_chromosomes)

    total_fitness = sum(sfc_list[0])

    parent1_index = wheel_builder(sfc_list, total_fitness) 
    parent2_index = wheel_builder(sfc_list, total_fitness, parent1_index)

    parent1 = sfc_list[1][parent1_index]
    parent2 = sfc_list[1][parent2_index]
    
    return [parent1, parent2]


# Helper da função roulette_wheel, cria a "roleta" para o sorteio:
def wheel_builder(sfc_list, total_fitness, previous_parent_index=-1):

    fitness_values = sfc_list[0]

    # Anti-elitismo
    if previous_parent_index != -1:
        total_fitness -= fitness_values[previous_parent_index]
    wheel = []

    picked_value = random()
    accumulated_values = 0
    for index, value in enumerate(fitness_values):
        if previous_parent_index == index:
            continue

        accumulated_values += value

        # Anti-divisão-por-zero:
        if total_fitness == 0:
            total_fitness = 0.000000000001
        wheel.append(accumulated_values/total_fitness)

        # Se for maior que o número aleatório entre 0 e 1, retorna o índice desse pai!
        if wheel[-1] >= picked_value:
            return index


# Função responsável pela evolução:
def evolve(pop, max_carry_weight, available_items_to_choose_from, 
           chromosomes_per_generation, best_chromosome, mutate_value=0.01):

    parents = []
    for chromosome in pop:
        if(fitness(chromosome, max_carry_weight,
                   available_items_to_choose_from) is not False): 
            parents.append([fitness(chromosome, max_carry_weight,
                                     available_items_to_choose_from), chromosome])         
    parents.sort(reverse=True)
    if parents[0][0] > best_chromosome[0]:
        best_chromosome = parents[0]

    children = reproduce(parents, chromosomes_per_generation)
    mutate(children, mutate_value)

    return children, best_chromosome

# Função para a etapa de reprodução:
def reproduce(parents, chromosomes_per_generation):

    children = []
    while len(children) < chromosomes_per_generation:
        chosen_parents = roulette_wheel(parents)
        parent1 = chosen_parents[0]
        parent2 = chosen_parents[1]
        half_of_the_genes = len(parent1) // 2
        child = parent1[:half_of_the_genes] + parent2[half_of_the_genes:]
        children.append(child)
    return children

# Função para a etapa de mutação:
def mutate(children, mutate_value):

    for chromosome in children:
        if random() < mutate_value:
            pos_to_mutate = randint(0, len(chromosome)-1)
            if chromosome[pos_to_mutate] == 1:
                chromosome[pos_to_mutate] = 0
            else:
                chromosome[pos_to_mutate] = 1


# Calcula e retorna a avaliação média da população.
def fitness_average(pop, max_carry_weight, available_items_to_choose_from):

    summed = 0
    for x in pop:
        if(fitness(x, max_carry_weight, available_items_to_choose_from) is not False):    
            summed += fitness(x, max_carry_weight, available_items_to_choose_from)
        
    return summed / (len(pop) * 1.0)

