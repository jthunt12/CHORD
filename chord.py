################################################################################
# File: chord.py
# Author: Jonathan Troy Hunt
# Date: Wed April 18, 2018
# Email: jthunt92@gmail.com
# Class: CSC 344 Computer Networks -- Universtiy of North Carolina Wilmington
# Description:
#
#   The following program simulates the CHORD (peer-to-peer) protocol.
#
#   In computing, Chord is a protocol and algorithm for a peer-to-peer distributed hash table.
#   A distributed hash table stores key-value pairs by assigning keys to different computers
#   (known as "nodes")
#   A node will store the values for all the keys for which it is responsible.
#   Chord specifies how keys are assigned to nodes, and how a node can discover the value for a given
#   key by first locating the node responsible for that key.
#
#   https: // en.wikipedia.org/wiki/Chord_(peer-to-peer)
#
################################################################################


def create_vars(maxValue, int_list, node_number):
    """
    function creates initial, randomly generated list using values between 1 and 2**B
    :param maxValue:
    :param int_list:
    :param node_number:
    :return int_list:
    """
    int_list = []
    random_var = 0
    for i in range(0, node_number):
        random_var = random.randint(1, maxValue - 1)
        int_list.append(random_var)
    return (int_list)


def createK_table(current_head, b_value):
    """
    Creates the initial k_table that is added to you N values
    :param current_head:
    :param b_value:
    :return k_table:
    """
    k_table = []
    k_value = current_head
    k_valueCopy = k_value
    token_multiplier = 1
    for i in range(0, b_value):
        k_value = k_valueCopy + token_multiplier
        token_multiplier = token_multiplier * 2
        k_table.append(k_value)
    return k_table


def stablizeK_table(k_table, maxValue):
    """
    This stablizes your list K by subtracting its value once it exceeds 2**B
    :param k_table:
    :param maxValue:
    :return k_table:
    """
    pickle = False
    for i in range(0, len(k_table)):
        pickle = False
        while pickle == False:
            if k_table[i] > maxValue:
                k_table[i] = k_table[i] - maxValue
            if k_table[i] <= maxValue:
                pickle = True

    return (k_table)


def createN_table(k_table, int_list):
    """
    Using the stableK list values are given depending on its realation to listN
    :param k_table:
    :param int_list:
    :return listOfThings:
    """
    listOfThings = [None] * len(k_table)
    int_list_copy = int_list
    for i in range(0, len(k_table)):
        for e in range(0,len(int_list)):
            if k_table[i] > int_list[e]:
                if int_list[-1] == int_list[e]:
                    int_list = int_list + int_list_copy
                    listOfThings[i] = int_list[e + 1]
                listOfThings[i] = int_list[e+1]
            else:
                listOfThings[i] = int_list[e]
                break
    return(listOfThings)


def link_lists(k_list, listOfThings):
    """
    Creates a visual table that shows the steps taken so far in the process, this links the two lists together
    :param k_list:
    :param listOfThings:
    :return linked_list:
    """
    linked_list = [[None, None] for r in range(len(k_list))]
    print("Current Table")
    print(["K, N"])
    for i in range(0, len(k_list)):
        linked_list[i][0] = k_list[i]
        linked_list[i][1] = listOfThings[i]
        print(linked_list[i])
    return linked_list


def designate_val(needToFind, k_table):
    """
    This function finds the optimal position and sends it to K
    :param needToFind:
    :param k_table:
    :return head_pos:
    """
    initial_head = 0
    head_pos = 0
    numb_check = False
    for i in range(0, len(k_table)):
        if needToFind == k_table[i]:
            return True
        if needToFind > k_table[i] > initial_head:
            initial_head = k_table[i]
            head_pos = i
            numb_check = True
    if numb_check is False:
        return len(k_table)-1
    return head_pos


import random
"""
Creates variables
"""
node_number = int(input("Please Give a Number of Nodes in CHORD: "))
b_value = int(input("Please Give a Value for B: "))
maxValue = 2 ** int(b_value)
int_list = []
int_list = create_vars(maxValue, int_list, node_number)
int_list = [ii for n, ii in enumerate(int_list) if ii not in int_list[:n]]
current_head = int_list[1]
needToFind = random.randint(0, maxValue)
print("We are going to find K",needToFind)
needToFind = random.randint(0,maxValue)
Turkey = True
travelList = [current_head]


while Turkey == True:
    """
    Responsible for interpreting your variables and determining what to send functions next
    This terminates when all N values have been used or when initial k_value is found. 
    """
    k_table = createK_table(current_head, b_value)
    k_table = stablizeK_table(k_table, maxValue)
    int_list = sorted(int_list)
    listOfThings = createN_table(k_table, int_list)
    linked_list = link_lists(k_table, listOfThings)
    nextLoop = designate_val(needToFind, listOfThings)
    for i in range(0, len(k_table)):
        if k_table[i] == needToFind:
            print("You Found K", k_table[i], " from N", travelList[-1])
            n_value = (listOfThings[i])
            Turkey = False
    if Turkey == True:
        i = 0
        print("You're next loop starts at [ N", listOfThings[nextLoop], "]")
        current_head = listOfThings[nextLoop]
        travelList.append(listOfThings[nextLoop])
        int_list.remove(listOfThings[nextLoop])
        if int_list == []:
            """
            I do not think this is proper troubleshooting But I did add the catch just in case
            """
            print("COULD NOT FIND: \nWe ran all paths \n", travelList, " \nwithout finding a solution")
            Turkey = False
if int_list != []:
    print("The nodes traveled to are: \n",travelList + [n_value])
