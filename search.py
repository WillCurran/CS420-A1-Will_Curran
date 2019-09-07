# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def generateDFSTree(problem, graph, current_vertex):
    """
    Recursively called algorithm which expands a given graph along the way and
    returns the first time food is found. Assumes food exists.
    """
    if(problem.isGoalState(current_vertex.state)):
      print "Returning goal vertex at ", current_vertex.state
      return current_vertex
    
    current_vertex.visited = True
    # insert newly discovered vertices and edges
    for successor in problem.getSuccessors(current_vertex.state):
      add_this_edge = True
      # search adjacency list of current vertex to ensure we haven't seen an edge with the successor
      for edge in current_vertex.edges:
        if(edge.oppositeTo(current_vertex).state == successor[0]):
          add_this_edge = False
          continue
      successor_vert = graph.findVertOfState(successor[0])      # copy or reference returned?
      # add to graph if appropriate
      if(successor_vert == None): 
        successor_vert = graph.insertVertex(successor[0], current_vertex)
      if(add_this_edge):
        graph.insertEdge(current_vertex, successor_vert, successor[1])
    
    # i = 1
    # print "All edges at ", current_vertex.state, ": "
    # for edge in current_vertex.edges:
    #   print "[", edge.verts[0].state, ", ", edge.verts[1].state, "]"
    # print "BEFORE FOR LOOP at ", current_vertex.state, ", vertex edges = "
    for edge in current_vertex.edges:
        edge.printSelf()
    initial_vertex = current_vertex # copy in order to keep track with prints
    for new_edge in current_vertex.edges:
      print "At ", initial_vertex.state
      # print "AFTER FOR LOOP DECLARATION at ", current_vertex.state, ", vertex edges = "
      # for edge in current_vertex.edges:
      #   edge.printSelf()
      # print "Edge ", i, " of ", current_vertex.state, ": [", new_edge.verts[0].state, ", ", new_edge.verts[1].state, new_edge.bearing, "]"
      # print "All edges at ", current_vertex.state, ": "
      # print "At ", current_vertex.state, " for the ", i, "-th time"
      # for edge in current_vertex.edges:
      #   print "[", edge.verts[0].state, ", ", edge.verts[1].state, edge.bearing, "]"
      # i += 1
      # if(new_edge.containsState((2,2))):
      #   print "At (2, 2)"
      # print "Is this edge adjacent to the current vertex? : "
      if(not new_edge.explored):
        print "Haven't explored: "
        new_edge.printSelf()
        graph.markEdgeExplored(new_edge)
        if(not new_edge.oppositeTo(initial_vertex).visited): # if the proposed new vertex has already been visited, don't go there.
          current_vertex = new_edge.oppositeTo(initial_vertex)
          print "Next recurse at ", current_vertex.state
          generateDFSTree(problem, graph, current_vertex)
          print "Done with recurse at ", current_vertex.state # are we sure this is the same vertex?
        else:
          print "back edge"
          new_edge.back_edge = True
    

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    graph = util.Graph()

    start_vertex = graph.insertVertex(problem.getStartState(), None)
    food_vertex = generateDFSTree(problem, graph, start_vertex)
    graph.printSelf()
    # trace the path
    curr = food_vertex
    path_stk = util.Stack()
    while(curr != start_vertex):
      parent_edge = curr.getParentEdge()
      path_stk.push(parent_edge.bearing)
      curr = curr.parent
    # flip the path
    path = []
    while(not path_stk.isEmpty()):
      path.append(path_stk.pop())
    return path
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
