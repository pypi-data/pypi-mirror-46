import time
import oldnepki

# These functions are used to define nodes of Behavior Trees in JSON format.

def negation(children, memory=False):
    json_ = {"node":"negation",  "state":"active", "memory":memory, "n":0, "children":children}
    return json_

def random_selector(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"random_selector", "state":"active", "memory":memory, "n":"none", "children":children}
    return json_

def until_success(children, n_max = 5, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"until_success", "state":"active", "memory":memory, "n":0, "max":n_max, "children":children}
    return json_
    

def always_failure(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"always_failure", "state":"active", "memory":memory, "n":0, "children":children}
    return json_
 

def action(primitives, robots, memory=False, output="robot"):
    # Function used to specify an action from a primitive or a list of primitives.
    # The user also specify the robots where execute these asction
    if type(primitives) is list:
        message = {"node":"action",  "state":"active", "memory":False, "n":0, "primitives":primitives, "robots":robots, "output":output}
    else:
        message = {"node":"action", "state":"active", "memory":False, "n":0, "primitives":[primitives], "robots":robots, "output":output}
    return message

def sequence(children, memory=False, reactive = "False"):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"sequence","state":"active", "memory":memory, "n":0,"children":children, "reactive":reactive}
    return json_

def selector(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"selector","state":"active", "memory":memory, "n":0,"children":children}
    return json_

def condition(primitive, memory= False, source = "blackboard", robots = "any", type_action = "ask"):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"condition","state":"active", "memory":memory, "n":0, "source":source,"primitive":primitive, "robots":robots, "action_type":type_action }
    return json_

