import nep
import time
from datetime import datetime
import sys, os


class sharo:

    def __init__(self, perception_model, forgot_time = 5, use_ros = False, use_ros2 = False, exit_signal = False):
        print ("SHARO STARTING ... ")
        self.datalog = []
        self.node = nep.node("sharo","ZMQ",exit_signal)
        self.sharo_sense = self.node.new_sub("/blackboard", "json")                # Get perceptual data
        self.sharo_pub = self.node.new_pub("/sharo", "json")                       # Pub active behaviors 
        self.model = perception_model
        self.active_behaviors = []
        self.cancel_behaviors = [] 
        self.behaviors = []
        self.run = True

        # Variables used for simple speech recognition tools
        self.current_word = ""
        self.current_word_time = time.time()

        self.forgot_time = forgot_time

        self.resetBlackboard()

        if use_ros:
            # Launch ros nodes
            pass
        if use_ros2:
            # Launch ros nodes
            pass

        if sys.version_info[0] == 3:
            import _thread as thread
            thread.start_new_thread(self.update_short_memory_py3, ())
            thread.start_new_thread(self.sense, ())
        else:
            import thread
            thread.start_new_thread(self.update_short_memory_py2, ())
            thread.start_new_thread(self.sense, ())

    def resetBlackboard(self):
        current_time = time.time()
        for key_m, value_m in self.model.iteritems():
            for key, value in self.model[key_m].iteritems():
                self.model[key_m][key]["time"] = current_time

    def sense(self):
        print ("READY TO GET DATA FROM PERCEPTIONS")
        while self.run:
            time.sleep(.001)
            s, msg = self.sharo_sense.listen()
            if s:
                print msg
                self.proccessInput(msg)



    def proccessInput(self,msg):

        node = msg["node"]                          # Is a perception or action node?
        timestamp = datetime.now().isoformat()      # Time stamp of this primitive in human rediable format
        current_time = time.time()                  # Current time in machine format
        msg["timestamp"] = timestamp
        msg["time"] = current_time

        if node == "perception":
            self.proccessPerception(msg, current_time)
        

        self.datalog.append(msg)   # Add to logger



    def proccessPerception(self,msg, current_time):
    
        input_ = msg["input"]                       # Action add, update or clear 
        primitive = msg["primitive"]                # Main primtive class 
        robot = msg["robot"]                        # Robot presenting this primitive
        parameters = msg["parameters"]              # Specific parameters values of this primitive

        
        if primitive in self.model:                 # Is primitive in model?
            for key_m, value_m in parameters.iteritems():
                if key_m in self.model[primitive]:   # Is primitive in the model
                    if input_ == "add":
                        self.model[primitive][key_m]["value"] = value_m
                        self.model[primitive][key_m]["time"] = current_time
                    if input_ == "delete":
                        self.model[primitive][key_m]["value"] = 0
                        
        self.datalog.append(msg)   # Add to logger

    
    def update_short_memory_py2(self): # Forgot perceptual inputs after some seconds (Python 2 implementation)

        while self.run:
            time.sleep(1)
            current_time = time.time()
            if (self.current_word_time - current_time) > self.forgot_time:
                self.current_word = ""

            for key_m, value_m in self.model.iteritems():
                for key, value in self.model[key_m].iteritems():
                    
                    primitive_time = self.model[key_m][key]["time"]
                    diference = abs(current_time - primitive_time) 
                    
                    if diference > self.forgot_time:
                        self.model[key_m][key]["value"] = 0


    def update_short_memory_py3(self): # Forgot perceptual inputs after some seconds (Python 2 implementation)

        while self.run:
            time.sleep(.1)
            current_time = time.time()

            current_time = time.time()
            if (self.current_word_time - current_time) > self.forgot_time:
                self.current_word = ""

            for key_m, value_m in self.model.items():
                for key, value in self.model[key_m].items():
                    primitive_time = self.model[key_m][key]["time"]
                    if (primitive_time - current_time) > self.forgot_time:
                        self.model[key_m][key]["value"] = 0




    def checkPrimitive(self, primitive, _input):

        if primitive in self.model: 
            if _input in self.model[primitive]:
                if type(self.model[primitive][_input]["value"]) == bool:
                    if self.model[primitive][_input]["value"] == True:
                        return True
                else:
                    if self.model[primitive][_input]["value"] > 0.5:
                        return True

        elif primitive == "word": #For speech check unicode
            r_memory_encoded = str(self.model[primitive][_input]["value"].encode('utf8'))      
            if _input.encode('utf8') == r_memory_encoded:
                return True
            else:      
                return False                 

        return False

        

    def share(self):
        while self.run:
            time.sleep(.1) 
            self.sharo_pub.publish({"active":self.active_behaviors, "cancel":self.cancel_behaviors})


    def update_active_behaviors(self):
        import nepki
        self.bt = nepki.engine()
        while True:
            self.bt.blackboard = self.model
            for b in self.behaviors: 
                result = self.bt.tick(b)




                
               
