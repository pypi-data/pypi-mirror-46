#!/usr/bin/env python

# ------------------------ Interaction class --------------------------------
# Description: Robot interaction manager class
# ---------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Autor: Luis Enrique Coronado Zuniga

import oldne
import time
import threading
import oldneki
import copy
            
class interaction():
    

    def __init__(self, middleware = "nanomsg",  pattern = "surveyor", debug = False,  blackboard = "sharo", method = "bt"):

        """
        Robot interaction manager class. Used mainly to send the robot behavior spcecification to the robots.

        Parameters
        ----------

        meddleware: string
            Middleware used for communication

        pattern : string
            Communication pattern used for behavior execution

        debug: bool
            Execute one goal, action or reaction without considering start a and cancel conditionals

        blackboard : string
            Blackboard selector. 

        method : string
            Behavior selector method

        """
        self.middleware = middleware
        self.pattern = pattern
        self.blackboard = blackboard
        self.method = method
        self.debug = debug
        self.goals = []
        self.reactions = []
        self.reaction_finished = True
        self.goal_finished = True

        if method == "bt":
            self.behavior_model = oldne.behavior_tree(.1, self.middleware, pattern)

    def load_program(self, folder):
        """
        Load a program from json files (goals and reactions)

        Parameters
        ----------
        folder : string
            path to the folder of the program


        Returns
        ----------
        reaction_list : list
            List of json files that represent the robot reactions

        goal_list : list
            List of json files that represent the robot goals

        """
        
        reactions_list = []
        goals_list = []
        reactions = oldne.getFiles(folder + "/reactions")
        goals = oldne.getFiles(folder + "/goals")

        for r in reactions: # Create a list of reactions
            reaction = oldne.read_json(folder + "/reactions/" + r) 
            reactions_list.append(oldne.json2dict(reaction))

        for g in goals: # Create a list of goals
            goal = oldne.read_json(folder + "/goals/" + g) 
            goals_list.append(oldne.json2dict(goal))

        self.goals = goals_list
        self.reactions = reactions_list

        return reactions_list, goals_list


    def print_tree(self,tree):
        """ Print a behavior tree

        Parameters
        ----------
        tree : string or dictionary
            Behavior tree definition to print

        """
        import json
        if type(tree) is str:
            tree_dict = rize.json2dict(tree)
            print (json.dumps(tree_dict, indent=4))
        elif type(tree) is dict:
            print (json.dumps(tree, indent=4))


    def execute(self,reactions, goals):
        self.behavior_model.set_goals(goals)
        self.behavior_model.set_reactions(reactions)
        self.behavior_model.manage()
            
            
    # Run part of code
    def runActions(self, tree):
        """
        Execute program

        Parameters
        ----------
        action : dictionary
            behavior JSON description

        """
        copy_tree = copy.deepcopy(tree)  # A deep copy is needed for do no pass by value
        self.behavior_model.execute(copy_tree)


    # -------------------------------------------------------- PYTHON oldneKI -----------------------------------       
    # ----------- to delete
   
    # ------------------------------------------------------ New action  function ------------------------------------------------------
    def new_action(self, primitives, robots, output="robot"):
        """
        Define a new action node

        Parameters
        ----------
        primitives : dictionary
            primitive or list of primitives that creates a composite action

        robot : list 
            list of robot names to execute the action
            
        Returns
        ----------
        action : dictionary
            Action description

        """

        action = oldneki.action(primitives, robots, False, output)
        return action


    # ------------------------------------------------------ New action  function ------------------------------------------------------
    def new_sequence(self, name = "main", action_list = []):
        """
        Define a sequence

        Parameters
        ----------
        name : string
            Sequence name

        Returns
        ----------
        sequence : dictionary
            JSON sequence

        """
        sequence = oldneki.sequence(action_list)
        return sequence

    def new_answer(self, yes_r, no_r, other_r):
        cond1 = oldneki.condition({"primitive":"speech","input":"yes"})
        cond2 = oldneki.condition({"primitive":"speech","input":"no"})
        se_y = oldneki.sequence([cond1,yes_r])
        se_n = oldneki.sequence([cond2,no_r])
        sel = oldneki.selector([se_y,se_n,other_r])
        return sel;
        

    def new_module(self, name = "main", action_list = [], node_type = "sequence"):
        """
        Define a module

        Parameters
        ----------
        name : string
            Sequence name

        Returns
        ----------
        sequence : dictionary
            JSON sequence

        """
        if node_type == "sequence":
            sequence = oldneki.sequence(action_list)
            return sequence
        elif node_type == "selector":
            selector = oldneki.selector(action_list)
            return selector

        elif node_type == "random":
            selector = oldneki.random_selector(action_list)
            return selector
            

    def new_reaction(self,name = "reaction", primitive = {}, action_list = [], reaction_source = "blackboard", memory = False):
        """
        Define a sequence

        Parameters
        ----------
        name : string
            Sequence name

        Returns
        ----------
        sequence : dictionary
            JSON sequence

        """
    
        cond = oldneki.condition(primitive, memory, reaction_source) 
        sequence_actions = oldneki.sequence(action_list, memory)
        l_tree = [cond, sequence_actions] 
        sequence_reaction = oldneki.sequence(l_tree, memory)

        return sequence_reaction


    def new_goal(self, name = "goal", activation = {}, cancelation = {}, time_number = 1, time_format = "seconds", action_list = []):
        """
        Define a goal

        Returns
        ----------
        sequence : dictionary
            JSON sequence

        """

        #if time_number == 0:
            
            #cond = oldneki.condition(activation, True,  "blackboard",) 
            #sequence_actions = oldneki.sequence(action_list, False)
            #l_tree = [cond, sequence_actions] 
            #sequence_reaction = oldneki.sequence(l_tree, True)

            #sequence_reaction = self.new_reaction("reaction",activation,action_list, False)
           
            #return sequence_reaction
        #else:

        goal_primitive = {'primitive': 'goal_check', 'input': name, "options":{"time":time_number ,"time_format":time_format}}

        cond = oldneki.condition(activation, False, "blackboard") 
        sequence_actions = oldneki.sequence(action_list, False)
        l_tree = [cond, sequence_actions] 
        sequence_reaction = oldneki.sequence(l_tree, False)


        #reaction_start = self.new_reaction("reaction", activation, action_list, False) 
        cond_stop = oldneki.condition(cancelation, True, "blackboard")
        cond_negado =  oldneki.negation([cond_stop],True)
        cond_goal = oldneki.condition(goal_primitive, False, "goal") 

        set_goal_time = self.new_action({"primitive":"goal_time", "input":name, "options":{"time":time_number ,"time_format":time_format}},"pepper","blackboard" ) #Temporal
        cond_stop_del = oldneki.condition(cancelation, False, "blackboard", "any", "forgot")
        ss_ = [set_goal_time,cond_stop_del] 
        seq_del =  oldneki.sequence(ss_, False)
        jeje = oldneki.always_failure([seq_del],False)
        reaction_stop = oldneki.selector([cond_negado,jeje])


        lista1 = [cond_goal,reaction_stop,sequence_reaction,set_goal_time, cond_stop_del]
        #lista2 = [sequence_reaction,set_goal_time]

        selector_actions1 = oldneki.sequence(lista1, False)
        #selector_actions2 = oldneki.sequence(lista2, False)

        #selector_actions3 =  oldneki.sequence([selector_actions1,selector_actions2], False)

        return selector_actions1
            



    def new_until_detected(self,name = "reaction", primitive = {}, while_list = [], do_list = [], reaction_source = "internal"):
        """
        Define a sequence

        Parameters
        ----------
        name : string
            Sequence name

        Returns
        ----------
        sequence : dictionary
            JSON sequence

        """
    
        cond = oldneki.condition(primitive, reaction_source) 
        sequence_while = oldneki.always_failure([oldneki.sequence(while_list)])
        sequence_do = oldneki.sequence(do_list)
        
        l_tree = [cond, sequence_do] 
        sequence_reaction = oldneki.sequence(l_tree)
        selector_reaction = oldneki.until_success([oldneki.selector([sequence_reaction,sequence_while])])

        return selector_reaction
        


if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
