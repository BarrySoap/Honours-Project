# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:03:30 2018

@author: Glenn Wilkie-Sullivan
"""

import neat

cooperate = (1, 0)
defect = (0, 1)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config')
p = neat.Population(config)

#def evo_alg(networks, config):
#    for network_id, network in networks:
#        network.fitness = 4.0
#        allNets = neat.nn.FeedForwardNetwork.create(network, config)
        

def run():
    print(p.population.values())


if __name__ == '__main__':
    run()