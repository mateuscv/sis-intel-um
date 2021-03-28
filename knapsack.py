from genetic_functions import *
from bokeh.plotting import figure, show

# Inicializando valores para teste:
max_carry_weight = 100 # Peso máximo suportado pela mochila.
chromosomes_per_generation = 50 # Número de cromossomos por geração.
generations = 300 # Número de gerações para evolução.

# Valores e pesos iniciais dos itens que podem ser selecionados para a mochila.
# Formato: [valor, peso]
available_items_to_choose_from = [[100, 20],[20, 30],[50, 10],[123, 100],
                                  [45, 20],[12,10],[5,39]]
# Geração da população inicial:
pop = population(chromosomes_per_generation, len(available_items_to_choose_from))
fitness_history = [fitness_average(pop, max_carry_weight,
                                   available_items_to_choose_from)]
# Laço de repetição principal:
best_chromosome = [0,0] # Lista para funcionar o retorno do melhor cromossomo.
for i in range(generations):
    pop, best_chromosome = evolve(pop, max_carry_weight, 
                                  available_items_to_choose_from,
                                  chromosomes_per_generation, best_chromosome)
    fitness_history.append(fitness_average(pop, max_carry_weight,
                                           available_items_to_choose_from))
# Prints para teste:
enumerated_fitness_history = enumerate(fitness_history)
for index, data in enumerated_fitness_history:
   print ("Knapsack generation #" + str(index) + ", has a value of",
          "{:.2f}".format(data) + ".")

# Print da melhor solução encontrada:
print("Best solution:", best_chromosome)

# Plot fitness x gerações
x = range(len(fitness_history))
y = fitness_history

plot_figure = figure(x_axis_label='x', y_axis_label='y')
plot_figure.line(x, y, line_color="red", line_width=2)
plot_figure.xaxis.axis_label = 'Gerações'
plot_figure.yaxis.axis_label = 'Fitness Médio'
show(plot_figure)

