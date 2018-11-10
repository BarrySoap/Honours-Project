# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:03:30 2018

@author: Glenn Wilkie-Sullivan
"""

import neat
import random
import numpy as np

_strategy = 3
_opponents = 49 # how many opponents for a network to play? (population size - 1)
_cooperate = "cooperate"
_defect = "defect"
_history = {}

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config')
p = neat.Population(config)

def Calculate_Payoff(_agentOneAction, _agentTwoAction):
	if _agentOneAction == "cooperate" and _agentTwoAction == "defect":
		return 0
	if _agentOneAction == "defect" and _agentTwoAction == "defect":
		return 2
	if _agentOneAction == "cooperate" and _agentTwoAction == "cooperate":
		return 3
	if _agentOneAction == "defect" and _agentTwoAction == "cooperate":
		return 5
		
def Fitness(move, payoff):
    if payoff == 0:
        if move == C:
			return [1, 0]
        else:               
			return [0, 1]        
    else:
        if move == C:
			return [0, 1]
        else:
			return [1, 0]

def Play_Round():
	

def evo_alg(networks, config):
	ids = []
    allNets = {}

    for network_id, network in networks:
        network.fitness = 0.0
        allNets[str(network_id)] = neat.nn.FeedForwardNetwork.create(playerOne, config)
		history[str(network_id)] =  [-1] * _history
		ids.append(network_id)
	random.shuffle(ids)
	

def run():
    print("w")
    # Only gets the fittest network, need to have a roulette wheel
    # selection for the next generation
    winner = p.run(evo_alg, 200)
    # Get fitness of all networks

if __name__ == '__main__':
    run()