import numpy as np
import random
import neat
import visualise as visualise

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

# Calculate payoff for round, returns number of years in the dilemma scenario
def Calculate_Payoff(agent_one_move, agent_two_action):

    if (agent_one_move == cooperate) and (agent_two_action == defect):
        return 0
    
    if (agent_one_move == defect) and (agent_two_action == defect):
        return 2
    
    if (agent_one_move == cooperate) and (agent_two_action == cooperate):
        return 3

    if (agent_one_move == defect) and (agent_two_action == cooperate):
        return 5

# Play agents against each other
def evo_alg(agents, config):

    agent_ids.clear()
    networks.clear()
    
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
        
        agent.fitness = 4.0

        for f in range(len(agents)):
            
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
    visualise.plot_species(stats, view=True)

run()