from transitions import Machine
import random

machines = {}
ids = []

class Prisoner(object):

    fitness = 4
    
    # Define some states. 
    states = ['thinking', 'cooperate', 'defect']

    def __init__(self):
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=Prisoner.states, initial='thinking')

        self.machine.add_transition(trigger='choose_move_cooperate', source='thinking', dest='cooperate', 
                                    after='calc_payoff')
        self.machine.add_transition(trigger='choose_move_defect', source='thinking', dest='defect', 
                                    after='calc_payoff')
        
    def calc_payoff():
        
        
def populate_machines():
    for x in range(0, 50):
        ids.append(x)
        machines[x] = Prisoner()
        machines[x].agent_id = x
        
def evo_alg(machines):
    
    for x in range(len(machines)):
        if (len(machines) == 0):
            break
        agentOne = random.choice(ids)
        ids.remove(agentOne)
        agentTwo = random.choice(ids)
        ids.remove(agentTwo)
    
        machines[agentOne].choose_move_cooperate()
        machines[agentTwo].choose_move_defect()
        
        machines.pop(agentOne)
        machines.pop(agentTwo)
        
populate_machines()
evo_alg(machines)