#!/usr/bin/env python

# ------------------------ oldne types --------------------------------
# Description: Basic types definition for oldne
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga

#TODO: add raise exceptions to avoid type errors 
from oldne import*


class vector:
    """Creates a new 3D vector instance to represent 3D points, position, linear and angular velocity or acceleration, or other 3D representation

    Parameters
    ----------

    x : float
        x coordinate
    y : float
        y coordinate
    z : float
        z coordinate

    Example
    ----------

    Access to the vector values using dictionary notation

    >>> import oldne.oldne_msg 
    >>> p = oldne.vector(10,20.5,30)
    >>> print p.data # Print dictionary value
    {'y': 20.5, 'x': 10, 'z': 30, 'type': 'point'}
    >>> print p.data['x'] # Print value of x
    10

    .. seealso:: Module :py:mod:`vector`

    """
    def __init__(self, x = 0, y = 0, z = 0):
        self.data = {'x' : x, 'y' : y, 'z' : z, 'type' : "vector"}

class quaternion:
    """Creates a new quaternion instance to represent orinetation

    Parameters
    ----------

    x : float
        x value
    y : float
        y value
    z : float
        z value
    w : float
        w value

    Example
    ----------

    Access to the vector values using dictionary notation

    >>> import oldne.oldne_msg 
    >>> q = oldne.quaternion(0,0,0,1)
    >>> x = q['x']
    
    """
    
    def __init__(self,x = 0, y = 0, z = 0, w = 0):
        self.data = {'x' : x, 'y' : y, 'z' : z, 'w' : 0,  'type' : "quaternion"}

class velocity:
    """Creates a new velocity (twist) instance

    Parameters
    ----------

    linear : oldne.vector
        linear velocity
    angular : oldne.vector
        angular velocity

    Example
    ----------

    Access to the vector values using dictionary notation

    >>> import oldne.oldne_msg
    >>> linear = oldne.vector(0,1,0)
    >>> angular = oldne.vector(0,0,1)
    >>> vel = oldne.velocity(linear,angular)
    >>> x_linear = vel.data['linear']['x']
    
    """

    def __init__(self, linear , angular):
        
        self.data = {'linear' : linear.data , 'angular': angular.data, 'type' : "velocity"}
        
class accel:
    """Creates a new acceleration instance

    Parameters
    ----------

    linear : oldne.vector
        linear acceleration
    angular : oldne.vector
        angular acceleration

    Example
    ----------

    Access to the vector values using dictionary notation

    >>> import oldne.oldne_msg
    >>> linear = oldne.vector(0,1,0)
    >>> angular = oldne.vector(0,0,1)
    >>> accel= oldne.accel(linear,angular)
    >>> x_linear = accel.data['linear']['x']
    
    """

    def __init__(self, linear , angular):
        self.data = {'linear' : linear.data , 'angular': angular.data, 'type' : "accel"}

class wrench:
    """Creates a new wrench instance 
    
    Parameters
    ----------

    force : oldne.vector
        force component
    torque : oldne.vector
        torque component

    Example
    ----------

    Access to the vector values using dictionary notation

    >>> import oldne.oldne_msg
    >>> force = oldne.vector(15,10,100)
    >>> torque = oldne.vector(10,10,20)
    >>> wr = oldne.wrench(force,torque)
    >>> Fx = wr.data['force']['x']
    
    """



    def __init__(self, force , torque):
        self.data = {'force' : force , 'torque' : torque, 'type' : "wrench"}
    
class pose:
    """Creates a new pose instance 

    Parameters
    ----------

    position : oldne.vector
        position component
    orientation : oldne.quaternion
        orientation component in quaternion representation

    Example
    ----------

    Access to the vector values using dictionary notation

    >>> import oldne.oldne_msg
    >>> position = oldne.vector(15,10,100)
    >>> rotation = oldne.quaternion(0,0,0,1)
    >>> pose = oldne.pose(position,rotation)
    >>> w = pose.data['orientation']['w']
    
    """

    def __init__(position, orientation):
        self.data = {'position' : position , 'orientation' : orientation, 'type' : "pose" }
                                    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
                              
