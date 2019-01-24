from transitions import Machine
import random

class Prisoner(object):

    # Define some states. 
    states = ['Thinking', 'Cooperate', 'Defect']

    def __init__(self):
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=Prisoner.states, initial='Thinking')

        self.machine.add_transition(trigger='choose_move', source='Thinking', dest='Cooperate')
        self.machine.add_transition(trigger='choose_move', source='Thinking', dest='Defect')

    def choose_move(self):
        
        
batman = Prisoner()
print(batman.state)
batman.wake_up()
print(batman.state)