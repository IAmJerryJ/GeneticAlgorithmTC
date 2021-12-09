#Runde Jia
#44434065
import random

from deap import base, creator, tools
from copy import deepcopy

import warnings
warnings.simplefilter("ignore")


# define the payoff matrix
tc1_payoffs = ((5,4),(8,0))
tc2_payoffs = ((12,11),(13,12))


# exercise 2(a)
def payoff_to_player1(player1, player2, game):
    payoff = game[player1][player2]
    return payoff

# exercise 2(b)
def next_move(player1, player2,round):
    m_depth = 2
    strat_bit = 2**(2*m_depth)
    player1_move = player1[strat_bit + round] if round < m_depth else player1[int('0b' + str(player1[-2]) + str(player2[-2]) + str(player1[-1]) + str(player2[-1]),2)]
    return player1_move


# exercise 2(c)
def process_move(player, move, m_depth):
    memory_strat_bit = 2**(2*m_depth) + m_depth
    player[memory_strat_bit],player[memory_strat_bit + 1] =  player[memory_strat_bit + 1],move


# exercise 2(d)
def score(player1, player2, m_depth, n_rounds, game): 
    score_to_player1  = 0
    for round in range(n_rounds):
        p1_move = next_move(player1,player2,round)
        p2_move = next_move(player2,player1,round)
        c_score = payoff_to_player1(p1_move, p2_move, game)
        process_move(player1,p1_move,m_depth)
        process_move(player2,p2_move,m_depth)

        score_to_player1 += c_score

    return score_to_player1

# Create the toolbox with the right parameters
def create_toolbox(num_bits):
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness = creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register('attr_bool', random.randint, 0, 1)
    toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_bool, n = num_bits)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    toolbox.register('selTournament', tools.selTournament, tournsize = 2)
    toolbox.register("evaluate", score)
    return toolbox



# This function implements the evolutionary algorithm for the game
def play_game(mem_depth, population_size, generation_size, n_rounds, game,crossing,mutating):   
    mem_depth = 2
    num_bits = 2**(2*mem_depth) + 2*mem_depth

    # Create a toolbox using the above parameter
    toolbox = create_toolbox(num_bits)

    # Seed the random number generator
    random.seed(3)

    # Create an initial population of n individuals
    population = toolbox.population(n = population_size)

    # Define probabilities of crossing and mutating
    probab_crossing, probab_mutating  = crossing,mutating  
    
    print('\nStarting the evolution process')
    
    # Evaluate the entire population    
    fitnesses = []
	# your code goes here:
	# Calculate the fitness value for each player.
	# Each player will play against every other player in the population.
	# The fitness values of a player is the total score of all games played against every other players. 
    for i in population:
        f_scores = sum([score(i,other, mem_depth, n_rounds, game) for other in population])
        fitnesses.append((f_scores,))
        i.fitness.values = (f_scores,)
    
    print('\nEvaluated', len(population), 'individuals')
 
    # Iterate through generations
    for g in range(generation_size):
        print("\n===== Generation", g)
        
        Tour = toolbox.selTournament(population,3)

        # crossing use cxTwoPoint
        gn1,gn2,gn3 = [toolbox.clone(ind) for ind in Tour]
        crossing = [gn1,gn2,gn3]
        if random.random() < probab_crossing:
            crossing1,crossing2 = random.sample([gn1,gn2,gn3],2)
            tools.cxTwoPoint(crossing1,crossing2)
            crossing.extend([crossing1,crossing2])
        
        # mutant use mutFlipBit
        generation = []
        for cross in crossing:
            if random.random() < probab_mutating:
                mutant = toolbox.clone(cross)
                tools.mutFlipBit(mutant, 0.05)
                generation.append(deepcopy(mutant))
            else:
                generation.append(deepcopy(cross))
        
        # add new generations 
        population.extend(generation)
        # calculate the fitness values 

        fitnesses = []
        for i in population:
            f_scores = sum([score(i,other, mem_depth, n_rounds, game) for other in population])
            fitnesses.append((f_scores,))
            i.fitness.values = (f_scores,) 
        # select the best 
        population = tools.selBest(population,population_size)
    
    for individual in population:
        print("The fitness value: {} the strategy: {}".format(individual.fitness.values,individual))


if __name__ == "__main__":
    mem_depth = 2
    population_size = 10
    generation_size = 5
    n_rounds = 4

    print('===================')
    print('Play the game ITC1')
    print('===================')
    play_game(mem_depth, population_size, generation_size, n_rounds, tc1_payoffs,0.5,0)

    print('\n\n===================')
    print('Play the game ITC2')
    print('===================')
    play_game(mem_depth, population_size, generation_size, n_rounds, tc2_payoffs,0.9,0.9)
