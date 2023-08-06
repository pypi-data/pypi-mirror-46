#!/usr/bin/env python

# ------------------------ Behavior tree class --------------------------------

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Autor: Luis Enrique Coronado Zuniga

import time
import oldneki
import oldne
import copy
            

class behavior_tree():
        
    def __init__(self, tick_time = 0.1, middleware = "nanomsg", pattern="survey"):
        self.bt = oldneki.engine(middleware)
        self.tick_time = tick_time
        self.goal_times = {}

    def check_goal_time(self,id_, delay_):

    
        if id_ in self.goal_times:
            value = self.goal_times[id_]
            since = time.time() - value["time"]
            #print "delay = " + str(delay_)
            #print "since = " + str(since)

            if (int(since) >= int(delay_)):
                self.goal_times[id_] = {"time":time.time()}
                return True
            else:
                return False
        else:
            self.goal_times[id_] = {"time":time.time()}
            return True

    def set_goal_time(self,node): # Set time to the goal to wait for new execution #TODO delete
        id_ = node["id"]
        print ("Set goal new time")
        self.goal_times[id_] = time.time()
        return True

    def check_reaction_priority(self,utility):
        if self.status == "goal_running":
            if utility >= self.current_goal ["utility"]:
                return True
            else:
                return False
        return True   

    def checkActivateConditionals(self,node_type):
        if node_type == "reactions":
            for r in self.reactions:
                reaction_ok = self.check_reaction_priority(r["utility"]) # If utility of the reaction bigger that utility of the current goal 
                if reaction_ok:
                    state =  self.bt.run_condition(r["activate"]) 
                    if state == "success":
                        print ("------- Reaction activated: ------- ")
                        print "name: " + str(r["name"])
                        return "success", r
            return "failure", {}

        elif node_type == "goals":
            for g in self.goals:
                state =  self.bt.run_condition(g["activate"]) 
                if state == "success":
                    goal_ok = self.check_goal_time(g["id"], g["delay"]) # If goal can is in time
                    if goal_ok:
                        print ("------- Goal activated: ------- ")
                        print "name: " + str(g["name"])
                        return "success", g
            return "failure", {}
    
    def checkCancelConditionals(self,goal):
        state =  self.bt.run_condition(goal["cancel"])
        if state == "success":   
            return "success"
        else:
            return "failure" 
    def forgotConditional(self,toForgot, type_):
        if type_ == "reaction":
            condition = toForgot["activate"]
        elif type_ == "goal_activate":
            condition = toForgot["activate"]
        else:
            condition = toForgot["cancel"]
        
        conditionF = copy.deepcopy(condition)
        conditionF["action"] = "forget"
        self.bt.run_condition(conditionF)


    def manage(self):
        self.old_status = "none"
        self.status = "idle"
        current_reaction = {}
        self.current_goal  = {}
        goal_in_process = False

        while True:
            

            """
            print "the tree status is:"  + self.status
            if self.status == "idle":
                state_goal, goal =  self.checkActivateConditionals("goals")
                if state_goal == "success":
                    self.forgotConditional(goal, "goal_activate")
                    self.current_goal = copy.deepcopy(goal) # Copy a the goal / Reset
                    self.status = "goal_running"
                    goal_in_process = True


            elif self.status == "goal_running":
                canceled =  self.checkCancelConditionals(self.current_goal )
                if canceled == "success":
                    self.forgotConditional(self.current_goal , "goal_cancel")
                    self.current_goal = {}
                    self.status = "idle"
                    goal_in_process = False

                else:
                    response = self.do_step(self.current_goal ["bt"], "goal") 
                    if response == "success" or response == "failure":
                        self.current_goal = {}
                        self.status = "idle"
                        goal_in_process =  False"""
            
            if self.old_status != self.status:
                print "the tree status is:"  + self.status
                
            self.old_status = self.status

            if self.status == "reaction_running":
                response = self.do_step(current_reaction["bt"],"reaction")
                if response == "success" or response == "failure":
                    self.status = "reaction_finished"
                    time.sleep(.001)
            
            elif self.status == "reaction_finished":
                if goal_in_process:
                    self.status = "goal_running"
                else:
                    self.status = "idle"
                time.sleep(.001)

            #or status == "goal_running" or status == "goal_finished"
            elif self.status == "idle":
                # If goal is running check reaction conditions
                state, reaction =  self.checkActivateConditionals("reactions")
                # If a reaction is active do reaction
                if state == "success":
                    self.status = "reaction_running"
                    self.forgotConditional(reaction, "reaction")
                    current_reaction = copy.deepcopy(reaction) # Copy a the reaction / Reset
                else:
                    state_goal, goal =  self.checkActivateConditionals("goals")
                    if state_goal == "success":
                        self.forgotConditional(goal, "goal_activate")
                        self.current_goal = copy.deepcopy(goal) # Copy a the goal / Reset
                        self.status = "goal_running"
                        goal_in_process = True

            elif self.status == "goal_running":
                
                if len(self.current_goal) == 0:
                    self.status = "goal_finished"
                else:
                    # If goal is running check reaction conditions
                    state, reaction =  self.checkActivateConditionals("reactions")
                    if state == "success":
                        self.status = "reaction_running"
                        print ("Reaction prempt GOAL ================")
                        self.forgotConditional(reaction, "reaction")
                        current_reaction = copy.deepcopy(reaction) # Copy a the reaction / Reset
                    else:
                        canceled =  self.checkCancelConditionals(self.current_goal )
                        if canceled == "success":
                            self.forgotConditional(self.current_goal , "goal_cancel")
                            self.current_goal = {}
                            self.status = "goal_finished"
                            goal_in_process = False

                        else:
                            response = self.do_step(self.current_goal ["bt"], "goal") 
                            if response == "success" or response == "failure":
                                self.current_goal = {}
                                self.status = "goal_finished"
                                goal_in_process =  False
                
            elif self.status == "goal_finished":
                self.current_goal = {}
                self.status =  "idle" 


    def set_reactions(self,reaction_list):
        self.reactions = reaction_list
        
    def set_goals(self,goals_list):
        self.goals = goals_list
        
    def do_step(self,tree, node_type, debug = False):
        response = self.bt.tick(tree)
        if debug:
            if node_type == "reaction":
                print ("REACTION STEP RETURNS:" + str(response))
            else:
                print ("GOAL STEP RETURNS:" + str(response))
        time.sleep(self.tick_time)
        return response

    def step(self):
        response = self.bt.tick(self.tree)
        print ("FINAL STEP RESPONSE:" + str(response))
        time.sleep(self.tick_time)
        return response

    def execute(self,tree):
        self.tree = tree
        while True:
            response = self.step()
            self.bt.current_state == response
            if response == "success" or response =="failure" or response == "error":
                break
            elif response == "running":
                pass
                

