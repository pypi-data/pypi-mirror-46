import oldne
import threading
import time
import signal
import multiprocessing
import sys, os

class robot:
    
    def __init__(self, robot_name, pattern = "survey", middleware = "nanomsg" ):
        """ Define a new robot node using actionlib, the client-server pattern, the survey pattern or the publish/subscriber pattern

            Parameters
            ----------

            robot_name : string
                Node or robot name which identify the robot

            pattern : string
                - If selected "survey" or "surveyor", then "nanomsg" will be used as middleware
                - If selected "actionlib", then "ROS" will be used as middleware
                - If selected "client-server", then "ZeroMQ" will be used as middleware
                - If selected "pub-sub", then  "ZeroMQ" or "nanomsg" can be used as middleware

             middleware : string
                Used to select the middleware (only if the pattern parameter is set as "pub-sub")

        """

        self.pattern = pattern
        self.robot_name = robot_name
        self.deadline = 60 # cancel action that last more that 60 seconds
        self.action = {"state":"success"}
        self.currentActionID = "0"

        # Use survey pattern
        if self.pattern == "survey" or self.pattern == "surveyor":
            print ("ROBOT NODE using: survey pattern")
            self.resp = oldne.respondent("/manager") # Respondent subscribes to /manager topic 
            self.node = oldne.node(robot_name, "ZMQ", "robot") # New oldne node that can be used to kill the app
            conf_pub = self.node.conf_pub(mode='many2many')
            self.sharo = self.node.new_pub("/sharo", conf_pub)
        #TODO
        elif self.pattern == "pubsub":
            print ("ROBOT NODE using: publisher-subscriber pattern")
            # --------------- Publisher subscriber action nodes --------------------
            self.node = oldne.node(robot_name,"ZMQ","robot")
            conf_pub = self.node.conf_pub(mode='many2one')
            self.pub=  self.node.new_pub("/action_response",conf_pub)
            conf_sub =  self.node.conf_sub(mode='one2many')
            self.sub =  self.node.new_sub("/action_request",conf_sub)


            #conf_pub = self.node.conf_pub(mode='many2one')
            #self.pub_cond=  self.node.new_pub("/condition_response",conf_pub)
            #conf_sub =  self.node.conf_sub(mode='one2many')
            #self.sub_cond =  self.node.new_sub("/condition_request",conf_sub)
            time.sleep(1)
    
        self.state = "idle" # idle can only be idle, busy or wait
        self.result = "inactive" # result can only be success or failure.
        self.action2do = {"status":"0", "action":{}}
        # Give feedback to the rize interface
        self.fd = oldne.feedback(robot_name)
        self.robot_actions = {}
        self.isCanceled = False
        self.inActionExecution = False

        # ------------------------- Update thread ------------------------------------
        self.action_response = threading.Thread(target = self.__onUpdateStatus)
        # TODO add deamon, and deamon option in the costructor

        # ------------------------- Update thread ------------------------------------
        #self.condition_response = threading.Thread(target = self.__onCheckCondition)

        self.action_response.start()
        #self.condition_response.start()        
    def send_connection_error(self):
        self.fd.connection_error()
        
    def set_robot_conditions(self,robot_conditions):
        """ Set a python dictionary with all the internal conditions as a functions that returns False or True (with the own robot sensors).
            Parameters
            ----------
            robot_conditions : dictionary
                Dictionary of functions
            
        """

        try:
            self.robot_conditions = robot_conditions
        except Exception as e: 
            print(e)
            print ("Error setting conditions")
            self.fd.connection_error()
            time.sleep(1)

    def set_robot_actions(self,robot_actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        try:
            self.robot_actions = robot_actions
        except Exception as e: 
            print(e)
            print ("Error setting actions")
            self.fd.connection_error()
            time.sleep(1)
        


    def __onCheckCondition(self):
        while True:
            success, condition_request =  self.__listen_condition_request()
            if success:
                if condition_request["node"] == "condition":
                    print ("New internal condition check")
                    condition_state = self.check_condition(condition_request["primitive"])
                    print ("Condition result: " + str(condition_state))
                    self.__send_condition_response({"node":condition_state})
                      


    def __listen_request(self):
        """ Listen and wait for the robot actions
        """
        success =  False
        action_request = {}
        if self.pattern == "survey" or self.pattern == "surveyor":
            success, action_request = self.resp.listen_info(block_mode=False)
            #print action_request
        elif self.pattern == "pubsub":
            success, action_request = self.sub.listen_info(block_mode=False)

        if success:
            if self.robot_name in action_request['robots']: 
                success = True
            else:
                success = False

        return success, action_request



    def __listen_condition_request(self):
        """ Listen and wait for the robot actions
        """

        success =  False
        condition_request = {}
        if self.pattern == "survey" or self.pattern == "surveyor":
            condition_request = self.resp_cond.listen_info()
            success =  True
        elif self.pattern == "pubsub":
            success, condition_request = self.sub_cond.listen_info(block_mode=False)
        else:
            print ("ERROR: pattern " + self.pattern + "no avaliable")
        return success, condition_request
        

    def __send_response(self,msg):
        """ Send the response to the survey/cognitive node
        """
        #print 
        #print ("Response:")
        #print (msg)
        if self.pattern == "survey":
            self.resp.send_info(msg)
        elif self.pattern == "pubsub":
            self.pub.send_info(msg)


    def __send_condition_response(self,msg):
        """ Send the response to the survey/cognitive node
        """
        if self.pattern == "survey":
            self.resp_cond.send_info(msg)
        elif self.pattern == "pubsub":
            self.pub_cond.send_info(msg)


    
    def __onUpdateStatus_(self): #TODO delete
        """
        Update the state machine for action execution
        """
        while True:
            success, action_request =  self.__listen_request()
            if success:
                if action_request["node"] == "action":
                    if action_request["state"] == 'active':
                        self.action2do =  action_request
                        self.state = "ready"
                        msg = {"node":"running", "robot":self.robot_name}
                        if self.pattern == "survey": # TODO: improve?
                            self.__send_response(msg)

                    
                    elif action_request["state"] == 'running':
                        if self.state == "busy" or self.state == "ready":
                            self.state == "busy"
                            msg = {"node":"running", "robot":self.robot_name}
                            if self.pattern == "survey": # TODO: improve?
                                self.__send_response(msg)
                        elif self.state == "wait":
                            self.state = "idle"
                            msg = {"node":"success", "robot":self.robot_name}
                            if self.pattern == "survey": # TODO: improve?
                                self.__send_response(msg)
                        elif self.state == "idle": # TODO --- here if action state == running but current fsm state is idle, then the action was preempted.
                            msg = {"node":"success", "robot":self.robot_name}
                            if self.pattern == "survey": # TODO: improve?
                                self.__send_response(msg)


                #if action_request["node"] == "action":
                    #self.action2do =  action_request

                #if self.state == "idle":
                    #self.state = "busy"
                    #msg = {"node":"running", "robot":self.robot_name}
                    #if self.pattern == "survey": # TODO: improve?
                        #self.__send_response(msg)

            elif self.state == "wait" and self.pattern == "pubsub":  # TODO: improve?
                    self.state = "idle"
                    msg = {"node":"success", "robot":self.robot_name}
                    self.__send_response(msg)
    
        
    def run(self):
        self.fd.connection_ready()

        while True:

            if self.action["state"] == "active" or self.action["state"] == "pending":
                #self.action_process = multiprocessing.Process(target=self.run_action(self.action))
                self.inActionExecution = True
                try:
                    self.run_action(self.action)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)

                print (self.action["id"] + " finished")
                self.sharo.send_info(self.action)
                self.inActionExecution = False
                self.action["state"] = "success"
                self.isCanceled = False


                #self.run_action(self.action)
                #self.action["state"] = "success"
                #self.action_process.deamon = True
                #self.action_process.start()
            
                #if self.isCanceled == True:
                #if self.action_process.is_alive():
                    #self.action_process.terminate()
                    #self.action_process.joint()
                    #self.inActionExecution = False
                    #self.isCanceled = False
            time.sleep(.01)
                     

                    

    def cancelCurrentAction(self):
        self.isCanceled = True

    def resetActionTime(self):
        self.initActionTime =  time.time()

    def setAction(self,action_request):
        self.currentActionID = action_request["id"]
        self.action = action_request

    def getActionTime(self):
        return time.time() - self.initActionTime 
    
    def __onUpdateStatus(self):
        while True:
            success, action_request =  self.__listen_request()

            if success:
                print
                print "NWWWWWWWWWWWWWWWWWWWWWWWWWWW"
                print action_request
                if self.inActionExecution: # If action is in execution
                    new_action = self.checkIfNew(action_request)
                    print "returned new action" + str(new_action)
                    if new_action:
                        print "new action - cancel"
                        self.cancelCurrentAction() # Cancel current action
                        self.execution_state = "pending" # Send pending
                    else:
                        self.execution_state = "running"
                else:
                    new_action = self.checkIfNew(action_request)
                    print "returned new action " + str(new_action)
                    if new_action:
                        print "new action  - run"
                        print "running " + action_request["id"]
                        self.resetActionTime() #Reset time counter for actions
                        self.setAction(action_request) #Set new action to execute
                        self.execution_state = "running"
                    else:
                        self.execution_state = "success"

                msg = {"node":self.execution_state, "robot":self.robot_name}

                if self.execution_state == "success":
                    print ("Action -- " + action_request["id"] + " -- success")
                print msg

                self.__send_response(msg)
                
                
            if self.inActionExecution:
                action_time = self.getActionTime()
                if action_time > self.deadline: # Cancel if is in a posible deadlock
                    self.cancelCurrentAction() # Cancel current action
            time.sleep(0.01)
            


    def checkIfNew(self,action_request):
        state = action_request["state"]
        id_ = action_request["id"]
        print "Is new"

        print self.currentActionID
        print id_
        print id_ == self.currentActionID
        print 
        if id_ != self.currentActionID:
            return True
        else:
            return False
        


    def run_(self):  #TODO delete
        """ Run the action node
        """
        self.fd.connection_ready()
        
        while True:
            if self.state == "busy" or self.state == "ready":
                self.state = "busy"
                p = multiprocessing.Process(target=self.run_action(self.action2do))
                p.deamon = True
                p.start()

                # Wait for 10 seconds or until process finishes
                #p.join(30)
                #if p.is_alive():
                    #p.terminate()
                    #p.join()
                    #print ("WARNING: action have taken more than 30 seconds, it was closed")
                    #self.state == "ready"

                if not self.state == "ready":
                    self.state = "wait"
            else:
                time.sleep(.001)




    def check_condition(self, message):
        """ Run an action
            
            Parameters
            ----------

            action : dictionary
                Action description

        """
        condition_name = message["primitive"]
        print (condition_name + ":" +  message["input"])
        #options = primitive["options"]
        if condition_name in self.robot_conditions:
            # Execute function
            state = self.robot_conditions[condition_name](message)
            print (condition_name, " was executed")
            return state
                    
        else:
            print (condition_name, "is not a valid primitive")

        


    def run_action(self, message):
        """ Run an action
            
            Parameters
            ----------

            action : dictionary
                Action description

        """
            
        action = message["primitives"] # Get list of concatenated primitives
        n_primitives = len(action)
        in_parallel = True
                
        # Perform all the actions in parallel
        for i in range(n_primitives):
                    
            # Except the last one
            if (i == n_primitives-1):
                in_parallel = False
                
            primitive = action[i]
            primitive_name = primitive["primitive"] #Name of the primitive
            input_ = primitive["input"]
            options = primitive["options"]

            if primitive_name in self.robot_actions:
                # Execute function
                self.robot_actions[primitive_name](input_, options, in_parallel)
                print (primitive_name, " was executed")
                    
            else:
                print (primitive_name, "is not a valid primitive")




