from transitions import Machine
import random

# Iterator used to move down the move history
hist_iterator = 3

# Moves
cooperate = 0
defect = 0

# History of moves made by the agents
history = {}

# Container to randomise play
agent_ids = []
# Container for agents
machines = {}

round_count = []

coop_move_count = 0
def_move_count = 0

total_count_coop = []
total_count_def = []
total_move_count = []

generation_count = []

class Prisoner(object):

    fitness = 4
    agent_id = 0
    
    # Define some states. 
    states = ['thinking', 'cooperate', 'defect']

    def __init__(self):
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=Prisoner.states, initial='thinking')

        self.machine.add_transition(trigger='choose_move_cooperate', source='thinking', dest='cooperate')
        self.machine.add_transition(trigger='choose_move_defect', source='thinking', dest='defect')


def populate_machines():
    for x in range(0, 50):
        machines[x] = Prisoner()
        machines[x].agent_id = x

def add_coop_move():
    global coop_move_count
    coop_move_count += 1
    
def add_def_move():
    global def_move_count
    def_move_count += 1
    
def count_generations():
    global geneation_count
    for x in range (0, 50):
        generation_count.append(x)
        
# Calculate payoff for round, returns number of years in the dilemma scenario
def Calculate_Payoff(agent_one_move, agent_two_action):

    if (agent_one_move == cooperate) and (agent_two_action == defect):
        add_coop_move()
        add_def_move()
        return 0
    
    if (agent_one_move == defect) and (agent_two_action == defect):
        add_def_move()
        add_def_move()
        return 2
    
    if (agent_one_move == cooperate) and (agent_two_action == cooperate):
        add_coop_move()
        add_coop_move()
        return 3

    if (agent_one_move == defect) and (agent_two_action == cooperate):
        add_def_move()
        add_coop_move()
        return 5
    
# Play agents against each other
def evo_alg(agents):

    total_count_coop.append(coop_move_count)
    total_count_def.append(def_move_count)
    total_move_count.append(coop_move_count + def_move_count)
    
    for agent in agents:
        
        # Add agent ids
        #agent_ids.append(agent.agent_id)
        print("")
        
    # Randomise order of play
    random.shuffle(agent_ids)

    # Play Round
    for agent_id, agent in agents:
        
        #round_count.append("round")

        for f in range(len(agents)):
            
            # Initialise opposing agent
            opponent_id, opponent = agents[f]
       
            # Based on the opposing agent's previous actions, determine move to make
            move = machines[str(agent_id)].choose_move_cooperate()
            history[str(agent_id)].append(move)

            opponent_move = machines[str(opponent_id)].choose_move_defect()
            history[str(opponent_id)].append(opponent_move)

            # Calculate new fitness
            agent.fitness += Calculate_Payoff(move, opponent_move) 
            opponent.fitness += Calculate_Payoff(opponent_move, move)
            
            print(agent.fitness)
            print(opponent.fitness)
            
            round_count.append("round")
            
def run():
    
#    batman = Prisoner()
#    print(batman.state)
#    batman.wake_up()
#    print(batman.state)
    
    populate_machines()
    evo_alg(machines)

run()