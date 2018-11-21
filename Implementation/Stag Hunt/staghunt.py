import numpy as np
import random
import neat
import visualise as visualise

# Iterator used to move down the move history
hist_iterator = 3

# Moves
hunt_stag = 0       # Cooperate
hunt_hare = 1       # Defect

# History of moves made by the agents
history = {}

# Container to randomise play
hunter_ids = []
# Container for agents
networks = {}

# Calculate payoff for round, returns number of years in the dilemma scenario
def Calculate_Payoff(hunter_one_move, hunter_two_action):

    if (hunter_one_move == hunt_stag) and (hunter_two_action == hunt_hare):
        return 0
    
    if (hunter_one_move == hunt_hare) and (hunter_two_action == hunt_hare):
        return 1
    
    if (hunter_one_move == hunt_stag) and (hunter_two_action == hunt_stag):
        return 2

    if (hunter_one_move == hunt_hare) and (hunter_two_action == hunt_stag):
        return 3

# Play agents against each other
def evo_alg(hunters, config):

    hunter_ids.clear()
    networks.clear()
    
    for hunter_id, hunter in hunters:
        # Reset agent fitness
        hunter.fitness = 4.0
        networks[str(hunter_id)] = neat.nn.FeedForwardNetwork.create(hunter, config)
        # Using the history iterator, go back in the history of moves
        # to judge the remaining agents
        history[str(hunter_id)] =  [-1] * hist_iterator
        # Add agent ids
        hunter_ids.append(hunter_id)

    # Randomise order of play
    random.shuffle(hunter_ids)

    # Play Round
    for hunter_id, hunter in hunters:
        
        hunter.fitness = 4.0

        for f in range(len(hunters)):
            
            # Initialise opposing agent
            opponent_id, opponent = hunters[f]
            # Get history of agent's moves
            agent_history = history[str(hunter_id)]      
            # Get history of opposing agent's moves
            opponent_history = history[str(opponent_id)]
       
            # Based on the opposing agent's previous actions, determine move to make
            determineMove = networks[str(hunter_id)].activate(opponent_history[-hist_iterator:])
            move = np.argmax(determineMove)
            history[str(hunter_id)].append(move)

            determineMoveOpponent = networks[str(opponent_id)].activate(agent_history[-hist_iterator:])
            opponent_move = np.argmax(determineMoveOpponent)
            history[str(opponent_id)].append(opponent_move)

            # Calculate new fitness
            hunter.fitness += Calculate_Payoff(move, opponent_move) 
            opponent.fitness += Calculate_Payoff(opponent_move, move)

def run():
    
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

    # Print fittest agent
    print('\nFittest Agent:\n{!s}'.format(winner)) # Doesn't get fittest agent, needs to be fixed.

    visualise.plot_stats(stats, ylog=False, view=True)
    #visualise.plot_species(stats, view=True)

run()