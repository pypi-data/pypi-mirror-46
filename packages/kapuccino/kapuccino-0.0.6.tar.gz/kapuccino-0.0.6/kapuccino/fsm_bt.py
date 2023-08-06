#!/usr/bin/env python

# ------------------------ BlockEngine --------------------------------

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Autor: Luis Enrique Coronado Zuniga

import kapuccino
import time
import nep
import copy
import os
from transitions import Machine


class Matter(object):
    pass            

class fsm_bt():
        
    def __init__(self, blackboard_model = {}, middleware = "nanomsg"):
        """
        Class for execution of block-based programs using Behavior Trees

        Parameters
        ----------
        blackboard_model : dict
            Blackboard model used

        """

        self.bt = kapuccino.btree(middleware)
        self.bt.setBlackboard(blackboard_model)
        
        self.tick_time = 0.1      # Iteration time of BT engine
        self.goal_times = {}            # Goal manager time
        self.reactions_times = {}       # Reaction manager time
        self.goals = []                 # Goal list to process
        self.reactions = []             # Reaction list to process

        self.on = True                  # While True, program will be executed in a loop
        self.pause = False              # While True be in idle
        self.stop = True                # Reset goals and reactions

        self.active_reaction = {}
        self.active_goal = {}

        self.dict_reactions = {}
        self.dict_goals = {}
        self.current_goal = {}

        self.reaction_running = False
        self.goal_running = False
        self.goal_canceled = False
        self.lump = Matter()
        self.states=['idle', 'goal', 'reaction', 'cancel_goal','continue_goal']

        # And some transitions between states. We're lazy, so we'll leave out
        # the inverse phase transitions (freezing, condensation, etc.).
        self.transitions = [
            { 'trigger': 'ex_reaction', 'source': 'idle', 'dest': 'reaction' },
            { 'trigger': 'ex_reaction', 'source': 'goal', 'dest': 'reaction' },
            { 'trigger': 'ex_goal', 'source': 'idle', 'dest': 'goal' },
            { 'trigger': 'continue_goal', 'source': 'reaction', 'dest': 'continue_goal' },
            { 'trigger': 'return_goal', 'source': 'continue_goal', 'dest': 'goal' },
            { 'trigger': 'return_goal', 'source': 'reaction', 'dest': 'goal' },
            { 'trigger': 'return_idle', 'source': 'reaction', 'dest': 'idle' },
            { 'trigger': 'return_idle', 'source': 'goal', 'dest': 'idle' },
            { 'trigger': 'return_idle', 'source': 'cancel_goal', 'dest': 'idle' },
            { 'trigger': 'cancel_goal', 'source': 'goal', 'dest': 'cancel_goal'},

        ]


        self.machine = Machine(self.lump, states=self.states, transitions=self.transitions, initial='idle')


    def checkActiveBehaviors(self,lista):
        active = {}
        for l in lista:
            result = self.bt.tick(l["activate"])    # Check active conditionals
            if result:
                active[l["name"]] = l["utility"]    # Get utility   
        return sorted(active)

    def ModuleProgram(self, folder, name, type_):

        reactions_list = []
        goals_list = []
        try:
            if type_ == "reaction":
                reactions = nep.getFiles(folder + "/reaction/json/")
                for r in reactions: # Create a list of reactions
                    reaction = nep.read_json(folder + "/reaction/json/" + r) 
                    temp_dict = nep.json2dict(reaction)
                    if name == temp_dict["name"]:
                        reactions_list.append(temp_dict)
                        self.dict_reactions[temp_dict["name"]] = temp_dict
                        #print ("Using: reaction_" + temp_dict["name"])
            
            elif type_ == "goal":
                goals = nep.getFiles(folder + "/goal/json/")
                for g in goals: # Create a list of goals
                    goal = nep.read_json(folder + "/goal/json/" + g) 
                    temp_dict = nep.json2dict(goal)
                    if name ==  temp_dict["name"] :
                        goals_list.append(temp_dict)
                        self.dict_goals[temp_dict["name"]] = temp_dict
                        #print ("Using: goal_" + temp_dict["name"])

            self.goals = goals_list
            self.reactions = reactions_list
        except:
            pass

        return reactions_list, goals_list


    def loadProgram(self, folder):
        """
        Load a program from json files (goals and reactions)

        Parameters
        ----------
        folder : string
            path to the folder of the program


        Returns
        ----------
        reaction_list : list
            List of json files that represent the robot reactions

        goal_list : list
            List of json files that represent the robot goals

        """

        reactions_list = []
        goals_list = []


        try:
            reactions = nep.getFiles(folder + "/reaction/json/")
            goals = nep.getFiles(folder + "/goal/json/")

            print ("Available reactions:" +  str(onlyfiles))
            print ("Available goals:" +  str(onlyfiles))


            for r in reactions: # Create a list of reactions
                reaction = nep.read_json(folder + "/reaction/json/" + r) 
                temp_dict = nep.json2dict(reaction)
                reactions_list.append(temp_dict)
                self.dict_reactions[temp_dict["name"]] = temp_dict

            for g in goals: # Create a list of goals
                goal = nep.read_json(folder + "/goal/json/" + g) 
                temp_dict = nep.json2dict(goal)
                goals_list.append(temp_dict)
                self.dict_goals[temp_dict["name"]] = temp_dict

            self.goals = goals_list
            self.reactions = reactions_list
        except:
            pass

        return reactions_list, goals_list

    def set_goal_time(self,node):
        name = node["name"]
        if name in self.dict_goals[name]:
            value = self.dict_goals[name]
            value["time"] = time.time()
        return "success"

    def set_reaction_time(self,node):
        name = node["name"]
        if name in self.dict_reactions[name]:
            value = self.dict_reactions[name]
            value["time"] = time.time()
        return "success"


    def runAction(self, action):
        """
        Run a simple action task

        Parameters
        ----------
        action : dictionary
            Action definition in JSON format (dictionary)
        """

        result = "running"
        while result == "running":
            result = self.doStep(action, "reaction")

    def checkActivateConditionals(self,node_type):
        """
        Check if some condition is met 

        Parameters
        ----------
        node_type : string
            Can be "reaction" or "goal"

        Returns
        ----------
        active : list
            List of active behaviors
        """
        
        if node_type == "reactions":
            reactive_list = self.checkTimeConstrain(self.reactions)
            active = self.checkActiveBehaviors(reactive_list)
            return active

        elif node_type == "goals":
            goal_list = self.checkTimeConstrain(self.goals)
            active = self.checkActiveBehaviors(goal_list)
            return active

    def checkTimeConstrain(self, behaviors):

        lista = []
        since = time.time()
        for b in behaviors:
            time_ = since - b["time"]

            if (int(time_) >= int(b["period"])):
                lista.append(b)

        return lista
    
    def checkCancelConditional(self):
        """
        Check if the condition to cancel current goal is met

        Returns
        ----------
        status : string
            Can be "success" or "failure"
        """
        if len (self.current_goal["cancel"]) == 0:
            return "failure"
        else:
            result = self.bt.tick(self.current_goal["cancel"])
            if result == True:   
                return "success"
            else:
                return "failure" 


    def managment(self):

        time.sleep(2)
        print ("Starting managment of behaviors")
        while True:
            time.sleep(.5)
            """thread worker function"""
            if self.lump.state == "idle":
                
                goals =  self.checkActivateConditionals("goals")
                if len(goals) > 0:
                    goal = goals[0]
                    self.current_goal = copy.deepcopy(self.dict_goals[goal])
                    self.set_goal_time(self.current_goal)
                    self.lump.ex_goal()
                else:
                    reactions =  self.checkActivateConditionals("reactions")
                    if len(reactions) > 0:

                        reaction = reactions[0]
                        self.current_reaction = copy.deepcopy(self.dict_reactions[reaction])
                        self.set_reaction_time(self.current_reaction)
                        self.lump.ex_reaction()



            if self.lump.state == "reaction":
                print self.current_reaction["activate"]
                response = self.doStep(self.current_reaction["bt"],"reaction")
                if response == "success" or response == "failure":
                    if not len (self.current_goal) == 0:
                        self.return_bt = copy.deepcopy(self.current_goal ["return_bt"])
                        self.lump.continue_goal()
                        time.sleep(.001)
                    else:
                        self.lump.return_idle()
                        time.sleep(.001)
                

            if self.lump.state == "continue_goal":
                if "return_bt" in self.current_goal:
                    response = self.doStep(self.return_bt, "goal")
                    if response == "success" or response == "failure":
                            self.activateLastGoalAction(self.current_goal ["bt"])
                            self.lump.return_goal()
                else:
                    self.lump.return_goal()


            if self.lump.state == "cancel_goal":
                if "stop_bt" in self.current_goal:
                    if len(self.current_goal ["stop_bt"]) > 0:
                        response = self.doStep(self.current_goal ["stop_bt"], "goal")
                        if response == "success" or response == "failure": 
                                self.current_goal = {}
                                self.lump.return_idle()
                    else:
                        self.current_goal = {}
                        self.lump.return_idle()
                else:
                    self.current_goal = {}
                    self.lump.return_idle()

            if self.lump.state == "goal":
                    # If goal is running check reaction conditions
                    reactions =  self.checkActivateConditionals("reactions")
                    if len(reactions) > 0:
                        reaction = reactions[0]
                        self.current_reaction = copy.deepcopy(self.dict_reactions[reaction])
                        self.set_reaction_time(self.current_reaction)
                        self.doCancel()
                        self.lump.ex_reaction()
                    else:
                        canceled =  self.checkCancelConditional()
                        # Goal canceled -------------------------------------------------------------------------
                        if canceled == "success":
                            print ("CANCEL GOAL")
                            self.doCancel()
                            self.lump.cancel_goal()
                               
                        else:
                            response = self.doStep(self.current_goal ["bt"], "goal") 
                            if response == "success" or response == "failure":
                                self.current_goal = {}
                                self.lump.return_idle()

    def activateLastGoalAction(self,tree):
        response = self.bt.tick(tree, True)
        return response


    def doCancel(self):
        response = self.bt.tick({"node":"cancel", "state":"active"})

        
    def doStep(self,tree, node_type, debug = False):
        response = self.bt.tick(tree)
        if debug:
            if node_type == "reaction":
                print ("REACTION STEP RETURNS:" + str(response))
            else:
                print ("GOAL STEP RETURNS:" + str(response))
        time.sleep(self.tick_time)
        return response


