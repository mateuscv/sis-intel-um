from genetic_functions import *
from bokeh.plotting import figure, show

# Inicializando valores para teste:
max_weight = 100 # Peso máximo suportado pela mochila.
chromosomes = 100 # Número de cromossomos por geração.
values_weight = [[100, 20],[20, 30],[50, 10],[123, 100],[45, 20],[12,10],[5,39]] # Valor e peso de cada item.
generations = 100 # Número de gerações para evolução.

# Geração da população inicial:
p = population(chromosomes, len(values_weight))
fitness_history = [fitness_average(p, max_weight, values_weight)]

# Laço de repetição principal:
best_chromosome = [0,0]
for i in range(generations):
    p, best_chromosome = evolve(p, max_weight, values_weight, chromosomes, best_chromosome)
    fitness_history.append(fitness_average(p, max_weight, values_weight))

# Prints para teste:
enumerated_fitness_history = enumerate(fitness_history)
for index, data in enumerated_fitness_history:
   print ("Knapsack generation #" + str(index) + ", has a value of", "{:.2f}".format(data) + ".")

print("Best solution:", best_chromosome)

x = range(len(fitness_history))
y = fitness_history

p = figure(x_axis_label='x', y_axis_label='y')
p.line(x, y, line_color="red", line_width=2)
p.xaxis.axis_label = 'Gerações'
p.yaxis.axis_label = 'Fitness'
show(p)