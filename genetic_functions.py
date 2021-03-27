from random import *

# Cria e retorna um cromossomo:
def chromosome(length):
    return [ randint(0, 1) for x in range(length) ]


# Cria e retorna uma população (conjunto de cromossomos):
def population(count_individual, length):
    pop = []
    for x in range(count_individual):
        pop.append(chromosome(length))
    return pop


# Avalia se o cromossomo se encaixa na mochila:
def fitness(chromosome, max_weight, values_weight): 
    
    total_weight = 0
    total_value = 0
    enumerated_chromosomes = enumerate(chromosome)

    for index, value in enumerated_chromosomes:
        total_value += (chromosome[index] * values_weight[index][0])
        total_weight += (chromosome[index] * values_weight[index][1])

    if check_weight(max_weight, total_weight):
        return total_value
    else:
        return False


# Helper da função fitness, verifica se a mochila suporta o peso do cromossomo:
def check_weight(max_weight, total_weight):
    if (max_weight - total_weight) < 0:
        return False
    else:
        return True


# Função que realiza a seleção em roleta, selecionando dois pais para a reprodução:
def roulette_wheel(parents):

    values_proto = zip(*parents)
    values_lists = list(values_proto)
    total_fitness = sum(values_lists[0])

    parent1 = pick(values_lists, total_fitness) 
    parent2 = pick(values_lists, total_fitness, parent1)

    parent1 = values_lists[1][parent1]
    parent2 = values_lists[1][parent2]
    
    return [parent1, parent2]


# Helper da função roulette_wheel, cria a "roleta" para o sorteio:
def pick(values_list, total_fitness, already_accessed_index=-1):

    wheel = []
    accumulator = 0
    picked_value = random()

    if already_accessed_index != -1:
        total_fitness -= values_list[0][already_accessed_index]

    for index, value in enumerate(values_list[0]):
        if already_accessed_index == index:
            continue
        accumulator += value
        if total_fitness == 0:
            total_fitness = 0.000001
        wheel.append(accumulator/total_fitness)
        if wheel[-1] >= picked_value:
            return index


# Função responsável pela evolução:
def evolve(pop, max_weight, values_weight, chromosomes, best_chromosome, mutate_value=0.10):

    parents = []
    for item in pop:
        if(fitness(item, max_weight, values_weight) is not False): 
            parents.append([fitness(item, max_weight, values_weight), item])

    parents.sort(reverse=True)
    if parents[0][0] > best_chromosome[0]:
        best_chromosome = parents[0]

    children = reproduce(parents, chromosomes)
    mutate(children, mutate_value)

    return children, best_chromosome


# Função para a etapa de reprodução:
def reproduce(parents, chromosomes):
    children = []
    while len(children) < chromosomes:
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
        if mutate_value > random():
            pos_to_mutate = randint(0, len(chromosome)-1)
            if chromosome[pos_to_mutate] == 1:
                chromosome[pos_to_mutate] = 0
            else:
                chromosome[pos_to_mutate] = 1


# Calcula e retorna a avaliação média da população.
def fitness_average(pop, max_weight, values_weight):
    summed = 0
    for x in pop:
        if(fitness(x, max_weight, values_weight) is not False):    
            summed += fitness(x, max_weight, values_weight)
        
    return summed / (len(pop) * 1.0)
