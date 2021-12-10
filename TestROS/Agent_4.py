#!/usr/bin/env python
# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.
# from turtlesim_enacter import TurtleSimEnacter # requires ROS
from turtlepy_enacter import TurtlePyEnacter
import random
import copy
from ressources import Interaction

class Agent:
    def __init__(self, _hedonist_table):
        """ Creating our agent """
        self.hedonist_table = _hedonist_table
        self._action = 0
        self.anticipated_outcome = None
        self.outcome_dict = {0: 0, 1: 0, 2: 0}
        self.hedo_dict = {0: 0, 1: 0, 2: 0}
        self.action_history = 0
        self.possible_action = [0, 1, 2]
        self.interaction_history = {}
        self.last_inter = None
        self.current_inter = None

    def action(self, outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self.anticipated_outcome) +
                  ", Outcome: " + str(outcome) +
                  ", Satisfaction: (anticipation: " + str(self.anticipated_outcome == outcome) +
                  ", valence: " + str(self.hedonist_table[self._action][outcome]) + ")")

        """ Computing the next action to enact """
        self.outcome_dict[self._action] = outcome
        satisfaction = self.hedonist_table[self._action][outcome]
        self.hedo_dict[self._action] = satisfaction
        # print(self.hedo_dict)
        self.last_inter = copy.deepcopy(self.current_inter)
        self.current_inter = Interaction(self._action, outcome, satisfaction)
        self.interaction_history[self.last_inter] = self.current_inter

        if self.action_history <= 3:
            if self.current_inter in self.interaction_history.keys():
                if self.interaction_history[self.current_inter].valence == 1:
                    action = self.interaction_history[self.current_inter].action
                    self.anticipated_outcome = self.outcome_dict[action]
                    if action == self._action:
                        self.action_history += 1
                        self._action = action
                        return self._action
                    else:
                        self.action_history = 0
                        self._action = action
                        return self._action
                else:
                    if self.hedo_dict[self._action] == 1:
                        self.anticipated_outcome = self.outcome_dict[self._action]
                        self.action_history += 1
                        # print("meme action")
                        return self._action
                    else:
                        # print("action maximale random")
                        maximum = max(self.hedo_dict.values())
                        # print("maximum : ", maximum)
                        action_list = [k for k,v in self.hedo_dict.items() if v == maximum]
                        # print("liste : ", action_list)
                        self._action = random.choice(action_list)
                        # print("action : ", self._action)
                        self.anticipated_outcome = self.outcome_dict[self._action]
                        self.action_history += 1
                        return self._action
            else:
                self._action = random.choice(self.possible_action)
                self.anticipated_outcome = self.outcome_dict[self._action]

        else:
            self.action_history = 0
            action_temp = copy.deepcopy(self.possible_action)
            action_temp.remove(self._action)
            action = random.choice(action_temp)
            self._action = action
            self.anticipated_outcome = self.outcome_dict[self._action]
            return self._action



class Environment1:
    """ In Environment 1, action 0 yields outcome 0, action 1 yields outcome 1 """
    def outcome(self, action):
        # return int(input("entre 0 1 ou 2"))
        if action == 0:
            return 0
        else:
            return 1


class Environment2:
    """ In Environment 2, action 0 yields outcome 1, action 1 yields outcome 0 """
    def outcome(self, action):
        if action == 0:
            return 1
        else:
            return 0


class Environment3:
    """ Environment 3 yields outcome 1 only when the agent alternates actions 0 and 1 """
    def __init__(self):
        """ Initializing Environment3 """
        self.previous_action = 0

    def outcome(self, action):
        _outcome = 1
        if action == self.previous_action:
            _outcome = 0
        self.previous_action = action
        return _outcome


# TODO Define the hedonist valance of interactions (action, outcome)
hedonist_table = [[-1, 1], [-1, 1], [1, 1]]
# TODO Choose an agent
a = Agent(hedonist_table)
# a = Agent4(hedonist_table)
# TODO Choose an environment
# e = Environment1()
# e = Environment2()
e = Environment3()
#e = TurtleSimEnacter()
# e = TurtlePyEnacter()

if __name__ == '__main__':
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    for i in range(20):
        action = a.action(outcome)
        outcome = e.outcome(action)
