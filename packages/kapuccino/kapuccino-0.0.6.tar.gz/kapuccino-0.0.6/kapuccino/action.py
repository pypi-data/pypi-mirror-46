#!/usr/bin/env python

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Autor: Luis Enrique Coronado Zuniga


import nep
import time
            
class action():
    
    def __init__(self, robot_middleware = "ZMQ", exit_signal = False):

        """
        Link class used to communicate with robots and the blackboard

        Parameters
        ----------

        robot_middleware: string
            Middleware used for communication with robots, can be "ZMQ" (using client-server), "nanomsg" (using surveyor pattern), "ROS" (using actionlib) or "ROS2" (using actionlib)


        """

        self.goals = {}
        # NEP node definition
        self.node = nep.node("robot_manager","ZMQ", exit_signal) # Node manager
        self.robot_middleware = robot_middleware

        # Survey pattern error counter
        self.blackboard_error_counter = 0 # Communnication errors with blackboard
        self.robot_error_counter = 0 # Comunication errros with robots

        if self.robot_middleware == "nanomsg":
            deadline = 1000
            self.sur = nep.surveyor('action_survey',deadline)     # Robot Action Manager and Monitor
            time.sleep(1)
        elif self.robot_middleware == "ZMQ":
            self.client = self.node.new_client("action_server")
            time.sleep(1)

        elif self.robot_middleware == "ROS":
            pass
        
        elif self.robot_middleware == "ROS2":
            pass


    def send_request(self, node, node_type):

        if node_type == "action" or node_type == "cancel": 
            if self.robot_middleware == "nanomsg":
                self.sur.send_json(node)
            elif self.robot_middleware == "ZMQ":
                self.client.send_info(node)
            elif self.robot_middleware == "ROS":
                pass
        else:
            if self.robot_middleware == "nanomsg":
                self.sur_cond.send_json(node)
            elif self.robot_middleware == "ZMQ":
                self.client_cond.send_info(node)
            elif self.robot_middleware == "ROS":
                pass



    def get_response(self, node_type):
        if node_type == "action" or node_type == "cancel": 
            if self.robot_middleware == "nanomsg":
                s, msg = self.sur.listen_json()           
                return s, msg

            elif self.robot_middleware == "ZMQ":
                msg = self.client.listen_info()
                s = True
                return s, msg
        else:
            if self.robot_middleware == "nanomsg":
                for i in range(3):
                    s, msg = self.sur_cond.listen_json()
                    if s:
                        return s, msg
                    else:   # Try restarting the surveyor
                        print ("Restaring surveyor ...")
                        self.sur_cond.close()
                        deadline = 1000
                        self.sur_cond = nep.surveyor('/blackboard',deadline)     
                        time.sleep(1)

            elif self.robot_middleware == "ZMQ":
                msg = self.client_cond.listen_info()
                s = True
                return s, msg

        return False, {}




    # --------------------------------------------- check function -----------------------------------------------
    def check(self, node, node_type = "action"):
        """
        Send request and get response of execution (to an action engine)

        Parameters
        ----------
        node : dictionary
            node to be executed or checked
        node_type : string
            Type of the operation to perform, "action" to execute or "condition" to check

            
        Returns
        ----------
        response : string
            State of the action or condition execution
        """

        if not node_type == "cancel": 
            if len(node['primitives']) == 0:            # Is primitives field null?
                    return "success"


        for i in range(100):
            self.send_request(node, node_type)
            s, msg = self.get_response(node_type)

            if s:
                response = msg["node"]
                return response

        print ("ERROR: not response from robot")
        return "error"


if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
