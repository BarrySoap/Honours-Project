# CURRENT ISSUE: Rounds are single-shot, but agents only play against one opponent. They should play against every other agent in the population. #

from transitions import Machine
import random
import csv
import matplotlib.pyplot as plt

machines = {}
played_machines = {}
ids = []

generations = 50

generation_count = []

agent_fitnesses = []

with open('history.csv', mode = 'w') as output_file:
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Agent', 'Fitness', 'Move'])
    output_file.close()
    
def count_generations():
    global geneation_count
    for x in range (0, 50):
        generation_count.append(x)
        
def visualise_graph(generation_count, fitnesses):
    
    plt.plot(generation_count, fitnesses)
    plt.ylabel('Fitness')
    plt.xlabel('Generations')
    plt.title('Agent Fitnesses Across Generations')
    plt.legend(loc='best')
    plt.show()

class Prisoner(object):

    fitness = 4
    agent_id = 0
    move = ''
    move_history = []
    strategy = 0
    
    # Define some states. 
    states = ['thinking', 'cooperate', 'defect']

    def __init__(self):
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=Prisoner.states, initial='thinking')

        self.machine.add_transition(trigger='choose_move_cooperate', source='*', dest='cooperate', 
                                    after='update_move_coop')
        self.machine.add_transition(trigger='choose_move_defect', source='*', dest='defect', 
                                    after='update_move_def')
        
        strategy = random.random()
        
        if (strategy < 0.5):
            self.machine.add_transition(trigger='choose_move', source='cooperate', dest='defect', 
                                        conditions = ['opponent_defected'], after='update_move_def')
            self.machine.add_transition(trigger='choose_move', source='cooperate', dest='cooperate', 
                                        conditions = ['opponent_cooperated'], after='update_move_coop')
            self.machine.add_transition(trigger='choose_move', source='defect', dest='cooperate', 
                                        conditions = ['opponent_cooperated'], after='update_move_coop')
            self.machine.add_transition(trigger='choose_move', source='defect', dest='defect', 
                                        conditions = ['opponent_defected'], after='update_move_def')
        else:
            self.machine.add_transition(trigger='choose_move', source='*', dest='defect', 
                                        conditions = ['random_strategy'], after='update_move_def')
            self.machine.add_transition(trigger='choose_move', source='*', dest='cooperate', 
                                        conditions = ['random_strategy'], after='update_move_coop')
        
        
    def update_move_coop(self):
        print(str(self.agent_id) + ' cooperated')
        self.move = 'cooperate'
        
    def update_move_def(self):
        print(str(self.agent_id) + ' defected')
        self.move = 'defect'
        
    def opponent_defected(self):
        #print(str(self.move_history[len(self.move_history) - 1]))
        if self.move_history[len(self.move_history) - 1] == 'defect':
            return True
        else:
            return False
        
    def opponent_cooperated(self):
        #print(str(self.move_history[len(self.move_history) - 1]))
        if self.move_history[len(self.move_history) - 1] == 'cooperate':
            return True
        else:
            return False
        
    def random_strategy(self):
        return random.random() < 0.5
        
def compare_machines_fitness(list, object):
    
    fitness_is_lower = 0
    fitness_is_higher = 0
    fitness_is_same = 0
    
    for x in range(0, len(list)):
        if (object.fitness < list[x].fitness):
            fitness_is_lower += 1
        elif (object.fitness > list[x].fitness):
            fitness_is_higher += 1
        elif (object.fitness == list[x].fitness):
            fitness_is_same += 1
    
    #print("Lower fitness: " + str(fitness_is_lower) + ", Higher fitness: " + str(fitness_is_higher) + ", Same fitness: " + str(fitness_is_same))
    return fitness_is_lower, fitness_is_higher, fitness_is_same
    
def populate_machines():
    
    for x in range(0, 50):
        ids.append(x)
        machines[x] = Prisoner()
        machines[x].agent_id = x
        
def calc_payoff(agent_one_move, agent_two_move):
    
    if (agent_one_move == 'cooperate') and (agent_two_move == 'defect'):
        return 0
    
    if (agent_one_move == 'defect') and (agent_two_move == 'defect'):
        return 2
    
    if (agent_one_move == 'cooperate') and (agent_two_move == 'cooperate'):
        return 3

    if (agent_one_move == 'defect') and (agent_two_move == 'cooperate'):
        return 5
    
def evo_alg(machines):
    
    for x in range(0, generations):
        print('\n' + 'Generation ' + str(x) + ':' + '\n')
        for y in range(len(machines)):
            if (len(machines) == 0):
                break
            agentOne = random.choice(ids)
            machines[agentOne].agent_id = agentOne
            machines[agentOne].fitness = 4
            ids.remove(agentOne)
            agentTwo = random.choice(ids)
            machines[agentTwo].agent_id = agentTwo
            machines[agentTwo].fitness = 4
            ids.remove(agentTwo)
            
            #print(str(machines[agentOne].fitness))
            
            if (x == 0):
                machines[agentOne].choose_move_cooperate()
                machines[agentTwo].move_history.append('cooperate')
                machines[agentTwo].choose_move_defect()
                machines[agentOne].move_history.append('defect')
            else:
                machines[agentOne].choose_move()
                
                if (machines[agentOne].move == 'cooperate'):
                    machines[agentTwo].move_history.append('cooperate')
                else:
                    machines[agentTwo].move_history.append('defect')
                    
                machines[agentTwo].choose_move()
                
                if (machines[agentTwo].move == 'cooperate'):
                    machines[agentOne].move_history.append('cooperate')
                else:
                    machines[agentOne].move_history.append('defect')
                    
                with open('history.csv', mode = 'a') as output_file:
                    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["Generation: " + repr(x)])
                    writer.writerow([agentOne, machines[agentOne].fitness, machines[agentOne].move])
                    writer.writerow([agentTwo, machines[agentTwo].fitness, machines[agentTwo].move])
                    output_file.close()
            
            machines[agentOne].fitness += calc_payoff(machines[agentOne].move, machines[agentTwo].move)
            machines[agentTwo].fitness += calc_payoff(machines[agentTwo].move, machines[agentOne].move)
            
            if (len(played_machines) == 0):
                played_machines[0] = machines[agentOne]
                played_machines[1] = machines[agentTwo]
            else:
                played_machines[len(played_machines)] = machines[agentOne]
                played_machines[len(played_machines)] = machines[agentTwo]
            
            machines.pop(agentOne)
            machines.pop(agentTwo)
            
        fitnesses = []
    
        for a in range(0, 50):
            machines[a] = played_machines[a]
            
        for b in range(0, len(machines)):
            fitnesses.append(machines[b].fitness)
            
        agent_fitnesses.append(sum(fitnesses) / float(len(fitnesses)))
        
        for z in range(0, 50):
            add_state = random.random()
            delete_state = random.random()
            ids.append(z)
            
            if add_state < 0.15:
                comparitive_fitness = compare_machines_fitness(machines, machines[z])
                if comparitive_fitness[0] < 25:
                    machines[z].states.append('cooperate')
                elif comparitive_fitness[0] > 25:
                    machines[z].states.append('defect')
                
            elif delete_state < 0.15 and len(machines[z].states) is not 1:
                machines[z].states.pop(random.randrange(1, len(machines[z].states)))
        
populate_machines()
evo_alg(machines)
count_generations()
visualise_graph(generation_count, agent_fitnesses)