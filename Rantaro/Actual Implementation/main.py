# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:03:30 2018

@author: Glenn Wilkie-Sullivan
"""

import neat

_strategy = 3
_opponents = 49 # how many opponents for a network to play? (population size - 1)
_cooperate = 1
_defect = 0
_history = {}

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config')
p = neat.Population(config)

def evo_alg(networks, config):
    for network_id_one, playerOne in networks:
        playerOne.fitness = 4.0
        allNets = neat.nn.FeedForwardNetwork.create(playerOne, config)
        for network_id_two, playerTwo in networks:
            playerTwo.fitness = 4.0
            allNets.activate(cooperate, defect)
            # Play one network against another, for each in the network
            # Ping one neuron as the move, how do they decide?
            # Update payoffs according to result
    # Tally payoffs into new fitness

def run():
    print("w")
    # Only gets the fittest network, need to have a roulette wheel
    # selection for the next generation
    winner = p.run(evo_alg, 200)
    # Get fitness of all networks

if __name__ == '__main__':
    run()