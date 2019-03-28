# -*- coding: utf-8 -*-
"""
Class: Repeated Prisoner's Dilemma (Neural Networks)
Author: Glenn Wilkie-Sullivan
Purpose: This program will run a prisoner's dilemma (https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)
         in a repeated fashion (more than one round played between agents). Agents are represented as neural networks.
         This program DOES allow the agents to play against each other.
"""

import numpy as np
import random
import neat
import visualise as visualise
import csv
import matplotlib.pyplot as plt
from fractions import Fraction

hist_iterator = 3       # Iterator used to move down the move history

cooperate = 0           # Neurons for the agents to ping if they choose
defect = 1              # a cooperate or defect move respectively

history = {}            # History of moves made by the agents

agent_ids = []          # Container for unique IDs attached to the agents

networks = {}           # Container for the agents

coop_move_count = 0     # Tracks how many cooperative moves are made during the simulation
def_move_count = 0      # Tracks how many defective moves are made during the simulation

total_count_coop = []
total_count_def = []    # These lists contain the move_count variables, making it easier to plot on a graph
total_move_count = []

round_count = []        # Container for the amount of rounds

numberOfGenerations = 50       # Modify this to change the amount of generations the simulation runs for
generation_count = []          # List of generations (purely for visualisation purposes)

### UNCOMMENT THIS TO SERIALISE GAME LOG TO A CSV WITHIN ROOT FOLDER ###

#with open('history.csv', mode = 'w') as output_file:
#    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Game/Replicant #', 'Average Fitness', 'Fitness Standard Deviation'])
#    output_file.close()
    
########################################################################
    
# This method will increment the variable tracking 
# how many cooperative moves are made
def add_coop_move():
    global coop_move_count
    coop_move_count += 1
    
# Conversely, this will increment the defect variable
def add_def_move():
    global def_move_count
    def_move_count += 1
    
# This method is used to append the number of generations to the generation list
def count_generations():
    global geneation_count
    for x in range (0, numberOfGenerations):
        generation_count.append(x)

# Basic prisoner's dilemma payoff matrix method
def Calculate_Payoff(agent_one_move, agent_two_action):

    # Using the chosen moves of the two agents playing against each other,
    # if agent one chooses to cooperate and agent two defects,
    # agent one gets a payoff of 0
    if (agent_one_move == cooperate) and (agent_two_action == defect):
        add_coop_move()
        add_def_move()
        return 0
    
    if (agent_one_move == defect) and (agent_two_action == defect):
        add_def_move()
        add_def_move()
        return 2
    
    if (agent_one_move == cooperate) and (agent_two_action == cooperate):
        add_coop_move()
        add_coop_move()
        return 3

    if (agent_one_move == defect) and (agent_two_action == cooperate):
        add_def_move()
        add_coop_move()
        return 5

# Play agents against each other
def evo_alg(agents, config):

    # Reset the game
    agent_ids.clear()
    networks.clear()
    
    # This section is purely for visualisation purposes #
    global total_count_coop
    global total_count_def
    global total_move_count
    
    if (len(total_move_count) != numberOfGenerations):
        total_count_coop.append(coop_move_count)
        total_count_def.append(def_move_count)
        total_move_count.append(coop_move_count + def_move_count)
    else:
        total_move_count = [total_count_coop[i] + total_count_def[i] for i in range(len(total_count_coop))]
    #####################################################
    
    # Reset the agents and initialise them again
    for agent_id, agent in agents:
        # Reset agent fitness
        agent.fitness = 4.0
        networks[str(agent_id)] = neat.nn.FeedForwardNetwork.create(agent, config)
        # Using the history iterator, go back in the history of moves
        # to judge the remaining agents
        history[str(agent_id)] =  [-1] * hist_iterator
        # Add agent ids
        agent_ids.append(agent_id)

    # Randomise order of play
    random.shuffle(agent_ids)

    # Play Round
    for agent_id, agent in agents:
        
        #round_count.append("round")
        
        agent.fitness = 4.0

        for f in range(len(agents)):
            
            # Change the second range value to however many round are to be played.
            for x in range (0, 20):
                # Initialise opposing agent
                opponent_id, opponent = agents[f]
                # Get history of agent's moves
                agent_history = history[str(agent_id)]      
                # Get history of opposing agent's moves
                opponent_history = history[str(opponent_id)]
                
                # Based on the opposing agent's previous actions, determine move to make
                determineMove = networks[str(agent_id)].activate(opponent_history[-hist_iterator:])
                move = np.argmax(determineMove)
                history[str(agent_id)].append(move)
                
                determineMoveOpponent = networks[str(opponent_id)].activate(agent_history[-hist_iterator:])
                opponent_move = np.argmax(determineMoveOpponent)
                history[str(opponent_id)].append(opponent_move)
                
                # Calculate new fitness
                agent.fitness += Calculate_Payoff(move, opponent_move) 
                opponent.fitness += Calculate_Payoff(opponent_move, move)
                
                ### UNCOMMENT THIS TO SERIALISE GAME LOG TO A CSV WITHIN ROOT FOLDER ###
                
#                round_count.append("round")
#                
#                with open('history.csv', mode = 'a') as output_file:
#                    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                    writer.writerow(["Round: " + repr(len(round_count))])
#                    writer.writerow([agent.key, agent.fitness, move])
#                    writer.writerow([opponent.key, opponent.fitness, opponent_move])
#                    output_file.close()
                    
                ########################################################################

def run():
    
    # Count the amount of generations
    if (len(generation_count) != numberOfGenerations):
        count_generations()
    
    # load network config
    config = neat.Config(neat.DefaultGenome, 
                        neat.DefaultReproduction, 
                        neat.DefaultSpeciesSet, 
                        neat.DefaultStagnation, 
                        'config')

    # Initialise population
    p = neat.Population(config)
  
    # add reporter to display progress in terminal
    p.add_reporter(neat.StdOutReporter(False))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for 50 generations
    winner = p.run(evo_alg, numberOfGenerations)

    fittest_agent = stats.best_genome()
    # Print fittest agent of last round
    print('\nFittest Agent:\n{!s}'.format(fittest_agent))
    
    # This section is purely for visualisation purposes #
    for p in range(len(total_move_count)):
        if (p != 0):
            total_count_coop[p] = Fraction(total_count_coop[p] / total_move_count[p]).limit_denominator()
            total_count_def[p] = Fraction(total_count_def[p] / total_move_count[p]).limit_denominator()
    
    plt.plot(generation_count, total_count_coop, label='Proportion of Cooperative Moves')
    plt.ylabel('Ratio of Moves')
    plt.xlabel('Generations')
    plt.title('Proportion of Moves - Speciation Off')
    plt.plot(generation_count, total_count_def, label='Proportion of Defective Moves')
    plt.legend(loc='best')
    plt.show()
    #####################################################
    
    # Visualise game log
    visualise.plot_stats(stats, ylog=False, view=True)
    #visualise.plot_species(stats, view=True)

run()