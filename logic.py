#################################################################################################################################
# Authors: Marc Thomas
# Project: Cannibals and Missionaries
# Date: 9/28/2012
#
# Description:  In this logic problem, there are 2 types of people, cannibals and missionaries
#                There is a river which must be crossed, and a boat that holds up to 2 at a time
#                Cannibals must never out number missionaries or else the missioniary's will be eaten
#                Goal is to move all individuals from start side to goal side
#
# Implementation: In this implementation, we perform a recursive depth-first search. Our heuristics include the  
#                use several flags and rules. The rules start with being the based "Can't have more cannibals than missionaries"
#                to the much more complicated tracking of inverse vectors, dead ends, pattern recognition, recursion level etc.
##################################################################################################################################
#
#
# Current Status:    Complete
#  Fully Functional
#
# Work needing to be done includes:
#  Write additional comments/documentation
#
# Additional functionality for fun:
#    Add ability to modify the capacity of the boat.

###################################################################################################################################

from visuals import vectors

CONST_MIS = 3
CONST_CAN = 3

# Represents the starting goal side
CONST_START = [0,0,0]
# Represents a successful goal side
CONST_GOAL = [CONST_MIS,CONST_CAN,1]

# Represents status of success in finding Goal
GLOB_BOOL = False
# Tracks level of recursion 
GLOB_RECURSION = 0

#Tracks Recursion level of patterns
GLOB_RECPAT = 0

# Represents Booleans for each possible movement

GLOB_BOOL1 = True
GLOB_BOOL2 = True
GLOB_BOOL3 = True
GLOB_BOOL4 = True
GLOB_BOOL5 = True
GLOB_BOOL6 = True
GLOB_BOOL7 = True
GLOB_BOOL8 = True
GLOB_BOOL9 = True
GLOB_BOOL10 = True

# Vector Arrays to keep track of unsuccessful routes.
GLOB_DEADSTART = []
GLOB_DEADGOAL = []

#Tracks and records successful routes
GLOB_TRACKGOAL = []
GLOB_TRACKVEC = []
GLOB_TRACKREC = []

# Tracks patterns to prevent infinite recursion
GLOB_PATTERN = []

# Tracks the first move by goal side. Prevents recursion from making
# same path recursively infinitely.
GLOB_FIRSTGOAL = []

def main():
    POS = []
    new = []
    
    # Creates a 2X2 dimensional array with first value a  tuple, 
    # second value tracking boat status
    for _ in range(2):
        for _ in range (3):
            new.append([0])
        POS.append(new)
        new = []
    
    # Set global variables for local use
    global GLOB_BOOL
    global GLOB_FIRSTGOAL
    global GLOB_TRACKVEC
    #Set Starting values
    POS[0][0] = CONST_MIS
    POS[0][1] = CONST_CAN
    POS[0][2] = 1
    POS[1][0] = 0
    POS[1][1] = 0
    POS[1][2] = 0
    GLOB_FIRSTGOAL = [-1,-1,-1]
    vec = (0,0,0)
    
    print "Start Side", "\t\t", "Goal Side", "\t\t", "Vector", "\t\t" "Recursion"
    POS = startSide(POS,vec)

    print "Final Vector Result: ", GLOB_TRACKVEC
    
    if GLOB_BOOL == True:
        vectors(CONST_MIS, CONST_CAN, GLOB_TRACKVEC)
    else:
        print("No solution to display visually")    
    
def startSide(H_ARR, vec):
    # Set global variables for local use
    global GLOB_BOOL
    global GLOB_RECURSION
    global GLOB_BOOL1
    global GLOB_BOOL2
    global GLOB_BOOL3
    global GLOB_BOOL4
    global GLOB_BOOL5
    global GLOB_DEADSTART
    global GLOB_DEADGOAL
    global GLOB_FIRSTGOAL
    global GLOB_RECPAT
    
    # Increment recursion level
    GLOB_RECURSION += 1
    
    # Stop Case: Check if goal has been met
    if GLOB_BOOL == True:
        return H_ARR
    
    # Keep track of initial vector
    logVec = vec
    
    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
    # Confirm boat is on start side
    if H_ARR[0][2] == 1:    
        # Move 1 Cannibal to Goal Side
        if H_ARR[0][1] >= 1:
            i = GLOB_DEADSTART.count([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            if i == 1:
                # If current position is blacklisted, revert to previous values
                startSideRevert(H_ARR, logVec)
                return
                
            elif (GLOB_BOOL1 == False and GLOB_RECURSION == 1) or (GLOB_RECURSION > 1 
                                                                 and H_ARR[0][0] == 3
                                                                 and H_ARR[0][1] == 3
                                                                 and H_ARR[0][2] == 1):
                GLOB_BOOL1 = False
            
            elif vec != (0,-1,-1):    
                tempvec = vec
                vec = (0,1,1)
                # Values are modified inside this function
                if(checkAndModify(H_ARR, vec)):
                # Check if Goal Values have been met
                    if (H_ARR[1] == CONST_GOAL):             
                        GLOB_BOOL = True
                        return
                   
                    GLOB_BOOL1 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    goalSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                else:
                    vec = tempvec
                
        # Move 2 Cannibals to Goal Side
        if H_ARR[0][1] >= 2:
            
            i = GLOB_DEADSTART.count([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            if i == 1:
                # If current position is blGLOB_RECPATacklisted, revert to previous values
                startSideRevert(H_ARR, logVec)
                return
            
            elif (GLOB_BOOL2 == False and GLOB_RECURSION == 1) or (GLOB_RECURSION > 1 
                                                                 and H_ARR[0][0] == 3
                                                                 and H_ARR[0][1] == 3
                                                                 and H_ARR[0][2] == 1):
                GLOB_BOOL2 = False
                           
            elif vec != (0,-2,-1):
                tempvec = vec
                vec = (0,2,1)
                if (checkAndModify(H_ARR,vec)):
                    GLOB_BOOL2 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                   
                    
                    goalSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                else:
                    vec = tempvec

        # Move 1 Missionary to Goal Side
        if H_ARR[0][0] >= 1:
            i = GLOB_DEADSTART.count([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            if i == 1:
                # If current position is blacklisted, revert to previous values
                startSideRevert(H_ARR, logVec)
                return
            
            elif (GLOB_BOOL3 == False and GLOB_RECURSION == 1) or (GLOB_RECURSION > 1 
                                                                 and H_ARR[0][0] == 3
                                                                 and H_ARR[0][1] == 3
                                                                 and H_ARR[0][2] == 1):
                GLOB_BOOL3 = False
            elif vec != (-1, 0, -1):
                tempvec = vec
                vec = (1,0,1)
                if(checkAndModify(H_ARR, vec)):
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    GLOB_BOOL3 = False
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                
                    goalSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                else:
                    vec = tempvec
   
        # Move 2 Missionary's to Goal Side
        if (H_ARR[0][0] >= 2):
            
            i = GLOB_DEADSTART.count([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            if i == 1:
                # If current position is blacklisted, revert to previous value
                startSideRevert(H_ARR, logVec)
                return
            elif (GLOB_BOOL4 == False and GLOB_RECURSION == 1) or (GLOB_RECURSION > 1 
                                                                 and H_ARR[0][0] == 3
                                                                 and H_ARR[0][1] == 3
                                                                 and H_ARR[0][2] == 1):
                GLOB_BOOL4 = False

            elif vec != (-2,0,-1):
                tempvec = vec
                vec = (2,0,1)
                if(checkAndModify(H_ARR, vec)):
                    GLOB_BOOL4 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                    
                    goalSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                else:
                    vec = tempvec
        
        #Move 1 Missionary and 1 Cannibal to Goal Side
        if (H_ARR[0][0] >= 1 and H_ARR[0][1] >= 1):
           
            i = GLOB_DEADSTART.count([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            if i == 1:
                # If current position is blacklisted, revert to previous value
                startSideRevert(H_ARR, logVec)
                return
            elif (GLOB_BOOL5 == False and GLOB_RECURSION == 1) or (GLOB_RECURSION > 1 
                                                                 and H_ARR[0][0] == 3
                                                                 and H_ARR[0][1] == 3
                                                                 and H_ARR[0][2] == 1):
                GLOB_BOOL5 = False

            elif vec != (-1,-1,-1):
                tempvec = vec
                vec = (1,1,1)
                if(checkAndModify(H_ARR, vec)):
                    GLOB_BOOL5 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                    
                    
                    goalSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            startSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                else:
                    vec = tempvec
                    
        # Revert and blacklist path            
        if 1:
            # Check if last position is already blacklisted
            i = GLOB_DEADSTART.count([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            # If position is not blacklisted, add to list
            if (i != 1 and H_ARR[0] != [CONST_MIS,CONST_CAN,1]):
                GLOB_DEADSTART.append([H_ARR[0][0], H_ARR[0][1], H_ARR[0][2]])
            
            print "Start: ", GLOB_DEADSTART
            # Revert to previous value
            startSideRevert(H_ARR, logVec)
            return


def goalSide(H_ARR, vec):
    # Enable global variables for local use
    global GLOB_RECURSION
    global GLOB_BOOL6
    global GLOB_BOOL7
    global GLOB_BOOL8
    global GLOB_BOOL9
    global GLOB_BOOL10
    global GLOB_DEADSTART
    global GLOB_DEADGOAL
    global GLOB_FIRSTGOAL
    global GLOB_BOOL
    global GLOB_RECPAT
    # Check if goal has been met
    if GLOB_BOOL == True:
        return H_ARR

    # Increment recursion index
    GLOB_RECURSION += 1
    # Keep track of vector
    logVec = vec
    
    # Check if first move by goal side
    if GLOB_RECURSION == 2:
        GLOB_FIRSTGOAL = ([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
        
    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION

    # Boat is on Goal side
    if (H_ARR[1][2] == 1):
        
        # Move 1 Cannibal to Start Side
        if (H_ARR[1][1] >= 1):
            i = GLOB_DEADGOAL.count([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            if i == 1:
                goalSideRevert(H_ARR, logVec)
                return
            elif (GLOB_RECURSION == 2 and GLOB_BOOL6 == False):
                GLOB_BOOL6 = False
           
            elif vec != (0,1,1):
                tempvec = vec
                vec = (0,-1,-1)
                if(checkAndModify(H_ARR, vec)):
                    GLOB_BOOL6 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    startSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if Goal Values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                    
                else:
                    vec = tempvec
                
        # Move 2 Cannibals to Start Side
        if (H_ARR[1][1] >= 2):
            i = GLOB_DEADGOAL.count([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            if i == 1:
                goalSideRevert(H_ARR, logVec)
                return
            
            elif(GLOB_RECURSION == 2 and GLOB_BOOL7 == False):
                GLOB_BOOL7 = False
            elif vec != (0,2,1):
                tempvec = vec
                vec = (0, -2, -1)
                if (checkAndModify(H_ARR,vec)):
                    GLOB_BOOL7 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0                  
                    
                    startSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                    
                else:
                    vec = tempvec

        # Move 1 Missionary to Start Side
        if (H_ARR[1][0] >= 1):
            i = GLOB_DEADGOAL.count([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            if i == 1:
                goalSideRevert(H_ARR, logVec)
                return
            
            elif(GLOB_RECURSION == 2 and GLOB_BOOL8 == False):
                GLOB_BOOL8 = False
            
            elif vec != (1,0,1):
                tempvec = vec
                vec = (-1,0,-1)
                if(checkAndModify(H_ARR, vec)):
                    GLOB_BOOL8 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                            
                    startSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                    
                else:
                    vec = tempvec
        
        # Move 2 Missionary's to Start Side
        if (H_ARR[1][0] >= 2):
            
            i = GLOB_DEADGOAL.count([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            if i == 1:
                goalSideRevert(H_ARR, logVec)
                return
            
            elif(GLOB_RECURSION == 2 and GLOB_BOOL9 == False):
                GLOB_BOOL9 = False
    
            elif vec != (2,0,1):
                tempvec = vec
                vec = (-2,0,-1)
                if(checkAndModify(H_ARR, vec)):
                    GLOB_BOOL9 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                            
                    startSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return     
                else:
                    vec = tempvec

        # Move 1 Missionary and 1 Cannibal to start side
        if (H_ARR[1][0] >= 1 and H_ARR[1][1] >= 1):
            i = GLOB_DEADGOAL.count([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            if i == 1:
                goalSideRevert(H_ARR, logVec)
                return
            
            elif(GLOB_RECURSION == 2 and GLOB_BOOL10 == False):
                GLOB_BOOL10 = False
            
            elif vec != (1,1,1):
                tempvec = vec;
                vec = (-1,-1,-1)
                if(checkAndModify(H_ARR, vec)):                    
                    GLOB_BOOL10 = False
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                            
                    startSide(H_ARR, vec)
                    GLOB_RECURSION -= 1
                    print H_ARR[0][0], H_ARR[0][1], H_ARR[0][2], "\t\t\t",H_ARR[1][0], H_ARR[1][1], H_ARR[1][2], "\t\t\t", vec, "\t\t", GLOB_RECURSION
                    # Run pattern elimination reversion
                    if GLOB_RECPAT != 0:
                        if GLOB_RECPAT > GLOB_RECURSION:
                            goalSideRevert(H_ARR, logVec)
                            return
                        else:
                            GLOB_RECPAT = 0
                    # Check if goal values have been met
                    if (H_ARR[1] == CONST_GOAL):
                        GLOB_BOOL = True
                        return
                else:
                    vec = tempvec
                    
        if 1 == 1:
            i = GLOB_DEADGOAL.count([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            if (i != 1 and H_ARR[0] != [3,3,1]):
                GLOB_DEADGOAL.append([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
            print "GOAL: ", GLOB_DEADGOAL
            goalSideRevert(H_ARR, logVec)
            return


def checkAndModify(H_ARR, vec):
    # This functions checks if H_ARR modified by vec
    # produces legal values. If Value's are legal,
    # True is returns. If values are not legal, 
    # values are returned to previous state and
    # startSide() is instructed to run the next comparison
    global GLOB_TRACKVEC
    global GLOB_TRACKREC
    
    # Modify Values
    H_ARR[0][0] += -vec[0]
    H_ARR[0][1] += -vec[1]
    H_ARR[0][2] += -vec[2]
    H_ARR[1][0] += vec[0]
    H_ARR[1][1] += vec[1]
    H_ARR[1][2] += vec[2]
    
#   print "Before: ", GLOB_TRACKVEC
    GLOB_TRACKVEC.append([vec[0], vec[1], vec[2]])
    GLOB_TRACKREC.append(GLOB_RECURSION)
#   print "After: ", GLOB_TRACKVEC
    
    if ((H_ARR[0][0] == 0 or (H_ARR[0][0] >= H_ARR[0][1])) and 
       (H_ARR[1][0] == 0 or (H_ARR[1][0] >= H_ARR[1][1])) and
       # Prevent start side starting position inside recursion
       (((H_ARR[0][0] == CONST_MIS and H_ARR[0][1] == CONST_CAN and H_ARR[0][2] == 1) and GLOB_RECURSION == 1) or
       (H_ARR[0][0] != CONST_MIS or H_ARR[0][1] != CONST_CAN or H_ARR[0][2] != 1))
       # Prevent goal side starting position inside recursion
       and (((H_ARR[1][0] == GLOB_FIRSTGOAL[0] and H_ARR[1][1] == GLOB_FIRSTGOAL[1] and H_ARR[1][2] == GLOB_FIRSTGOAL[2]) and GLOB_RECURSION == 2) or
       (H_ARR[1][0] != GLOB_FIRSTGOAL[0] or H_ARR[1][1] !=  GLOB_FIRSTGOAL[1] or H_ARR[1][2] != GLOB_FIRSTGOAL[2]))
       
       and patternRecognition()
       ):
        
        GLOB_TRACKGOAL.append([H_ARR[1][0], H_ARR[1][1], H_ARR[1][2]])
        return True
    else:
        # Revert values if they do not meet the criteria
        H_ARR[0][0] += vec[0]
        H_ARR[0][1] += vec[1]
        H_ARR[0][2] += vec[2]
        H_ARR[1][0] += -vec[0]
        H_ARR[1][1] += -vec[1]
        H_ARR[1][2] += -vec[2]
        GLOB_TRACKVEC.pop()
        GLOB_TRACKREC.pop()
        return False

def patternRecognition():
    # This function's purpose is to identify 
    # patterns that would cause infinite recursion
    # and prevent them from progressing
    
    global GLOB_TRACKVEC
    global GLOB_RECURSION
    global GLOB_RECPAT
    
    check = False
    if (len(GLOB_TRACKGOAL) > 0):
        countTotal = GLOB_TRACKGOAL.count((GLOB_TRACKGOAL[(len(GLOB_TRACKGOAL)-1)]))
        patternCount = -1
        checkValue = []
        checkNextValue = []
        index = []
        indexCount = 0
        while ((countTotal >= 3 or check == True) and countTotal >= 1) :
            check = True
            if countTotal != 1:
                index.append(GLOB_TRACKGOAL.index((GLOB_TRACKGOAL[(len(GLOB_TRACKGOAL)-1)])))
                checkValue.append([GLOB_TRACKGOAL[index[indexCount]][0], GLOB_TRACKGOAL[index[indexCount]][1], GLOB_TRACKGOAL[index[indexCount]][2]])
                checkNextValue.append([GLOB_TRACKGOAL[(index[indexCount]+1)][0], GLOB_TRACKGOAL[(index[indexCount]+1)][1], GLOB_TRACKGOAL[(index[indexCount]+1)][2]])
                GLOB_TRACKGOAL.pop(index[indexCount])
                indexCount += 1
            countTotal -= 1
                
        if len(checkValue) >=2 and len(checkNextValue) >=2:
            for x in range(len(checkNextValue) -1):
                for y in range(len(checkNextValue) -1):
                    if checkNextValue[x] == checkNextValue[y]:
                        patternCount += 1
                        if patternCount == 1:
                            try:
                                GLOB_RECPAT = GLOB_TRACKREC[index[x]-1]
                            
                            except IndexError:
                                print "Index out of range"
                            while len(index) > 0:
                                GLOB_TRACKGOAL.insert(index[0],checkValue[0])
                                GLOB_TRACKGOAL.insert((index[0]+1),checkNextValue[0])
                                index.pop(0)
                            print "Pattern Discovered, Recursion Level:", GLOB_RECPAT
                            return False
                patternCount = -1
            
        if check == True:
            while len(index) > 0:
                GLOB_TRACKGOAL.insert(index[0],checkValue[0])
                GLOB_TRACKGOAL.insert((index[0]+1),checkNextValue[0])
                index.pop(0)
    
    return True

        
def startSideRevert(H_ARR, logVec): 
    global GLOB_TRACKVEC  
    global GLOB_TRACKREC                     
    H_ARR[0][0] += logVec[0]
    H_ARR[0][1] += logVec[1]
    H_ARR[0][2] += logVec[2]
    
    H_ARR[1][0] += -logVec[0]
    H_ARR[1][1] += -logVec[1]
    H_ARR[1][2] += -logVec[2]
    if len(GLOB_TRACKVEC) > 0:
        GLOB_TRACKVEC.pop()
        GLOB_TRACKREC.pop()
        GLOB_TRACKGOAL.pop()
    print "------------------------------------------------------------------------------------------"
    

def goalSideRevert(H_ARR, logVec):
    global GLOB_TRACKVEC
    global GLOB_TRACKREC
    global GLOB_TRACKGOAL
    #Blacklist
    #Check is current start side values are black listed
    H_ARR[0][0] += logVec[0]
    H_ARR[0][1] += logVec[1]
    H_ARR[0][2] += logVec[2]
    
    H_ARR[1][0] += -logVec[0]
    H_ARR[1][1] += -logVec[1]
    H_ARR[1][2] += -logVec[2]
    if len(GLOB_TRACKVEC) > 0:
        GLOB_TRACKVEC.pop()
        GLOB_TRACKREC.pop()
        GLOB_TRACKGOAL.pop()
    print "------------------------------------------------------------------------------------------"
    
    
main()
