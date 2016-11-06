import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    valid_directions = [None, 'forward', 'left', 'right']
    lights = ['green','red']
    Qlist={}
    rememberedstate = ()
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        valid_directns = ['None', 'forward', 'left', 'right']
        lts = ['green','red']
        global Qlist 
        Qlist={}
        for actn in valid_directns:
            for waypt in valid_directns:
                for colr in lts:
                    for lft in valid_directns:
                        for oncing in valid_directns:
                            for rt in valid_directns:
                                Qlist[actn,''.join([waypt,colr,lft,oncing,rt])]=random.random()-0.2

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        directions = [None, 'forward', 'left', 'right']        
        def nunstring(entry):
            if entry == None:
                return 'None'
            return entry
        
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        inputstring =''.join([nunstring(self.next_waypoint),nunstring(inputs.get('light')),nunstring(inputs.get('left')),nunstring(inputs.get('oncoming')),nunstring(inputs.get('right'))])
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (self.next_waypoint, inputs)
        
        # TODO: Select action according to your policy
        keptact = None
        bestreward = 0
        global Qlist
        #print Qlist.get((nunstring(action), inputstring))
        for a in directions:
            if Qlist.get((nunstring(a), inputstring))>bestreward:
                bestreward = Qlist.get((nunstring(a), inputstring))
                keptact = a
        global rememberedstate
        rememberedstate = (nunstring(keptact), inputstring)
        action = keptact
        print rememberedstate

        # Execute action and get reward        
        #print ''.join([nunstring(self.next_waypoint),nunstring(inputs.get('light')),nunstring(inputs.get('left')),nunstring(inputs.get('oncoming')),nunstring(inputs.get('right'))])
        reward = self.env.act(self, action)
        #print ''.join([nunstring(self.next_waypoint),nunstring(inputs.get('light')),nunstring(inputs.get('left')),nunstring(inputs.get('oncoming')),nunstring(inputs.get('right'))])
        

        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
