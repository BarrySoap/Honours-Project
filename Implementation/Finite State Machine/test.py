from transitions import Machine
import random

machines = {}
ids = []
generations = 50

class Prisoner(object):

    fitness = 4
    agent_id = 0
    move = ''
    
    # Define some states. 
    states = ['thinking', 'cooperate', 'defect']

    def __init__(self):
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=Prisoner.states, initial='thinking')

        self.machine.add_transition(trigger='choose_move_cooperate', source='thinking', dest='cooperate', 
                                    after='update_move_coop')
        self.machine.add_transition(trigger='choose_move_defect', source='thinking', dest='defect', 
                                    after='update_move_def')
        
    def update_move_coop(self):
        self.move = 'cooperate'
        
    def update_move_def(self):
        self.move = 'defect'
        
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
    
    for generation in range(0, generations):
        for x in range(len(machines)):
            if (len(machines) == 0):
                break
            agentOne = random.choice(ids)
            ids.remove(agentOne)
            
            for y in range(len(machines)):
                agentTwo = random.choice(ids)
                ids.remove(agentTwo)
                
                #print(str(machines[agentOne].fitness))
                
                machines[agentOne].choose_move_cooperate()
                machines[agentTwo].choose_move_defect()
                
                machines[agentOne].fitness += calc_payoff(machines[agentOne].move, machines[agentTwo].move)
                machines[agentTwo].fitness += calc_payoff(machines[agentTwo].move, machines[agentOne].move)
                
                #print(str(machines[agentOne].fitness))
                
                machines.pop(agentOne)
                machines.pop(agentTwo)
        
populate_machines()
evo_alg(machines)