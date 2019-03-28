# -*- coding: utf-8 -*-
"""
Class: Single-Shot Prisoner's Dilemma (Finite State Machines)
Author: Glenn Wilkie-Sullivan
Purpose: This program will run a prisoner's dilemma (https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)
         with single-shot rounds (only one round played between agents). Agents are represented as finite state machines.
         This program DOES allow the agents to play against each other.
"""

from transitions import Machine
import random
import csv
import matplotlib.pyplot as plt
from fractions import Fraction

machines = {}           # Container for finite state machines
played_machines = {}    # Container for finite state machines which have played a round (during a generation)
ids = []                # Container for the IDs of the finite state machines

opponent_num = 1        # Temporary variable to track how many opponents an agent has played against

generations = 15        # Number of generations to cycle through

generation_count = []   # List of generations (purely for visualisation purposes)

agent_fitnesses = []    # Container for agent fitnesses across generations (visualisation purposes)

coop_move_count = 0     # Tracks how many cooperative moves are made during the simulation
def_move_count = 0      # Tracks how many defective moves are made during the simulation

total_count_coop = []
total_count_def = []    # These lists contain the move_count variables, making it easier to plot on a graph
total_move_count = []

### UNCOMMENT THIS TO SERIALISE GAME LOG TO A CSV WITHIN ROOT FOLDER ###

#with open('history.csv', mode = 'w') as output_file:
#    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Agent', 'Fitness', 'Move'])
#    output_file.close()

########################################################################
    
# This method is used to append the number of generations to the generation list
def count_generations():
    global geneation_count
    for x in range (0, generations):
        generation_count.append(x)
        
# This method is used to visualise the performace of agents across generations using matplotlib
def visualise_graph(generation_count, fitnesses):
    
    plt.plot(generation_count, fitnesses)
    plt.ylabel('Fitness')
    plt.xlabel('Generations')
    plt.title('Agent Fitnesses Across Generations')
    plt.legend(loc='best')
    plt.show()
    
    for p in range(len(total_move_count)):
        total_count_coop[p] = Fraction(total_count_coop[p] / total_move_count[p]).limit_denominator()
        total_count_def[p] = Fraction(total_count_def[p] / total_move_count[p]).limit_denominator()
            
    plt.plot(generation_count, total_count_coop, label='Proportion of Cooperative Moves')
    plt.ylabel('Ratio of Moves')
    plt.xlabel('Generations')
    plt.title('Proportion of Moves')
    plt.plot(generation_count, total_count_def, label='Proportion of Defective Moves')
    plt.legend(loc='best')
    plt.show()

class Prisoner(object):
    
    fitness = 4             # Agent starting fitness
    agent_id = 0            # ID of the agent
    move = ''               # Currently chosen move of the agent
    move_history = []       # History of moves for the agent
    strategy = 0            # Temporary variable to choose strategy for the agent (tit-for-tat or random)
    
    # Define some states. 
    states = ['cooperate', 'defect']    # List of states for the agent

    def __init__(self):
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=self.states, initial=self.states[random.randrange(0, len(self.states))])
        self.machine.add_transition(trigger='choose_initial_move', source='*', dest='cooperate', 
                                    after='update_move_coop')
        self.machine.add_transition(trigger='choose_initial_move', source='*', dest='defect', 
                                    after='update_move_def')
        
        strategy = random.random()                      # Choose strategy randomly
        numOfStartingStates = random.randint(2, 10)     # Initialise an agent with 2-10 states
        
        if (strategy < 0.5):                            # 50% chance of tit-for-tat strategy
            self.machine.add_transition(trigger='choose_move', source='cooperate', dest='defect', 
                                        conditions = ['opponent_defected'], after='update_move_def')
            self.machine.add_transition(trigger='choose_move', source='cooperate', dest='cooperate', 
                                        conditions = ['opponent_cooperated'], after='update_move_coop')
            self.machine.add_transition(trigger='choose_move', source='defect', dest='cooperate', 
                                        conditions = ['opponent_cooperated'], after='update_move_coop')
            self.machine.add_transition(trigger='choose_move', source='defect', dest='defect', 
                                        conditions = ['opponent_defected'], after='update_move_def')
        else:
            for x in range(0, numOfStartingStates):     # 50% chance of random strategy
                randomState = random.random()
                
                if randomState >= 0 and randomState <= 0.25:
                    self.machine.add_transition(trigger='choose_move', source='cooperate', dest='cooperate',
                                                conditions = ['opponent_defected'], after='update_move_coop')
                    self.machine.add_transition(trigger='choose_move', source='defect', dest='cooperate',
                                                conditions = ['opponent_cooperated'], after='update_move_coop')
                elif randomState >= 0.25 and randomState <= 0.50:
                    self.machine.add_transition(trigger='choose_move', source='cooperate', dest='defect',
                                                conditions = ['opponent_defected'], after='update_move_def')
                    self.machine.add_transition(trigger='choose_move', source='defect', dest='defect',
                                                conditions = ['opponent_cooperated'], after='update_move_def')
                elif randomState >= 0.50 and randomState <= 0.75:
                    self.machine.add_transition(trigger='choose_move', source='cooperate', dest='cooperate',
                                                conditions = ['opponent_defected'], after='update_move_coop')
                    self.machine.add_transition(trigger='choose_move', source='defect', dest='defect',
                                                conditions = ['opponent_cooperated'], after='update_move_def')
                elif randomState >= 0.75 and randomState <= 1:
                    self.machine.add_transition(trigger='choose_move', source='cooperate', dest='defect',
                                                conditions = ['opponent_defected'], after='update_move_def')
                    self.machine.add_transition(trigger='choose_move', source='defect', dest='cooperate',
                                                conditions = ['opponent_cooperated'], after='update_move_coop')
        
        
    # Method purpose - if an agent cooperates, choose cooperate
    # as the current move
    def update_move_coop(self):
        global coop_move_count
        coop_move_count += 1
        #print(str(self.agent_id) + ' cooperated')
        self.move = 'cooperate'
        
    # Conversely, update the move if the agent plays defect
    def update_move_def(self):
        global def_move_count
        def_move_count += 1
        #print(str(self.agent_id) + ' defected')
        self.move = 'defect'
        
    # Boolean method to check if the opponent played defect
    # as their last move
    def opponent_defected(self):
        if self.move_history[len(self.move_history) - 1] == 'defect':
            return True
        else:
            return False
        
    # Similarly, check if the opponent played cooperate
    def opponent_cooperated(self):
        if self.move_history[len(self.move_history) - 1] == 'cooperate':
            return True
        else:
            return False
    
# Method for populating the machines list with agents
def populate_machines():
    
    for x in range(0, 50):
        ids.append(x)
        machines[x] = Prisoner()
        machines[x].agent_id = x
        
# Basic prisoner's dilemma payoff matrix method
def calc_payoff(agent_one_move, agent_two_move):
    
    # Using the chosen moves of the two agents playing against each other,
    # if agent one chooses to cooperate and agent two defects,
    # agent one gets a payoff of 0
    if (agent_one_move == 'cooperate') and (agent_two_move == 'defect'):
        return 0
    
    if (agent_one_move == 'defect') and (agent_two_move == 'defect'):
        return 2
    
    if (agent_one_move == 'cooperate') and (agent_two_move == 'cooperate'):
        return 3

    if (agent_one_move == 'defect') and (agent_two_move == 'cooperate'):
        return 5
    
def evo_alg(machines):
    global opponent_num
    
    for generation in range(0, generations):                             # Repeat simulation for set amount of generations
        print('\n' + 'Generation ' + str(generation) + ':' + '\n')       # Output current generation number
        for x in range(0, 50):                                           # For each agent in the machines list,
            print('\n' + "Round " + str(x) + '\n')                       # Output current round number,
            if (len(ids) == 0):                                          # Check if there are agents left still to play a round.
                break                                                    # if not, end the current generation.
            agentOne = random.choice(ids)                                # If there are agents still waiting to play, choose one randomly as agent one.
            machines[agentOne].agent_id = agentOne                       # Assign an applicable ID,
            machines[agentOne].fitness = 4                               # Assign a starting (reset) fitness
            ids.remove(agentOne)                                         # Make sure the agent can't be chosen again
            
            for y in range(len(machines)):
                if (len(ids) == 0):                                      # Check if there are agents left still to play a round.
                    break
                agentTwo = random.choice(ids)
                machines[agentTwo].agent_id = agentTwo                   # Repeat for the second agent.
                machines[agentTwo].fitness = 4
                ids.remove(agentTwo)
                
                if (x == 0 and generation == 0 and agentOne is not agentTwo):   # If this is the starting generation,
                    if (opponent_num == 1):                                     # and this is the agents first opponent,
                        machines[agentOne].choose_initial_move()                # Have agents play specific moves
                        if (machines[agentOne].move == 'cooperate'):
                            machines[agentTwo].move_history.append('cooperate') # Update the move history lists accordingly.
                        else:
                            machines[agentTwo].move_history.append('defect')
                        machines[agentTwo].choose_initial_move()
                        if (machines[agentTwo].move == 'cooperate'):
                            machines[agentOne].move_history.append('cooperate') # Update the move history lists accordingly.
                        else:
                            machines[agentOne].move_history.append('defect')
                        
                        opponent_num += 1
                    else:
                        machines[agentOne].choose_move()                        # Have agents choose their own move.
                        if (machines[agentOne].move == 'cooperate'):
                            machines[agentTwo].move_history.append('cooperate') # Update the move history lists accordingly.
                        else:
                            machines[agentTwo].move_history.append('defect')
                        machines[agentTwo].choose_initial_move()
                        if (machines[agentTwo].move == 'cooperate'):
                            machines[agentOne].move_history.append('cooperate') # Update the move history lists accordingly.
                        else:
                            machines[agentOne].move_history.append('defect')
                        machines[agentTwo].machine.remove_transition(trigger='choose_initial_move', source='*', dest='cooperate')   # agents don't require
                        machines[agentTwo].machine.remove_transition(trigger='choose_initial_move', source='*', dest='defect')      # the default transitions.
                        opponent_num += 1
                else:                                                       # If this isn't the starting generation,
                    machines[agentOne].choose_move()                        # have the first agent play a move (depending on strategy).
                    
                    if (machines[agentOne].move == 'cooperate'):
                        machines[agentTwo].move_history.append('cooperate') # Update the move history lists accordingly.
                    else:
                        machines[agentTwo].move_history.append('defect')
                        
                    machines[agentTwo].choose_move()                        # have the second agent play a move (depending on strategy).
                    
                    if (machines[agentTwo].move == 'cooperate'):
                        machines[agentOne].move_history.append('cooperate') # Update the move history lists accordingly.
                    else:
                        machines[agentOne].move_history.append('defect')
                        
                    opponent_num += 1
                
                machines[agentOne].fitness += calc_payoff(machines[agentOne].move, machines[agentTwo].move)     # Calculate the payoffs of both
                machines[agentTwo].fitness += calc_payoff(machines[agentTwo].move, machines[agentOne].move)     # moves and add it to the fitnesses.
                
### UNCOMMENT THIS TO SERIALISE GAME LOG TO A CSV WITHIN ROOT FOLDER ###
                
#                with open('history.csv', mode = 'a') as output_file:
#                    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                    writer.writerow(["Generation: " + repr(x)])
#                    writer.writerow([agentOne, machines[agentOne].fitness, machines[agentOne].move])
#                    writer.writerow([agentTwo, machines[agentTwo].fitness, machines[agentTwo].move])
#                    output_file.close()
                
########################################################################
                
                if (len(played_machines) == 0):                             # After the round is finished,
                    played_machines[0] = machines[agentTwo]                 # move the agents to another list.
                else:
                    played_machines[len(played_machines)] = machines[agentTwo]
                
                machines.pop(agentTwo)                                      # and make sure the current opponent can't play again.
                
            if (len(played_machines) == 1):
                played_machines[1] = machines[agentOne]
            else:
                played_machines[len(played_machines)] = machines[agentOne]
                
            machines.pop(agentOne)                                          # Make sure the first agent can't play again.
            
            for z in range(0, 50):                                          # Reset the IDs
                ids.append(z)
                
            machines = dict(played_machines)                                # Then move the agents back to the original list
            
        fitnesses = []                                                  # Reset the agent fitnesses for the current generation,
        
        total_count_coop.append(coop_move_count)
        total_count_def.append(def_move_count)
        total_move_count.append(coop_move_count + def_move_count)
    
        for a in range(0, 50):
            machines[a] = played_machines[a]                            # Move the agents back to the original machines list,
            
        for b in range(0, len(machines)):
            fitnesses.append(machines[b].fitness)                       # Then gather the fitnesses from each agent.
            
        agent_fitnesses.append(sum(fitnesses) / float(len(fitnesses)))  # Finally, calculate the mean fitness for the current generation.
        
        for z in range(0, 50):                                          # For each agent,
            add_state = random.random()                                 # initialise temporary randoms
            delete_state = random.random()                              # to check if a mutation happens.
            
            if add_state < 0.05:                                        # There is a 10% chance that an agent will be mutated.
                temp_random = random.random()
                if (temp_random <= 0.5):                                # Either add a cooperate transition or a defect transition (50% chance).
                    machines[z].machine.add_transition(trigger='choose_move', source='*', dest='cooperate', 
                            conditions = ['opponent_defected'], after='update_move_coop')
                    machines[z].machine.add_transition(trigger='choose_move', source='*', dest='cooperate', 
                            conditions = ['opponent_cooperated'], after='update_move_coop')
                else:
                    machines[z].machine.add_transition(trigger='choose_move', source='*', dest='defect', 
                            conditions = ['opponent_defected'], after='update_move_def')
                    machines[z].machine.add_transition(trigger='choose_move', source='*', dest='defect', 
                            conditions = ['opponent_cooperated'], after='update_move_def')
                
            elif delete_state < 0.05 and len(machines[z].states) is not 1:  # The other mutation that can happen is a transition being deleted.
                machines[z].states.pop(random.randrange(1, len(machines[z].states)))
        
populate_machines()
evo_alg(machines)
count_generations()
visualise_graph(generation_count, agent_fitnesses)