import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    valid_directions = [None, 'forward', 'left', 'right']
    lights = ['green','red']
    traffic = ['None','other_heading']
    print traffic 
    Qlist={}
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        valid_directns = ['None', 'forward', 'left', 'right']
        lts = ['green','red']
        traffc = ['None','other_heading']
        global Qlist 
        Qlist={}
        for actn in valid_directns:
            for waypt in valid_directns:
                for colr in lts:
                    for lft in traffc:
                        for oncing in traffc:
                            for rt in traffc:
                                Qlist[actn,''.join([waypt,colr,lft,oncing,rt])]=random.random()-0.2
        print Qlist
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        def nunstring(entry):
            if entry == None:
                return 'None'
            return entry
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (self.next_waypoint, inputs)
        
        # TODO: Select action according to your policy
        # with thanks to studywolf
        #q = [self.getQ(state, a) for a in self.actions]
        #maxQ = max(q)
        #action = self.actions[maxQ]
        #return action
        
        #action = 
        #maxQ = max(Q)
        #action = self.actions[maxQ]
        #return action
        action = random.choice(self.valid_directions)
        print nunstring(action)

        # Execute action and get reward        
        reward = self.env.act(self, action)

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
