# coding = utf-8
#!/usr/bin/env python

# ------------------------ Communication module --------------------------------
# Description: Set of classes used for simplify the use of ZeroMQ, ROS and nanomsg
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
import simplejson
import sys
import socket
import signal
import threading
import oldne


#TODO: use of JSON to send info by normal POSIX sockets
#TODO: bug sending strings there is a space + message in publish-subscriber with ZMQ
#TODO: master node in mutiple PCs for many2many

try:
    import nanomsg
except ImportError:
    pass

class node:

    # ----------------------- __signal_handler  ------------------------------
    def __signal_handler(self, signal, frame):
        """Signal handler used to close when user press Ctrl+C"""
        print('Signal Handler, you pressed Ctrl+C! to close the node')
        time.sleep(1)
        import os
        pid = os.getpid()
        print (pid)
        import subprocess as s
        s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
        sys.exit(0)
        
    # ----------------------- __wait_kill ------------------------------
    def __wait_kill(self):
        """Listen for close the current node from an extrenal message on the topic \oldne_node"""
        exit = False
        time.sleep(.1)
        conf = self.conf_sub("dict","ZMQ","direct","7002","127.0.0.1", "one2many") 
        exit_sub  = self.new_sub("/oldne_node", conf)
        time.sleep(.1)

        # Always wait in blocking mode for the kill message of the node 
        while not exit:
            # Wait for kill signal (Operation in blocking mode)
            s, data = exit_sub.listen_info(True) 
            # If new kill signal detected
            if s == True:
      
                try:
                    kill_proccess = False
                    node_ = "NA"
                    type_ = "NA"
                    
                    # Check if message specify the name of a node
                    if "node" in data and "type" in data: 
                        try:
                            node_ = data["node"]
                            type_ = data["type"]

                            if type(node_) is list and type(type_) is str:
                                for l in node_:
                                    # If one of the names and the type of the request to kill is equal the name and type of this node, then kill the node
                                    if l == self.node_name and type_ == self.node_type:
                                        kill_proccess = True
                            elif type(node_) is str and type(type_) is str: 
                                # If current name and type of the request to kill is equal the name and type of this node, then kill the node
                                if node_ == self.node_name and type_ == self.node_type:
                                    kill_proccess = True
                        except:
                            print ("oldne ERROR: node key in kill menssage is not string or list of strings")


                    if kill_proccess:
                        print ("************* Signal to stop program **************")
                        print (data)
                            
                        exit = True
                        import os
                        pid = os.getpid()
                        print (pid)
                        import subprocess as s
                        s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
                except:
                    pass
        
    
    def __init__(self, node_name, transport = "ZMQ", node_type = "none" , exit_thread = True):
        """
        Class used to define a new node using the publisher-subscriber pattern. This class is compatible with ZeroMQ, Nanomsg and ROS.

        Parameters
        ----------

        node_name : string 
            Name of the node
        
        transport : string
            Define the transport layer of the node, can be 'ROS' to use ROS, 'ZMQ' to use ZeroMQ and 'NN' or 'nanomsg' to use nanomsg.

        node_type : string 
            This parameter specify the type of the node. This can enable to kill it publishing a dictionary in the '\oldne_node' topic. It takes the value of "none" by default.

        exit_thread : bool
            If True then the node can be killed sending a dictionary to the "/oldne_node topic with the info of {'node': <node-name-to-kill>} or {"type":<node-type-to-kill>}. Where  <node-name-to-kill> and  <node-type-to-kill> can be string or list of strings.

        """
        self.node_type = node_type
        self.NN_installed = False
        try:
            import nanomsg
            self.NN_installed = True
        except ImportError:
            print ("Nanomsg not installed")
            self.NN_installed = False
            
        # Enable to kill the node using Ctrl + C
        signal.signal(signal.SIGINT, self.__signal_handler)
        
        self.node_name = node_name
        self.transport  = transport 
        print ("New oldne node: " + self.node_name)

        if exit_thread: # Enable this node to be killed from an external signal
            # ------------------------- Kill thread ------------------------------------
            # thread that can de used to stop the program
            self.exit = threading.Thread(target = self.__wait_kill)
            # Used to finish the background thread when the main thread finish
            self.exit.daemon = True
            # start new thread 
            self.exit.start()

        
        if self.transport  == 'ROS':
            try:
                import rospy		
                rospy.init_node(node_name, anonymous=True)
                print ("ROS node started")
            except:
                print ("ERROR: rospy not found, possible causes:")
                print ("- Are you using Ubuntu?")
                print ("- Have you installed ROS in your PC?")
                print ("- Have you used roscore command to start the ROS Master")
                print ("- Are you using Python 2.7")
                
                if sys.version_info < (3.0):
                    y = raw_input("Press ENTER to continue and exit")
                else:
                    time.sleep(5)
                sys.exit(1)


    def conf_pub(self, msg_type = "dict", transport = "ZMQ" , network = "P2P", port = "9000", ip = "127.0.0.1", mode = "one2many" ):
        """

        The configuration of publishers are defined using a python dictionaries with a specific format. By default ZeroMQ is set in a "P2P" network in "one2many" mode.

        Parameters
        ----------
        msg_type : string 
            Type of data to send (recomended to allows ROS geometric messages compatibility)

        transport : string 
            Transport layer used for communication, it can be:"ZMQ" to use ZeroMQ, "ROS" to use ROS, and "NN" or "nanomsg" to use Nanomsg

        network : string 
            Type of network architecture, it can be "direct" and "P2P" (only for ZeroMQ and Nanomsg)

        port : string 
            Value of the port to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        ip : string 
            Value of the ip to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        mode : string
            Only for ZeroMQ and Nanomsg. It can be "one2many" (one publisher and many subscribers in a topic), "many2one" (one publisher and many subscribers in a topic), "many2many" (many publishers and many subscribers in a topic).    

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the publisher

        """

        
        conf = { 'msg_type': msg_type, 'transport': transport, 'network': network, 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def conf_sub(self, msg_type = "dict", transport = "ZMQ", network = "P2P", port = "9000", ip = "127.0.0.1", mode = "one2many" ):
        
        """
        This function can be used to define the configuration of a subscriber. By default ZeroMQ is set in a "P2P" network in "one2many" mode.

        Parameters
        ----------
        msg_type : string 
            Type of data to send (recomended to allows ROS geometric messages compatibility)

        transport : string 
            Transport layer used for communication, it can be "ZMQ" to use ZeroMQ, "ROS" to use ROS, and "NN"or "nanomsg" to use Nanomsg

        network : string 
            Type of network architecture, it can be "direct" and "P2P" (only for ZeroMQ and Nanomsg)

        port : string 
            Value of the port to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        ip : string 
            Value of the ip to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        mode : string
            Only for ZeroMQ and Nanomsg. It can be "one2many" (one publisher and many subscribers in a topic), "many2one" (one publisher and many subscribers in a topic), "many2many" (many publishers and many subscribers in a topic).    

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the subscriber

        """

        conf = { 'msg_type': msg_type, 'transport': transport, 'network': network, 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def new_pub(self,topic, configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip': '127.0.0.1', 'msg_type' : 'dict' }):
        """
        Function used to generate a new publisher in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        configuration : dictionary 
            Configuration of the publisher


        Returns
        ----------

        pub : publisher
            publisher instance


        Example
        ----------

        Creates a default ZMQ publisher connected to the oldne master node

        .. code-block:: python

            import oldne
            new_node = oldne.node("dummy_node")
            configuration = new_node.conf_pub() 
            pub = new_node.new_sub("dummy_topic", configuration)

        """
        
        #TODO: launch error if you dont put msg_type or conf
        pub = publisher(topic, self.node_name, configuration)
        return pub

    def new_sub(self,topic, configuration =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip': '127.0.0.1', 'msg_type' : 'dict' }):

        """
        Function used to generate a new subscriber in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        configuration : dictionary  
            Configuration of the subscriber

        Returns
        ----------

        sub : subscriber 
            subscriber instance


        Creates a default subscriber

        .. code-block:: python

            import oldne
            new_node = oldne.node("dummy_node")
            configuration = new_node.conf_sub() 
            sub = new_node.new_sub("dummy_topic", configuration)

        """

        sub = subscriber(topic, self.node_name, configuration)
        return sub



class publisher:
    """ Publisher class used for inter-process comunication between nodes. Supports ZeroMQ, nanomsg and ROS publishers. 
        Parameters
        ----------

        topic : string 
            Topic name to publish the messages

        node_name : string
            Name of the node 

        conf : dictionary
            Configuration of the publisher. The ease way to define this parameter is to use the conf_pub function of the node class

        Examples
        ----------

        Send a dictionary in a default ZeroMQ publisher:


        .. code-block:: python

            import oldne
            new_node = oldne.node("dummy_node")
            configuration = new_node.config_sub()
            pub = new_node.new_pub("dummy_topic", configuration)
            pub.send_info({'message':"hello"}) 


        Send a oldne_msg in a default ZeroMQ publisher:

        .. code-block:: python

            import oldne
            import oldne.oldne_msg
            new_node = oldne.node("dummy_node")
            configuration = new_node.conf_sub(msg_type = "vector") # oldne_msg definition
            pub = new_node.new_pub("dummy_topic", configuration)
            vector = oldne.vector(0,0,1)
            pub.send_info(vector)
            
        Send a oldne_msg in ROS publisher:

        .. code-block:: python

            import oldne
            import oldne.oldne_msg
            new_node = oldne.node("dummy_node", useROS=True)
            # ROS Vector3 definition
            configuration = new_node.conf_sub(msg_type = "vector", transport = "ROS")
            pub = new_node.new_pub("dummy_topic", configuration)
            vector = oldne.vector(0,0,1) 
            pub.send_info(vector) 

    """

    def __init__(self, topic, node_name = "default", conf =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip' : '127.0.0.1', 'msg_type' : 'dict' }):

        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node_name = node_name
        self.topic = topic
        self.msg_type =  self.conf['msg_type']

        if self.transport ==  "ZMQ": #Use ZeroMQ
            print ("New publisher using ZMQ")
            try:
                self.mode = self.conf['mode']
            except:
                print ("WARNING: publisher mode parameter not defined, 'one2many' mode is set by default")
                self.mode = "one2many"
            self.__create_ZMQ_publisher()

        elif self.transport ==  "ROS": #Use ROS
            print ("New publisher using ROS")
            self.__create_ROS_publisher()
            
        elif self.transport ==  "NN" or middleware == "nanomsg": #Use nanmsg

            self.NN_installed = False
            try:
                import nanomsg
                self.NN_installed = True
            except ImportError:
                print ("Nanomsg not installed")
                self.NN_installed = False

            if self.NN_installed == False:
                msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
                raise ValueError(msg)
            print ("New publisher using nanomsg")
            try:
                self.mode = self.conf['mode']
                self.__create_NN_publisher()
            except:
                print ("WARNING: publisher mode parameter not defined, 'one2many' mode is set by default")
                self.mode = "one2many"
                self.__create_NN_publisher()
        else:
            msg = "ERROR: Transport parameter " + self.transport + "is not supported, use instead 'ROS', 'ZMQ' (for ZeroMQ) or 'NN' (for nanomsg). "
            raise ValueError(msg)


    #TODO:also define queue_size
    def __create_ROS_publisher(self):
        """Function used to create a ROS publisher"""
        import rospy

        if self.msg_type == "string":
            from std_msgs.msg import String
            self.ros_pub = rospy.Publisher(self.topic, String, queue_size=10)

        elif self.msg_type == "velocity":
            from geometry_msgs.msg import Twist
            self.ros_pub = rospy.Publisher(self.topic, Twist, queue_size=10)

        elif self.msg_type == "point":

            from geometry_msgs.msg import Point
            self.ros_pub = rospy.Publisher(self.topic, Point, queue_size=10)

        elif self.msg_type == "wrench":

            from geometry_msgs.msg import Wrench
            self.ros_pub = rospy.Publisher(self.topic, Wrench, queue_size=10)

        elif self.msg_type == "accel":

            from geometry_msgs.msg import Accel
            self.ros_pub = rospy.Publisher(self.topic, Accel, queue_size=10)

        elif self.msg_type == "quaternion":

            from geometry_msgs.msg import Quaternion
            self.ros_pub = rospy.Publisher(self.topic, Quaternion, queue_size=10)

        elif self.msg_type == "vector":

            from geometry_msgs.msg import Vector3
            self.ros_pub = rospy.Publisher(self.topic, Vector3, queue_size=10)

        elif self.msg_type == "pose":

            from geometry_msgs.msg import Pose
            self.ros_pub = rospy.Publisher(self.topic, Pose, queue_size=10)
        

    def __create_ZMQ_publisher(self):
        """Function used to create a ZeroMQ publisher"""

        if self.network == "direct":
            self.port = self.conf['port']
            # Set the port selected by the user
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the oldne Master and get the port
            print ("Advertising topic (" + self.topic + ") to oldne Master ....")
            port = self.__advertising_oldne(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode )
            print ("Topic registered by the oldne Master")

        ip = self.conf['ip']
        endpoint = "tcp://" + ip + ":" + str(port)
        

        # Create a new ZeroMQ context and a publisher socket
        try:
            context = zmq.Context()
            # Define the socket using the "Context"
            self.sock = context.socket(zmq.PUB)


            #Set the topic of the publisher and the end_point
            
            if self.mode == "one2many":
                # This allows only use one publisher connected at the same endpoint
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                print ("publisher " + endpoint +  " connect")
                self.sock.connect(endpoint)
            elif  self.mode == "many2many":
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)

        except:
            print("Socket already in use, restarting")
            self.sock.close()
            context.destroy()
            time.sleep(.2)
            context = zmq.Context()
            self.sock = context.socket(zmq.PUB)
            if self.mode == "one2many":
                # This allows only use one publisher connected at the same endpoint
                self.sock.bind(endpoint)
                print ("publisher " + endpoint +  " bind")
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            elif  self.mode == "many2many":
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)

        time.sleep(1)
        #TODO: why this problem?
        #This next lines are used to start the comunication, and avoid some errors presented with zeromq
        #message = {'actions': [{'action':'none', 'inputs':'none'}]}
        #self.send_info(message)

        # ZeroMQ note:
        # There is one more important thing to know about PUB-SUB sockets: 
        # you do not know precisely when a subscriber starts to get messages.
        # Even if you start a subscriber, wait a while, and then start the publisher, 
        # the subscriber will always miss the first messages that the publisher sends. 


        # In Chapter 2 - Sockets and Patterns we'll explain how to synchronize a 
        # publisher and subscribers so that you don't start to publish data until 
        # the subscribers really are connected and ready. There is a simple and 
        # stupid way to delay the publisher, which is to sleep. Don't do this in a
        #  real application, though, because it is extremely fragile as well as
        #  inelegant and slow. Use sleeps to prove to yourself what's happening, 
        # and then wait for 
        # Chapter 2 - Sockets and Patterns to see how to do this right.

        #This delay in important, whithout them the comunication is not effective.

        time.sleep(1)
        print ("ZMQ publisher started in " +  endpoint)
        print

    def __create_NN_publisher(self):
        """Function used to create a Nanomsg publisher"""

        if self.NN_installed == False:
            msg = "Unable Nanomsg due that is not installed "
            raise ValueError(msg)

        if self.network == "direct":
            self.port = self.conf['port']
            # Set the port selected by the user
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the oldne Master and get the port
            print ("Advertising topic: '" + self.topic + "' to oldne Master ....")
            port = self.__advertising_oldne(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode )
            print ("Topic registered by the oldne Master")

        ip = self.conf['ip']

        # Create a new ZeroMQ context and a publisher socket
        try:
            self.sock = nanomsg.Socket(nanomsg.PUB)
            
            if self.mode == "one2many":
                # This allows only use one publisher connected at the same endpoint
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)
            elif self.mode == "many2one":
                # This allows two use more that one publisher ate the same endpoint
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("publisher " + endpoint +  " connect")
                self.sock.connect(endpoint)
            elif  self.mode == "many2many":
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("publisher " + endpoint +  " connect")
            else:
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("publisher " + endpoint +  " bind")
                self.sock.bind(endpoint)
            time.sleep(1)
        except:
            print ("Socket in use")
            #TODO: restart connection
        
 
    def __advertising_oldne(self, node_name, topic, master_ip = '127.0.0.1', master_port = 7000, mode = "one2many"):
        
        """ Function used to register a publisher in P2P connection
                
        Parameters
        ----------
        node_name : string 
            Name of the node

        topic : string
            Topic to register

        master_ip : string 
            ip of the master node service

        master_port : int
            port of the master node service

        Returns
        ----------
        port : string
            Port used to connect the socket
        
        """

        c = client( master_ip, master_port, transport = "ZMQ")
        c.send_info({'node_name':node_name, 'topic':topic, 'mode':mode })
        response = c.listen_info()
        
        topic_id = response['topic']
        if(topic_id == topic):
            port = response['port']
        return port

    def __dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8).
        
        See jsonapi.jsonmod.dumps for details on kwargs.
        """

        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        

        if sys.version_info[0] == 2: #Python 2
            if isinstance(s, unicode):
                s = s.encode('utf8')
        return s


    def __serialization(self, message):
        """ Function used to serialize a python dictionary using json. In this function the message to be send is attached to the topic. 
            
            Parameters
            ----------
            message : dictionary
                Python dictionary to be send
            
            Returns
            -------
            message : string
                Message to be send, topic + message 
        """
        return self.topic + ' ' + self.__dumps(message)
            
    
    
    def send_string(self,message):
        """ Publish a string value. 
            
            Parameters
            ----------
            message : string 
                String to be sended

            Example
            ----------

            Send a string in a default ZMQ publisher

            .. code-block:: python

                import oldne
                new_node = oldne.node("dummy_node")
                configuration = new_node.config_sub() 
                pub = new_node.new_pub("dummy_topic", configuration)
                pub.send_string("hello")  
        """

        if self.transport ==  "ZMQ":
            self.sock.send_string(topic + ' ' + message)
        
        if self.transport ==  "NN" or self.transport ==  "nanomsg":
            self.sock.send(topic + ' ' + message)

        if self.transport == "ROS":
            self.ros_pub.publish(message)
            

    #Status: OK
    def send_info(self, message):
        """ Function used to publish a python dictionary. The message is serialized using json format and then published by the socket
            
            Parameters
            ----------
            message : dictionary 
                Python dictionary to be send
            debug : bool
                if == True, then it print the message to send

            Examples
            ----------

            Send a dictionary in a default ZeroMQ publisher:


            .. code-block:: python

                import oldne
                new_node = oldne.node("dummy_node")
                configuration = new_node.config_sub()
                pub = new_node.new_pub("dummy_topic", configuration)
                pub.send_info({'message':"hello"}) 


            Send a oldne_msg in a default ZeroMQ publisher:

            .. code-block:: python

                import oldne
                import oldne.oldne_msg
                new_node = oldne.node("dummy_node")
                configuration = new_node.conf_sub(msg_type = "vector") # oldne_msg definition
                pub = new_node.new_pub("dummy_topic", configuration)
                vector = oldne.vector(0,0,1)
                pub.send_info(vector)
            
            Send a oldne_msg in ROS publisher:

            .. code-block:: python

                import oldne
                import oldne.oldne_msg
                new_node = oldne.node("dummy_node", useROS=True)
                # ROS Vector3 definition
                configuration = new_node.conf_sub(msg_type = "vector", transport = "ROS")
                pub = new_node.new_pub("dummy_topic", configuration)
                vector = oldne.vector(0,0,1) 
                pub.send_info(vector) 

        """

        if self.transport ==  "ZMQ" or self.transport ==  "NN" or self.transport ==  "nanomsg":
            # TODO: if data es diferente a la definida poner un warning
            info = self.__serialization(message)

            if sys.version_info[0] == 2: #Python 2
                self.sock.send(info)
            else: # Python 3
                self.sock.send_string(info)

        
        if self.transport == "ROS":
        #TODO add try and except fot error of data

            if self.msg_type == "string":
                pub.publish(message)
            
            elif self.msg_type == "velocity":
                from geometry_msgs.msg import Twist
                twist = Twist()
                twist.linear.x = message.data['linear']['x']
                twist.linear.y = message.data['linear']['y']
                twist.linear.z = message.data['linear']['z']
                twist.angular.x = message.data['angular']['x']
                twist.angular.y = message.data['angular']['y']
                twist.angular.z = message.data['angular']['z']
                self.ros_pub.publish(twist)

            elif self.msg_type == "point":
                from geometry_msgs.msg import Point
                point = Point()
                point.x = message.data['x']
                point.y = message.data['y']
                point.z = message.data['z']
                self.ros_pub.publish(point)

            elif self.msg_type == "wrench":
                from geometry_msgs.msg import Wrench
                wrench = Wrench()
                wrench.force.x = message.data['force']['x']
                wrench.force.y = message.data['force']['y']
                wrench.force.z = message.data['force']['z']
                wrench.torque.x = message.data['torque']['x']
                wrench.torque.y = message.data['torque']['y']
                wrench.torque.z = message.data['torque']['z']
                self.ros_pub.publish(wrench)
                

            elif self.msg_type == "accel":
                from geometry_msgs.msg import Accel
                accel = Accel()
                accel.linear.x = message.data['linear']['x']
                accel.linear.y = message.data['linear']['y']
                accel.linear.z = message.data['linear']['z']
                accel.angular.x = message.data['angular']['x']
                accel.angular.y = message.data['angular']['y']
                accel.angular.z = message.data['angular']['z']
                self.ros_pub.publish(accel)

            elif self.msg_type == "quaternion":
                from geometry_msgs.msg import Quaternion
                quaternion = Quaternion()
                quaternion.x = message.data['x']
                quaternion.y = message.data['y']
                quaternion.z = message.data['z']
                quaternion.w = message.data['w']
                self.ros_pub.publish(quaternion)
                pass

            elif self.msg_type == "vector":
                from geometry_msgs.msg import Vector3
                vector = Vector3()
                vector.x = message.data['x']
                vector.y = message.data['y']
                vector.z = message.data['z']
                self.ros_pub.publish(vector)

            elif self.msg_type == "pose":
                from geometry_msgs.msg import Pose
                pose = Pose()
                pose.position.x = message.data['position']['x']
                pose.position.y = message.data['position']['y']
                pose.position.z = message.data['position']['z']
                pose.orientation.x = message.data['orientation']['x']
                pose.orientation.y = message.data['orientation']['y']
                pose.orientation.z = message.data['orientation']['z']
                pose.orientation.w = message.data['orientation']['w']
                self.ros_pub.publish(pose)
        


    
#Status: OK
class subscriber:
    """ Subscriber class used for inter-process comunication between nodes. 

        Parameters
        ----------
        topic : string 
            topic name to publish the messages

        node_name : string
            Name of the node 

        conf: dictionary
            Configuration of the subscriber

    """
    def __init__(self, topic, node_name = "default", conf =  {'transport': "ZMQ", 'network': "P2P", 'mode':"one2many", 'ip' : '127.0.0.1', 'type':'dict' }):
    
        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node_name = node_name
        self.topic = topic
        self.delimiter = " "

        if self.transport ==  "ZMQ":
            self.mode = self.conf['mode']
            self.__create_ZMQ_subscriber()

        elif self.transport ==  "NN" or self.transport ==  "nanomsg": #Use nanmsg

            self.NN_installed = False
            try:
                import nanomsg
                self.NN_installed = True
            except ImportError:
                print ("Nanomsg not installed")
                self.NN_installed = False

            if self.NN_installed == False:
                msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
                raise ValueError(msg)
                
            print ("New subscriber using nanomsg")
            self.mode = self.conf['mode']
            self.__create_NN_subscriber()

        
        elif self.transport ==  "ROS":
            self.__create_ROS_subscriber()



    def __create_ZMQ_subscriber(self):
        """Function used to create a ZeroMQ publisher"""
        if self.network == "direct":
            # Set the port selected by the user
            self.port = self.conf["port"]
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the oldne Master and get the port
            print ("Advertising topic (" + self.topic + ") to oldne Master ....")
            port = self.__advertising_oldne(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode)
            print ("Topic registered by the oldne Master")

        ip = self.conf['ip']
        endpoint = "tcp://" + ip + ":" + str(port)
        
            
        try:        
            # ZeroMQ Context
            self.context = zmq.Context()

            # Start a null social signal current state
            self.info = ""

            self.delimiter = " " #space delimiter for python, for C# is "\n"

            # Define the type of context, in this case a subcriber
            self.sock = self.context.socket(zmq.SUB)

            # Define subscription and the messages with prefix to accept.
            # setsockopt obtain the data which message starts with the second argument
            # Then we obtain data from the topic with that starts with topic_name value
            if sys.version_info[0] == 2:
                self.sock.setsockopt(zmq.SUBSCRIBE, self.topic)
            else:
                self.sock.setsockopt_string(zmq.SUBSCRIBE, self.topic)
           
            if self.mode == "many2one":
                # This allows only use one publisher connected at the same endpoint
                # print ("Multiple subscribers: OFF")
                self.sock.bind(endpoint)
                print ("subcriber " + endpoint +  " bind")
            elif self.mode == "one2many":
                # This allows two use more that one publisher ate the same endpoint
                # print ("Multiple subscribers: ON")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")

            elif  self.mode == "many2many":
                endpoint = "tcp://" + ip + ":" + str(port+1)
                # print ("many2many mode")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")

            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("subcriber " + endpoint +  " bind")
                self.sock.connect(endpoint)


        except:
            
            print("Socket already in use, restarting")
            self.sock.close()
            self.context.destroy()
            time.sleep(.2)
            self.context = zmq.Context()
            self.sock = self.context.socket(zmq.SUB)
            
            if sys.version_info[0] == 2:
                self.sock.setsockopt(zmq.SUBSCRIBE, self.topic)
            else:
                self.sock.setsockopt_string(zmq.SUBSCRIBE, self.topic)

            if self.mode == "many2one":
                # This allows only use one publisher connected at the same endpoint
                #print ("Multiple subscribers: OFF")
                print ("subcriber " + endpoint +  " bind")
                self.sock.bind(endpoint)
                # This allows two use more that one publisher ate the same endpoint
            elif self.mode == "one2many":
                #print ("Multiple subscribers: ON")
                print ("subcriber " + endpoint +  " connect")
                self.sock.connect(endpoint)
            elif  self.mode == "many2many":
                endpoint = "tcp://" + ip + ":" + str(port+1)
                #print ("many2many mode")
                self.sock.connect(endpoint)
                print ("subcriber " + endpoint +  " connect")
            else:
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("subcriber " + endpoint +  " bind")
                self.sock.connect(endpoint)

        print ("ZMQ subscriber started in " +  endpoint)


    def __create_NN_subscriber(self):
        """Function used to create a NN publisher"""

        if self.NN_installed == False:
            msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
            raise ValueError(msg)

        if self.network == "direct":
            self.port = self.conf['port']
            # Set the port selected by the user
            port = self.port
        elif self.network == "P2P":
            # Register the topic in the oldne Master and get the port
            print ("Advertising topic: '" + self.topic + "' to oldne Master ....")
            port = self.__advertising_oldne(self.node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, mode = self.mode )
            print ("Topic registered by the oldne Master")

        ip = self.conf['ip']

        # Create a new NN socket
        try:
            self.sock = nanomsg.Socket(nanomsg.SUB)
            self.sock.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, self.topic)

                       
            if self.mode == "many2one":
                # This allows only use one publisher connected at the same endpoint
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                #print ("Multiple subscribers: OFF")
                self.sock.bind(endpoint)
                print ("subscriber " + endpoint +  " bind")
            elif self.mode == "one2many":
                # This allows two use more that one publisher ate the same endpoint
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                #print ("Multiple subscribers: ON")
                self.sock.connect(endpoint)
                print ("subscriber " + endpoint +  " connect")

            elif  self.mode == "many2many":
                if ip == '127.0.0.1':
                    ip = "localhost"
                endpoint = "tcp://" + ip + ":" + str(port)
                endpoint = "tcp://" + ip + ":" + str(port+1)
                print ("many2many mode")
                self.sock.connect(endpoint)
                print ("subscriber " + endpoint +  " connect")

            else:
                if ip == '127.0.0.1':
                    ip = "*"
                endpoint = "tcp://" + ip + ":" + str(port)
                print ("WARNING: mode selected as:" + str(self.mode) + "it can be only: 'many2one' or  'one2many'")
                print ("Mode set as 'one2many'")
                print ("subcriber " + endpoint +  " bind")
                self.sock.connect(endpoint)

        except:
            print ("Socket in use")
            #TODO: restart connection


    #TODO: close for nanomsg
    def close_ZMQ_subscriber(self):
        """ This function closes the socket"""
        print ("close listener")
        self.sock.close()
        self.context.destroy()
        time.sleep(1)




    def __advertising_oldne(self, node_name, topic, master_ip = '127.0.0.1', master_port = 7000, mode = "one2many"):
        
        """Function used to register a publisher in P2P connections
                
        Parameters
        ----------
        node_name : string 
            Name of the node

        topic : string
            Topic to register

        master_ip : string 
            ip of the master node service

        master_port : int
            port of the master node service

        Returns
        ----------
        port : string
            Port used to connect the socket
        
        """

        c = client( master_ip, master_port, transport = "ZMQ")
        c.send_info({'node_name':node_name, 'topic':topic, 'mode':mode })
        response = c.listen_info()
        
        topic_id = response['topic']
        if(topic_id == topic):
            port = response['port']
        return port


    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8).
        
        See jsonapi.jsonmod.loads for details on kwargs.
        """

        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)


    
    #Status: OK
    def __deserialization(self, info):
        """ Separate the topic and the json message from the data received from the ZeroMQ socket. If the deserialization was successful and the message as a python dictionary
            
            Parameters
            ----------
            info : string
                topic + message received by the ZQM socket 

            Returns
            -------
            msg : string
                String message as a python dictionary
        """
        try:
            json0 = info.find('{')
            topic = info[0:json0].strip()
            msg = self.__loads(info[json0:])
            success = True
        except:
            msg = ""
            success = False
        return msg


    def listen_string(self, block_mode = False):
        
        """ Function used to read string data from the sokect. The operation is by default in non blocking mode

            Parameters
            ----------
            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------
            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            message : string 
                String received in the socket.      
        """

        if self.transport ==  "ZMQ" or self.transport ==  "NN" or self.transport ==  "nanomsg":
            message = ""
            try:
                #Blocking mode
                if block_mode:
                    # Get the message
                    if sys.version_info[0] == 2:
                        info = self.sock.recv()
                    else:
                        info = self.sock.recv_string()
                    # Split the message

                    index = info.find(' ')
                    topic = info[0:index].strip()
                    message = info[index:]
                    success = True
                #Non blocking mode
                else:
                    if self.transport ==  "ZMQ":
                        if sys.version_info[0] == 2:
                            info = self.sock.recv(flags = zmq.NOBLOCK)
                        else:
                            info = self.sock.recv_string(flags = zmq.NOBLOCK)
                            print (info)
                    elif self.transport ==  "NN" or self.transport ==  "nanomsg":
                        info = self.sock.recv(flags=nanomsg.DONTWAIT)
                        
                        
                    # Split the message
                    index = info.find(' ')
                    topic = info[0:index].strip()
                    message = info[index:]

                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass

            #Exeption for non blocking mode timeout
            except nanomsg.NanoMsgAPIError:
                #Nothing to read
                success = False
                pass

            return  success, message
        
            


    #Status: OK
    def listen_info(self,block_mode =  False):
        """ Listen for a json message. The operation is by default in non blocking mode
            
            Parameters
            ----------

            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------

            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            info : dictionary
                Message obtained
        """
        if self.transport ==  "ZMQ" or self.transport == "NN":    
            success = False
            info = {}
            try:
                #Blocking mode
                if block_mode:
                    info = self.__deserialization(self.sock.recv())
                    time.sleep(.001)
                    success = True
                #Non blocking mode
                else:
                    if self.transport ==  "ZMQ":
                        if sys.version_info[0] == 2:
                            info = self.__deserialization(self.sock.recv(flags = zmq.NOBLOCK))
                        else:
                            info = self.__deserialization(self.sock.recv_string(flags = zmq.NOBLOCK))

                    elif self.transport ==  "NN" or self.transport ==  "nanomsg":
                        info = self.__deserialization(self.sock.recv(flags=nanomsg.DONTWAIT))

                    time.sleep(.001)
                    success = True
            #Exeption for non blocking mode timeout
            except zmq.Again as e:
                #Nothing to read
                success = False
                pass

            #Exeption for non blocking mode timeout
            except nanomsg.NanoMsgAPIError:
                #Nothing to read
                success = False
                pass

            return  success, info



class broker():
    def __init__(self, IP, PORT_XPUB, PORT_XSUB):
        """
        Creates a XPUB/XSUB broker for many2many publisher-subcriber connections

        Parameters
        ----------

        IP : int 
            IP value of the broker

        PORT_XPUB : int 
            XPUB port. Which must be different that PORT_XSUB.

        PORT_XSUB : int 
            XSUB port. Which must be different that PORT_XPUB.

        """
        context = zmq.Context()
        frontend = context.socket(zmq.XSUB)
        frontend.bind("tcp://" + IP + ":" + str(PORT_XSUB))
        backend = context.socket(zmq.XPUB)
        backend.bind("tcp://" + IP + ":" + str(PORT_XPUB))
        zmq.proxy(frontend, backend)
        frontend.close()
        backend.close()
        context.term()

# TODO: sock.close() and context.destroy() must be set when a process ends
# In some cases socket handles won't be freed until you destroy the context.
# When you exit the program, close your sockets and then call zmq_ctx_destroy(). This destroys the context.
# In a language with automatic object destruction, sockets and contexts 
# will be destroyed as you leave the scope. If you use exceptions you'll have to
#  do the clean-up in something like a "final" block, the same as for any resource.


class server:
    def __init__(self, IP, port, transport = "ZMQ"):
        """
        Creates a new server object

        Parameters
        ----------

        IP : string
            IP value of server

        port : string
            Port used to connect the socket
            
        transport : string
            Define the transport layer of the server, can be 'ZMQ' or "normal", to use ZeroMQ or TCP/IP python sockets

        """
        
        self.transport = transport

        if transport == "ZMQ":

            try:
                # ZMQ sockets
                context = zmq.Context()
                # Define the socket using the "Context"
                self.sock = context.socket(zmq.REP)
                self.sock.bind("tcp://" + IP + ":" + str(port))
                print ("New ZMQ server in " + IP + ":" + str(port))
            except:
                print ("server socked reused")
                self.sock.close()
                context.destroy()
                time.sleep(2)
                context = zmq.Context()
                # Define the socket using the "Context"
                self.sock = context.socket(zmq.REP)
                self.sock.bind("tcp://" + IP + ":" + str(port))
                print ("New ZMQ server in " + IP + ":" + str(port))
        
        elif transport == "normal": 
            # Normal sockets
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.s.setblocking(0)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except:
                print ('Failed in creating socket')
                sys.exit();

            try:
                if IP == "localhost":
                #Same computer
                        IP = socket.gethostbyname( IP )
                        print ("local host in :", IP)
                
            except socket.gaierror:
                #could not resolve
                print ('Hostname could not be resolved. Exiting')
                sys.exit()
            #Connect to remote server
            self.s.bind(('' , int(port)))
            self.s.listen(5)
            print ("New normal server in " + IP + ":" + str(port))
            print ('Waiting for a connection')
            self.connection, client_address = self.s.accept()

    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8).
        
        See jsonapi.jsonmod.loads for details on kwargs.
        """

        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def __deserialization(self, info):
        """ JSON deserialization function  (string to dictionary)
            
            Parameters
            ----------
            info : string
                topic + message received by the ZQM socket 

            Returns
            -------
            info : dictionary
                Message as python dictionary
        """
        try:
            msg = self.__loads(info)
            success = True
        except:
            msg = ""
            success = False
        return msg

    def __dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8).
    
            See jsonapi.jsonmod.dumps for details on kwargs.
        """
        
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        
        if sys.version_info[0] == 2: #Python 2
            if isinstance(s, unicode):
                s = s.encode('utf8')
        
        return s


    #Status: OK
    def __serialization(self, message):
        """ Function used to serialize a python dictionary using json.
            
            Parameters
            ----------
            message : dictionary
                Python dictionary to be send
            
            Returns
            -------
            message : string
                Message to be send
        """
        return self.__dumps(message)

    def listen_info(self):
        """ Listen for a json message
                        
            Returns
            -------

            request : dictionary or string
                Message obtained
        """

        if self.transport == "ZMQ":
            #response = self.sock.recv_json()
            #return response
            request = self.sock.recv()
            return self.__deserialization(request)
            
        else:
            # Wait for a connection
            try:
                request = self.connection.recv(16)
                return request
            except:
                self.connection.close()
                self.connection, client_address = self.s.accept()
                request = self.connection.recv(16)
                return request

    def send_info(self,response):
        """ Function used to send client response as a python dictionary  (if transport == "ZMQ") or as string (if transport == "normal")
            
            Parameters
            ----------

            response : dictionary or string
                    Python dictionary (ZMQ) or string (Python sockets) to be send

        """
        
        if self.transport == "ZMQ":
            #self.sock.send_json(response)
            if sys.version_info[0] == 2:
                self.sock.send(self.__serialization(response))
            else:
                self.sock.send_string(self.__serialization(response))
        else:
            try:
               self.connection.sendall(response)
            except:
                print ("ERROR: for normal socket messages must be string not dictionaries" )
                sys.exit()


class client:
    def __init__(self, IP, port, transport = "ZMQ"):
        """
        Creates a new client object

        Parameters
        ----------

        IP : string
            IP value of server

        port : string
            Port used to connect the socket
            
        transport : string
            Define the transport layer of the server, can be 'ZMQ' or "normal", to use ZeroMQ or TCP/IP python sockets

        """
        
        
        self.transport = transport
        if self.transport == "ZMQ":
            context = zmq.Context()
            # Define the socket using the "Context"
            self.sock = context.socket(zmq.REQ)
            self.sock.connect("tcp://" + IP + ":" + str(port))
            print ("New ZMQ client in " + IP + ":" + str(port))

        elif transport == "normal":

            # Normal sockets
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error:
                print ('Failed creating socket')
                sys.exit();

            try:
                if IP == "localhost":
                #Same computer
                        IP = socket.gethostbyname( IP )
                        print ("local host in :", IP)
                
            except socket.gaierror:
                #could not resolve
                print ('Hostname could not be resolved. Exiting')
                sys.exit()
            #Connect to remote server
            max_v = 10
            i = 0
            connect=False
            while not connect:
                try: 
                    self.s.connect((IP , int(port)))
                    print ("New normal client in " + IP + ":" + str(port))
                    connect = True
                except:
                    print ("Server not found intent:" + str(i) + ", max = 10")
                    time.sleep(2)
                    i = i + 1
                    if i > max_v-1:
                        print ("Server not found after max number of intents")
                        time.sleep(4)
                        sys.exit()
                        



    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8).
        
        See jsonapi.jsonmod.loads for details on kwargs.
        """
        
        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def __deserialization(self, info):
        """ 
            Parameters
            ----------
            info : string
                topic + message received by the ZQM socket 

            Returns
            -------
            msg : string
                String message as a python dictionary
        """
        try:
            msg = self.__loads(info)
        except:
            msg = ""
        return msg

    def __dumps(self,o, **kwargs):
        """ JSON deserialization function  (string to dictionary)
            
            Parameters
            ----------
            info : string
                Message received by the ZQM socket 

            Returns
            -------
            info : dictionary
                Message as python dictionary
        """
        
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        

        if sys.version_info[0] == 2: #Python 2
            if isinstance(s, unicode):
                s = s.encode('utf8')
        return s


    #Status: OK
    def __serialization(self, message):
        """ Function used to serialize a python dictionary using json. 

            Parameters
            ----------
            message : dictionary
                Python dictionary to be send
            
            Returns
            -------
            message : string
                Message to be send
        """
        return self.__dumps(message)



    def listen_info(self):
        """ Listen for a json message
                        
            Returns
            -------

            response : dictionary or string
                Message obtained
        """
        
        if self.transport == "ZMQ":
            #response = self.sock.recv_json()
            #return response
            response = self.sock.recv()
            return self.__deserialization(response)
            
        else:
          response = self.s.recv(1024)
          return response
            

    def send_info(self,request):
        
        """ Function used to send client request as a python dictionary  (if transport == "ZMQ") or as string (if transport == "normal")
            
            Parameters
            ----------

            request : dictionary or string
                    Python dictionary (ZMQ) or string (Python sockets) to be send

        """

        if self.transport == "ZMQ":
            #self.sock.send_json(request)
            if sys.version_info[0] == 2:
                self.sock.send(self.__serialization(request))
            else:
                self.sock.send_string(self.__serialization(request))

        else:
            try:
                self.s.sendall(request)
            except:
                print ("ERROR: for normal socket messages must be string not dictionaries")
                sys.exit()

class surveyor():
    
        def __init__(self, topic, timeout = 1000):
            
            """ Nanomsg surveyor class
            
            Parameters
            ----------

            topic : string
                Surveyor topic

            timeout : int
                Maximun miliseconds waiting for response

            """

            ip = "127.0.0.1"
            port = self.__advertising_oldne(topic)

            self.NN_installed = False
            try:
                import nanomsg
                self.NN_installed = True
            except ImportError:
                print ("Nanomsg not installed")
                self.NN_installed = False

            if self.NN_installed == False:
                msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
                raise ValueError(msg)
                
            self.sock = nanomsg.Socket(nanomsg.SURVEYOR)
            endpoint = "tcp://" + ip + ":" + str(port)
            self.sock.bind(endpoint)
            self.sock.set_int_option(nanomsg.SURVEYOR, nanomsg.SURVEYOR_DEADLINE, timeout)
            time.sleep(1)
            print ("oldne surveyor started in: " + str(endpoint))

        def __advertising_oldne(self, topic, master_ip = '127.0.0.1', master_port = 7000, mode = "surveyor"):
            
            """Function used to register a publisher in P2P connections
                    
            Parameters
            ----------

            topic : string
                Topic to register

            master_ip : string 
                ip of the master node service

            master_port : int
                port of the master node service

            Returns
            ----------
            port : string
                Port used to connect the socket
            
            """

            c = client( master_ip, master_port, transport = "ZMQ")
            c.send_info({'node_name':topic, 'topic':topic, 'mode':mode })
            response = c.listen_info()
            
            topic_id = response['topic']
            if(topic_id == topic):
                port = response['port']
            return port

        def __dumps(self,o, **kwargs):
            """ Serialize object to JSON bytes (utf-8).
                
                See jsonapi.jsonmod.dumps for details on kwargs.
            """

            if 'separators' not in kwargs:
                kwargs['separators'] = (',', ':')
        
            s = simplejson.dumps(o, **kwargs)
            
            if sys.version_info[0] == 2: #Python 2
                if isinstance(s, unicode):
                    s = s.encode('utf8')
            return s

        #Status: OK
        def __serialization(self, message):
            """ Function used to serialize a python dictionary using json. 

                Parameters
                ----------
                message : dictionary
                    Python dictionary to be send
                    
                Returns
                -------
                message : string
                    Message to be send
            """
            return self.__dumps(message)
            
    

        def send_info(self, message):
            """ Function used to send a python dictionary.
                    
                Parameters
                ----------
                message : dictionary 
                    Python dictionary to be send

            """

            info = self.__serialization(message)
            self.sock.send(info)


        def __loads(self, s, **kwargs):
            """Load object from JSON bytes (utf-8).
                
            See jsonapi.jsonmod.loads for details on kwargs.
            """

            if sys.version_info[0] == 2:
                if str is unicode and isinstance(s, bytes):
                    s = s.decode('utf8')
        
            return simplejson.loads(s, **kwargs)
                

    
        #Status: OK
        def __deserialization(self, info):
            """ Deserialization string to dictionary

                Parameters
                ----------
                info : string
                        Message received 

                Returns
                -------
                msg : dictionary
                    String message as a python dictionary
            """
            try:
                json0 = info.find('{')
                topic = info[0:json0].strip()
                msg = self.__loads(info[json0:])
                success = True
            except:
                msg = ""
                success = False
            return msg


       


        #Status: OK
        def listen_info(self):
            """ Listen for a json message
                        
                Returns
                -------
                success: bool
                    True if a message arrives before the timeout, otherwise return false

                info : dictionary
                    Message obtained
            """
          
            while True:
                    try:
                            info = self.__deserialization(self.sock.recv())
                            return True, info

                    #Exeption for non blocking mode timeout
                    except nanomsg.NanoMsgAPIError:
                            return  False, {}

         
        
        def close(self):
            """Close socket """
            self.sock.close()




class respondent():
        
        def __init__(self, topic):
            
            """ Nanomsg surveyor class
            
            Parameters
            ----------

            topic : string
                Topic to exchange info

            """

            ip = "127.0.0.1"
            port = self.__advertising_oldne(topic)

            self.NN_installed = False
            try:
                import nanomsg
                self.NN_installed = True
            except ImportError:
                print ("Nanomsg not installed")
                self.NN_installed = False

            if self.NN_installed == False:
                msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
                raise ValueError(msg)

            
            self.sock = nanomsg.Socket(nanomsg.RESPONDENT)
            endpoint = "tcp://" + ip + ":" + str(port)
            self.sock.connect(endpoint)
            time.sleep(1)
            print ("oldne respondent started in: " + str(endpoint))

        def __advertising_oldne(self, topic, master_ip = '127.0.0.1', master_port = 7000, mode = "surveyor"):
            
            """Function used to register a publisher in P2P connections
                    
            Parameters
            ----------

            topic : string
                Topic to register

            master_ip : string 
                ip of the master node service

            master_port : int
                port of the master node service

            Returns
            ----------
            port : string
                Port used to connect the socket
            
            """

            c = client( master_ip, master_port, transport = "ZMQ")
            c.send_info({'node_name':topic, 'topic':topic, 'mode':mode })
            response = c.listen_info()
            
            topic_id = response['topic']
            if(topic_id == topic):
                port = response['port']
            return port
              
        def __dumps(self,o, **kwargs):
            """Serialize object to JSON bytes (utf-8).
                
            See jsonapi.jsonmod.dumps for details on kwargs.
            """

            if 'separators' not in kwargs:
                kwargs['separators'] = (',', ':')
        
            s = simplejson.dumps(o, **kwargs)
            

            if sys.version_info[0] == 2: #Python 2
                if isinstance(s, unicode):
                    s = s.encode('utf8')
            return s


        #Status: OK
        def __serialization(self, message):
            """ Function used to serialize a python dictionary using json. 

                Parameters
                ----------
                message : dictionary
                    Python dictionary to be send

                    
                Returns
                -------
                message : string
                    Message to be send, topic + message 
            """
            return self.__dumps(message)
            
    

        def send_info(self, message):
            """ Function used to send a python dictionary.
                    
                Parameters
                ----------
                message : dictionary 
                    Python dictionary to be send

            """

            info = self.__serialization(message)
            self.sock.send(info)


        def __loads(self, s, **kwargs):
            """Load object from JSON bytes (utf-8).
                
            See jsonapi.jsonmod.loads for details on kwargs.
            """

            if sys.version_info[0] == 2:
                if str is unicode and isinstance(s, bytes):
                    s = s.decode('utf8')
        
            return simplejson.loads(s, **kwargs)


    
        #Status: OK
        def __deserialization(self, info):
            """ JSON deserialization function
                    
                Parameters
                ----------
                info : string
                    message received

                Returns
                -------
                info : dictionary
                    Message as python dictionary
            """
            try:
                json0 = info.find('{')
                topic = info[0:json0].strip()
                msg = self.__loads(info[json0:])
                success = True
            except:
                msg = ""
                success = False
            return msg


       


        #Status: OK
        def listen_info(self, block_mode = False):
            """ Listen for a json message
                        
                Returns
                -------

                info : dictionary
                    Message obtained
            """
          
            if block_mode:#TODO, change s, data= ....
                info = self.__deserialization(self.sock.recv())
                return  True, info
            else:
                try:
                     info = self.__deserialization(self.sock.recv(flags=nanomsg.DONTWAIT))
                     return True, info
                except nanomsg.NanoMsgAPIError:
                    return  False, {}


         
        
        def close(self):
            """Close socket """
            self.sock.close()
                
if __name__ == "__main__":
    import doctest
    doctest.testmod()

# Which is better?
# From ZeroMQ v3.x, filtering happens at the publisher side when using a
#  connected protocol (tcp:// or ipc://). Using the epgm:// protocol,
#  filtering happens at the subscriber side.
#  In ZeroMQ v2.x, all filtering happened at the subscriber side.
