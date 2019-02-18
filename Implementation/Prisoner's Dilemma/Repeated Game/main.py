import numpy as np
import random
import neat
import visualise as visualise
import csv
import matplotlib.pyplot as plt
from fractions import Fraction

# Iterator used to move down the move history
hist_iterator = 3

# Moves
cooperate = 0
defect = 1

# History of moves made by the agents
history = {}

# Container to randomise play
agent_ids = []
# Container for agents
networks = {}

round_count = []

coop_move_count = 0
def_move_count = 0

total_count_coop = []
total_count_def = []
total_move_count = []

generation_count = []

with open('history.csv', mode = 'w') as output_file:
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Agent', 'Fitness', 'Move'])
    output_file.close()
    
def add_coop_move():
    global coop_move_count
    coop_move_count += 1
    
def add_def_move():
    global def_move_count
    def_move_count += 1
    
def count_generations():
    global geneation_count
    for x in range (0, 50):
        generation_count.append(x)

# Calculate payoff for round, returns number of years in the dilemma scenario
def Calculate_Payoff(agent_one_move, agent_two_action):

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

    agent_ids.clear()
    networks.clear()
    
    total_count_coop.append(coop_move_count)
    total_count_def.append(def_move_count)
    total_move_count.append(coop_move_count + def_move_count)
    
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
            for x in range (0, 50):
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
                
                round_count.append("round")
                
#                with open('history.csv', mode = 'a') as output_file:
#                        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                        writer.writerow(["Round: " + repr(len(round_count))])
#                        writer.writerow([agent.key, agent.fitness, move])
#                        writer.writerow([opponent.key, opponent.fitness, opponent_move])
#                        output_file.close()

def run():
    
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
    winner = p.run(evo_alg, 50)

    fittest_agent = stats.best_genome()
    # Print fittest agent of last round
    print('\nFittest Agent:\n{!s}'.format(fittest_agent))
    
    for p in range(len(total_move_count)):
        if (p != 0):
            total_count_coop[p] = Fraction(total_count_coop[p] / total_move_count[p]).limit_denominator()
            total_count_def[p] = Fraction(total_count_def[p] / total_move_count[p]).limit_denominator()
    
    plt.plot(generation_count, total_count_coop, label='Proportion of Cooperative Moves')
    plt.ylabel('Ratio of Moves')
    plt.xlabel('Generations')
    plt.title('Proportion of Moves - Speciation On')
    plt.plot(generation_count, total_count_def, label='Proportion of Defective Moves')
    plt.legend(loc='best')
    plt.show()
    
    visualise.plot_stats(stats, ylog=False, view=True)
    #visualise.plot_species(stats, view=True)
    
#    print(len(total_count_coop))
#    print(len(total_count_def))
#    print(len(generation_count))
#    print(*total_count_coop, sep = ", ")
#    print(*total_move_count, sep = ", ")
    
    for p in range(len(total_move_count)):
        if (p != 0):
            print("Generation: " + str(p) + " cooperate move count = " + str(total_count_coop[p]))

run()