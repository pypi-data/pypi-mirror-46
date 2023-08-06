import kapuccino
import nep
from random import randint
import copy 


#TODO: delate activation parameter

class btree():
    def __init__(self, middleware = "nanomsg", exit_signal = False):
        """
        Behavior Tree main class.

        Parameters
        ----------

        middleware : string
            Can be "nanomsg", "ZMQ", "ROS" or "ROS2"

        """
        
        self.current_state = "running"
        self.exit = True
        self.next = False
        self.action_manager = kapuccino.action(middleware, exit_signal)


    
    def setBlackboard(self, perception_model = {}, forgot_time = 5, use_ros = False, use_ros2 = False):
        self.blackboard = kapuccino.sharo(perception_model, forgot_time, use_ros, use_ros2)

            
    def tick(self,node, activate = False):
        node_type =  node["node"]

        if activate:
            if node_type == "action":
                if node["state"] == "running":
                    node["state"] = "active"

        if node_type == "condition":
            return self.runCondition(node)

        elif node["state"] == "active" or node["state"] == "running":
            
            if node_type == "sequence":
                return self.runSequence(node,activate)
            
            elif node_type == "selector":
                return self.runSelector(node,activate)

            elif node_type == "action":
                return self.runAction(node)

            elif node_type == "cancel":
                return self.runCancel(node)

            elif node_type == "random_selector":
                return self.runRandomSelector(node,activate)

            elif node_type == "always_failure":
                return self.runAlwaysFailure(node,activate)

            elif node_type == "negation":
                return self.runNegation(node,activate)

    # ------------- Condition code  --------------

    def runCondition(self,node):
        primitive = node["primitive"]
        input_ = node["input"]
        return self.blackboard.checkPrimitive(primitive, input_)

    # ------------- Run or cancel some action --------------

    def runAction(self,node):
        print ("Action to do: " + node["id"])
        response = self.action_manager.check(node, "action")
        #print (response)
        if response == "running":
            if node["state"] == "active":
                print ("Action now in execution")
            print ("running")
            self.setNodeRunning(node)
        elif response == "pending":
            print ("Action waiting for execution")
            response = "running"
        elif response == "failure":
            self.setNodeFailure(node)
            print  ("Action returned: " + str(response)) 
        elif response == "success":
            self.setNodeSuccess(node)
            print  ("Action returned: " + str(response)) 
        elif response == "error":
            self.setNodeError(node)
            print  ("Action returned: " + str(response))
        else:
            response = "error"

        return response

    def runCancel(self,node):
        response = self.action_manager.check(node, "cancel")
        return response


    # ------------- Inner nodes code --------------

    def runSequence(self,node,activate):
        children = node["children"]

        if type(children) is list:

            for child in children:
                response = self.tick(child,activate) # Get response from child
                if response == "success":
                    pass
                elif response == "running":
                    return response # Return exit and "running" state
                elif response == "failure":
                    self.setNodeFailure(node)
                    return  response
                elif response == "error":
                    self.set_node#rror(node)
                    return response
        else:
            response = self.tick(children,activate) # Get response from child
            if response == "success":
                pass
            elif response == "running":
                self.setNodeRunning(node) #Set parent in "running"
                return response # Return exit and "running" state
            elif response == "failure":
                self.setNodeFailure(node)
                return  response
            elif response == "error":
                self.setNodeError(node)
                return response
            
        self.setNodeSuccess(node)
        return "success"

    def runSelector(self,node,activate):

        children = node["children"]
        if type(children) is list:
            for child in children:
                response = self.tick(child,activate) # Get response from child
                if response == "success":
                    self.setNodeSuccess(node) 
                    return  response
                elif response == "running":
                    self.setNodeRunning(node) #Set parent in "running"
                    return response # Return exit and "running" state
                elif response == "failure":
                    pass
                elif response == "error":
                    self.setNodeError(node)
                    return response

        elif type(children) is dict:
            children = [children]

            response = self.tick(child,activate) # Get response from child

            if response == "success":
                self.setNodeSuccess(node) 
                return  response
            elif response == "running":
                self.setNodeRunning(node) #Set parent in "running"
                return response # Return exit and "running" state
            elif response == "failure":
                pass
            elif response == "error":
                self.setNodeError(node)
                return response
        self.setNodeFailure(node)
        return "failure"


    def runRandomSelector(self,node,activate):
        children = node["children"]
        if node["n"] == "none":
            n_child = len(children)
            n_selected = randint(0, n_child-1)
            node["n"] = n_selected 
        response = self.tick(children[node["n"]],activate)
        if response == "running":
            self.setNodeRunning(node)
            return response
        elif response == "success":
            self.setNodeSuccess(node)
            node["n"] = "none"
            return response
        elif response == "failure":
            self.setNodeFailure(node)
            node["n"] = "none"
            return response               

    def runAlwaysFailure(self,node,activate):
        children = node["children"]
        child = children[0]
        response = self.tick(child, activate)
      
        if response == "running":
            self.setNodeRunning(node)
            return response
        else:
            self.setNodeFailure(node)
            return "failure"
        return "error"

    def runNegation(self,node,activate):
        children = node["children"]
        child = children[0]
        response = self.tick(child, activate)
      
        if response == "running":
            self.setNodeRunning(node)
            return response
        elif response == "success":
            self.setNodeFailure(node)
            return "failure"
        else:
            self.setNodeSuccess(node)
            return "success"
        return "error"


    # ----------------- Set node status ------------------

    def setNodeRunning(self,node):
        # Set the node with running state
        node["state"] = "running"

    def setNodeSuccess(self,node):
        # Set the node with succeess state
        node["state"] = "success"

    def setNodeFailure(self,node):
        # Set the node with succeess state
        node["state"] = "failure"

    def setNodeError(self,node):
        # Set the node with error state
        print ("ERROR: in")
        node["state"] = "error"


