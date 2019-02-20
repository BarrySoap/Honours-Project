from transitions import Machine
import random

machines = {}
played_machines = {}
ids = []

opponent_move = ''

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
        self.machine.add_transition(trigger='choose_move_cooperate', source='cooperate', dest='cooperate', 
                                    after='update_move_coop')
        self.machine.add_transition(trigger='choose_move_cooperate', source='defect', dest='cooperate', 
                                    after='update_move_coop')
        
        self.machine.add_transition(trigger='choose_move_defect', source='thinking', dest='defect', 
                                    after='update_move_def')
        self.machine.add_transition(trigger='choose_move_defect', source='cooperate', dest='defect', 
                                    after='update_move_def')
        self.machine.add_transition(trigger='choose_move_defect', source='defect', dest='defect', 
                                    after='update_move_def')
        
        self.machine.add_transition(trigger='choose_move', source='cooperate', dest='defect', 
                                    conditions = ['opponent_defected'], after='update_move_def')
        self.machine.add_transition(trigger='choose_move', source='cooperate', dest='cooperate', 
                                    conditions = ['opponent_cooperated'], after='update_move_coop')
        self.machine.add_transition(trigger='choose_move', source='defect', dest='cooperate', 
                                    conditions = ['opponent_cooperated'], after='update_move_coop')
        self.machine.add_transition(trigger='choose_move', source='defect', dest='defect', 
                                    conditions = ['opponent_defected'], after='update_move_def')
        
    def update_move_coop(self):
        print(str(self.agent_id) + ' cooperated')
        self.move = 'cooperate'
        
    def update_move_def(self):
        print(str(self.agent_id) + ' defected')
        self.move = 'defect'
        
    def opponent_defected():
        if opponent_move == 'defect':
            return True
        else:
            return False
        
    def opponent_cooperated():
        if opponent_move == 'cooperate':
            return True
        else:
            return False
        
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
        for x in range(len(machines)):
            if (len(machines) == 0):
                break
            agentOne = random.choice(ids)
            machines[agentOne].agent_id = agentOne
            ids.remove(agentOne)
            agentTwo = random.choice(ids)
            machines[agentTwo].agent_id = agentTwo
            ids.remove(agentTwo)
            
            #print(str(machines[agentOne].fitness))
            
            machines[agentOne].choose_move_cooperate()
            machines[agentTwo].choose_move_defect()
            
            machines[agentOne].fitness += calc_payoff(machines[agentOne].move, machines[agentTwo].move)
            
            #print(str(machines[agentOne].fitness))
            
            if (len(played_machines) == 0):
                played_machines[0] = machines[agentOne]
                played_machines[1] = machines[agentTwo]
            else:
                played_machines[len(played_machines)] = machines[agentOne]
                played_machines[len(played_machines)] = machines[agentTwo]
            
            machines.pop(agentOne)
            machines.pop(agentTwo)
    
        for z in range(0, 50):
            machines[z] = played_machines[z]
            ids.append(z)
        
populate_machines()
evo_alg(machines)