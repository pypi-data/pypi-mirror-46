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
            
class behavior_manager():
    

    def __init__(self, middleware = "nanomsg",  pattern = "pubsub", blackboard = "sharo"):

        """
        Robot interaction manager class. Used mainly to send the robot behavior spcecification to the robots.

        Parameters
        ----------

        meddleware: string
            Middleware used for communication

        pattern : string
            Communication pattern used for behavior execution

        blackboard : string
            Blackboard selector. 

        """

        success = False
        self.goals = {}
        # oldne node definition
        self.node = oldne.node("robot_manager","False","cognition")
        self.blackboard = blackboard
        self.pattern = pattern
        self.middleware = middleware
        self.blackboard_error_counter = 0 # Communnication errors with blackboard
        self.robot_error_counter = 0 # Comunication errros with robots

        if  middleware == "ROS":
            pass
        elif middleware == "ZMQ":
            
            if pattern == "pubsub":
                try:
                    # ----------------------- Action request publisher ------------------------
                    # This publisher is in one2many communication mode
                    # Therefore, only one execution manager can be runned at the same time
                    # In this way we can detect when a program is already running

                    conf = self.node.conf_pub(mode= "one2many") 
                    self.pub = self.node.new_pub("/action_request", conf)

                    # ---------------------- Action response subscriber ------------------------
                    # Responses from several robots can be read only for this node 
                    conf = self.node.conf_sub(mode= "many2one")
                    self.sub = self.node.new_sub("/action_response", conf)


                    # ----------------------- Condition request publisher ------------------------
                    # This publisher is in one2many communication mode
                    # Therefore, only one execution manager can be runned at the same time
                    # In this way we can detect when a program is already running

                    conf = self.node.conf_pub(mode= "one2many") 
                    self.pub_cond = self.node.new_pub("/condition_request", conf)

                    # ---------------------- Action response subscriber ------------------------
                    # Responses from several robots can be read only for this node 
                    conf = self.node.conf_sub(mode= "many2one")
                    self.sub_cond = self.node.new_sub("/condition_response", conf)

                    success = True

                except:
                    # ---------------------- Node already used case ----------------------------
                    # If another program have been launched then give feedback to the user and close this node.
                    print ("WARNING: Another behavior manager node have been launched, please stop the execution of that node first")
                    time.sleep(2)
                    # Feedback to the user are send via "/node_status" topic
                    # Send message to the node supervisor, node already open
                    fd = oldne.feedback("robot_manager")
                    fd.execution_busy()
                    import sys
                    sys.exit()
                    
            elif pattern == "client-server":
                pass

        elif middleware == "NN" or middleware == "nanomsg":
            
            # --------------------------- Action Surveyor  -----------------------------
            # TODO: simplify this.
            deadline = 3000
            self.sur = oldne.surveyor('/manager',deadline)     # Robot Action Manager and Monitor
            self.sur_cond = oldne.surveyor('/blackboard',deadline)  # Blackboard 
            time.sleep(1)
            success= True

        else:
            print ("middleware parameter can only take values of 'ROS', 'ZMQ' or 'nanomsg'")

        
    def check_goal_condition(self,node): # TODO delete
        name = node["input"]
        options =  node["options"]

        if name in self.goals:
            value = self.goals[name]
            since = time.time() - value["time"]

            if (int(since) >= int(options["time"])):
                return "success"
            else:
                return "failure"
        else:
            self.goals[name] = {"time":time.time()}
            return "success"

    def set_goal_time(self,node): # Set time to the goal to wait for new execution # TODO delete
        name = node["input"]
        if name in self.goals:
            value =self.goals[name]
            value["time"] = time.time()
        return "success"
    # ----------------------------------------------------- Check condition function -------------------------------------------------
    def check_condition(self,condition, current_state):
        """
        Ask to the blackboard about the state of some condition. This function returns "success" if the condition is True, otherwise the function returns "failure".

        Parameters
        ----------
        condition : dictionary
            Condition to be cheked. Use the format {"node":"condition","primitive":<primitive_name>, "input":<state_name>}. Where <primitive_name> is the primitive behavior id and <state_name> the state to verify the condition.

        Returns
        ----------

        result : string
            Returns "success" if the condition is True, otherwise returns "failure".

        """

        # TODO: change working_memory_client for surveyor pattern
        #print ("-------- Condition ---------")
        #print (condition["primitives"])
        #print (condition["logic"])
        if not condition["source"] == "goal":
            
            state = self.research(condition,"condition")
            #if not current_state == "running":
                #condition["memory"] = False
                #copy_condition["input"] = "delete"
                #self.research(condition,"condition")

            if type(state) is bool:
                if state == True:
                    return "success"
                else:
                    return "failure"
            else:
                return state

        else:
            result = self.check_goal_condition(condition["primitive"])
            return result 


    # ------------------------------------------------------ New action  function ------------------------------------------------------
    def new_action(self, primitives, robots):
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
        action =  ""

        if not bool(primitives) and not bool(robots):
            print ("Primitives or robot not filled")
        else:
            # call oldneki.nodes.action
            action = oldneki.action(primitives, robots)
            if self.execute == True:
                self.run(action)
        return action

    # --------------------------------------------- Research function -----------------------------------------------
    def research(self,node,node_type="action"):
        """
        Send a request of execution or research of an action using the survey pattern

        Parameters
        ----------
        node : dictionary
            node to be executed or checked
        node_type : dictionary
            "action" or "condition"

            
        Returns
        ----------
        response : string
            State of the action or condition execution
        """
        if self.middleware == "NN" or self.middleware == "nanomsg":
            if node_type == "action":
                node["output"] = "x"
                if node["output"] == "blackboard":
                    self.set_goal_time(node["primitives"][0])
                    return "success"
                else:
                    self.sur.send_info(node)
                    s, msg = self.sur.listen_info()
                    if s:
                        response = msg["node"]
                        return response
                    else:
                        print ("ERROR: not response from robot")
                        return "error"
            elif node_type == "condition":

                # Is primitives field non null?
                if len(node['primitives']) == 0:
                    return "failure"
                else:
                    # If non null then ask if condition is met
                    self.sur_cond.send_info(node)
                    s, msg = self.sur_cond.listen_info()
                    if s: # If robot response
                        self.blackboard_error_counter = 0
                        response = msg["node"]
                        return response
                    else: # If not response from blackboard give feedback after 5 continue errors 
                        self.blackboard_error_counter = self.blackboard_error_counter + 1
                        if self.blackboard_error_counter > 5:
                            print ("ERROR: not response from blackboard")
                        return "failure"
                
        elif self.middleware == "ZMQ"and self.pattern == "pubsub":
            if node_type == "action":
                if node["output"] == "blackboard":
                    self.set_goal_time(node["primitives"][0])
                    return "success"
                else:
                    self.__action_pub_sub(node)
                    return "success"  #TODO: feedback from the subscribers? 
            else:
                return self.__condition_pub_sub(node)  #TODO: feedback from the subscribers? 
                
            

    def __condition_pub_sub(self, condition):
        print ("CONDITION checking:")
        print (condition)
        self.pub_cond.send_info(condition)
        return self.wait_cond_response()
        

    def __action_pub_sub(self, action):
        """
        Send action to execute using pub_sub pattern

        Parameters
        ----------
        tree : dictionary
            behavior tree JSON description

        """

        print ("ACTION execution:")
        print (action)
        self.pub.send_info(action)

        if type(action['robots']) is list:
            robots =  action['robots']
        else:
            robots =  [action['robots']]

        # Wait for robot responses
        self.wait_response(robots)


    def wait_cond_response(self): # Improve blocking mode, and select robots
        success, state = self.sub_cond.listen_info(True)
        return state["node"]

    def wait_response(self, robots): # Improve blocking mode
        """
        Wait until get response from all robots

        Parameters
        ----------
        robots : list
            list of robot names (nodes)

        """

        new_robot_list = robots[:]

        print ("Waiting for response of " + str(new_robot_list))
        while len(new_robot_list) > 0:
            success, state = self.sub.listen_info(False)
            if success:
                robot = str(state["robot"]) 
                result = str(state["node"])
                print ("Action performed by " + robot + " with: " + result + " ")
                if robot in new_robot_list:
                    new_robot_list.remove(robot)
                    if new_robot_list != []:
                        print ("Robots left: " + str(new_robot_list) )
            time.sleep(.001)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
