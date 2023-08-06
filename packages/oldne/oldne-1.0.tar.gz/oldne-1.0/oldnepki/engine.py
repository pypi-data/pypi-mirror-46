import oldnepki
from random import randint
import copy 
# These is the main Behavior Tree class
#TODO: delate activation parameter
class engine():
    def __init__(self, middleware = "NN"):
        """
        oldnepkiKi Behavior Tree main class.

        Parameters
        ----------

        middleware : string
            If == "NN" then the surveyor pattern will be used, else ROS action lib will be used

        """
        self.current_state = "running"
        print ("New BT class created")
        self.exit = True
        self.next = False
        if middleware == "NN" or middleware == "nanomsg":
            self.manager = oldnepki.behavior_manager("NN",  pattern = "surveyor")
        elif middleware == "ROS":
            self.manager = oldnepki.behavior_manager("ROS",  pattern = "actionlib")
        elif middleware == "ZMQ":
            self.manager = oldnepki.behavior_manager("ZMQ",  pattern = "pubsub")
        else:
            print ("behavior tree initialization error")
            
            

    def tick(self,node, activate = False):
        node_type =  node["node"]
        if node["state"] == "active" or node["state"] == "running":
            
            if node_type == "sequence":
                return self.run_sequence(node,activate)
            
            elif node_type == "selector":
                return self.run_selector(node,activate)

            elif node_type == "action":
                return self.run_action(node)

            elif node_type == "condition":
                return self.run_condition(node)

            elif node_type == "random_selector":
                return self.run_random_selector(node,activate)

            elif node_type == "always_failure":
                return self.run_always_failure(node,activate)

            elif node_type == "until_success":
                return self.run_until_success(node,activate)

            elif node_type == "negation":
                return self.run_negation(node,activate)


    def run_until_success(self,node,activate):
        children = node["children"]
        if activate == True:
            node["n"] = 0
        child = children[0]
        n_max = node["max"]
        n_times = node["n"]
        if (n_times < n_max):
            if node["state"] == "loop":
                print ("loop")
                print (n_times)
                self.tick(child,True) #Activation

            response = self.tick(child,False) #Execution
            print ("until success response " + str(response))
            if response == "failure":
                node["n"] = node["n"] + 1
                self.set_node_running(node) #TODO: Esta y la siguiente linea casuo confusion
                node["state"] = "loop" # TODO: Loop simpre debe ir luego de un ser node state, mejor has un set loop
                return "running"
            elif response == "running":
                self.set_node_running(node)
                return "running"
            elif response == "success":
                self.set_node_success(node)
                return "success"
            print (child)
            
        else:
            self.set_node_success(node)
            return "success"

    def run_always_failure(self,node,activate):
        children = node["children"]
        child = children[0]
        response = self.tick(child, activate)
      
        if response == "running":
            self.set_node_running(node)
            return response
        else:
            self.set_node_failure(node)
            return "failure"
        return "error"


    def run_negation(self,node,activate):
        children = node["children"]
        child = children[0]
        response = self.tick(child, activate)
      
        if response == "running":
            self.set_node_running(node)
            return response
        elif response == "success":
            self.set_node_failure(node)
            return "failure"
        else:
            self.set_node_success(node)
            return "success"
        return "error"

    def run_random_selector(self,node,activate):
        children = node["children"]
        if node["n"] == "none":
            n_child = len(children)
            n_selected = randint(0, n_child-1)
            node["n"] = n_selected 
        response = self.tick(children[node["n"]],activate)
        if response == "running":
            self.set_node_running(node)
            return response
        elif response == "success":
            self.set_node_success(node)
            node["n"] = "none"
            return response
        elif response == "failure":
            self.set_node_failure(node)
            node["n"] = "none"
            return response 

    def run_condition(self,node):
        response = self.manager.check_condition(node, self.current_state)

        if response == "failure":
            self.set_node_failure(node)
        elif response == "success":
            self.set_node_success(node)
        return response

    def run_action(self,node):

        print ("Action to do: " + node["id"])
        response = self.manager.research(node)
        if response == "running":
            if node["state"] == "active":
                print ("Action now in execution")
            print "running"
            self.set_node_running(node)
        elif response == "pending":
            print ("Action waiting for execution")
            response = "running"
        elif response == "failure":
            self.set_node_failure(node)
            print  ("Action returned: " + str(response)) 
        elif response == "success":
            self.set_node_success(node)
            print  ("Action returned: " + str(response)) 
        elif response == "error":
            self.set_node_error(node)
            print  ("Action returned: " + str(response))         
        
        return response
        

    def set_node_running(self,node):
        # Set the node with running state
        node["state"] = "running"

    def set_node_success(self,node):
        # Set the node with succeess state
        node["state"] = "success"

    def set_node_failure(self,node):
        # Set the node with succeess state
        node["state"] = "failure"

    def set_node_error(self,node):
        # Set the node with error state
        print ("ERROR: in")
        node["state"] = "error"


    def run_sequence(self,node,activate):
        children = node["children"]
        if type(children) is list:

            for child in children:
                response = self.tick(child,activate) # Get response from child
                if response == "success":
                    pass
                elif response == "running":
                    return response # Return exit and "running" state
                elif response == "failure":
                    self.set_node_failure(node)
                    return  response
                elif response == "error":
                    self.set_node_error(node)
                    return response
        else:
            response = self.tick(children,activate) # Get response from child
            if response == "success":
                pass
            elif response == "running":
                self.set_node_running(node) #Set parent in "running"
                return response # Return exit and "running" state
            elif response == "failure":
                self.set_node_failure(node)
                return  response
            elif response == "error":
                self.set_node_error(node)
                return response
            

        self.set_node_success(node)
        return "success"

    def run_selector(self,node,activate):

        children = node["children"]
        if type(children) is list:
            for child in children:
                response = self.tick(child,activate) # Get response from child
                if response == "success":
                    self.set_node_success(node) 
                    return  response
                elif response == "running":
                    self.set_node_running(node) #Set parent in "running"
                    return response # Return exit and "running" state
                elif response == "failure":
                    pass
                elif response == "error":
                    self.set_node_error(node)
                    return response

        elif type(children) is dict:
            children = [children]

            response = self.tick(child,activate) # Get response from child

            if response == "success":
                self.set_node_success(node) 
                return  response
            elif response == "running":
                self.set_node_running(node) #Set parent in "running"
                return response # Return exit and "running" state
            elif response == "failure":
                pass
            elif response == "error":
                self.set_node_error(node)
                return response
        self.set_node_failure(node)
        return "failure"

