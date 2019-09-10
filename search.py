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
    vert_stk = util.Stack()
    start_vertex = graph.insertVertex(problem.getStartState(), None)
    start_vertex.visited = True
    next_vertex = None
    vert_stk.push(start_vertex)
  
    while(not vert_stk.isEmpty()):
      prev = next_vertex
      next_vertex = vert_stk.pop()
      if(next_vertex.isAdjacentTo(prev)): # new parent if assigned incorrectly
        next_vertex.parent = prev
      # print "At ", next_vertex.state
      # print next_vertex.state, " was popped from the stack."
      if(problem.isGoalState(next_vertex.state)):
        break
      # insert newly discovered vertices and edges
      for successor in problem.getSuccessors(next_vertex.state):
        add_this_edge = True
        # search adjacency list of current vertex to ensure we haven't seen an edge with the successor
        for vert in next_vertex.adjacent_verts:
          if(vert.state == successor[0]): # if this edge is a duplicate, don't add
            add_this_edge = False
            continue
        successor_vert = graph.findVertOfState(successor[0])      # O(n), copy or reference returned?
        # add to graph if appropriate
        if(successor_vert == None): 
          successor_vert = graph.insertVertex(successor[0], next_vertex) # str type bug
        if(add_this_edge):
          # next_vertex.adjacent_verts.append(successor_vert)
          # successor_vert.adjacent_verts.append(next_vertex)
          graph.insertEdge(next_vertex, successor_vert, successor[1], successor[2])

      for vert in next_vertex.adjacent_verts:                     # duplicate code to top, let it go for now
        if(not vert.visited):
          # print vert.state, " was pushed to the stack --- from ", next_vertex.state
          vert.visited = True
          vert_stk.push(vert)
    # trace the path
    path_stk = util.Stack()
    while(next_vertex != start_vertex):
      path_stk.push(next_vertex.getBearing())
      next_vertex = next_vertex.parent
    # flip the path
    path = []
    while(not path_stk.isEmpty()):
      path.append(path_stk.pop())
    return path
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    graph = util.Graph()
    vert_queue = util.Queue()
    start_vertex = graph.insertVertex(problem.getStartState(), None)
    start_vertex.visited = True
    next_vertex = None
    vert_queue.push(start_vertex)
  
    while(not vert_queue.isEmpty()):
      next_vertex = vert_queue.pop()
      # print "At ", next_vertex.state
      # print next_vertex.state, " was popped from the stack."
      if(problem.isGoalState(next_vertex.state)):
        break
      # insert newly discovered vertices and edges
      for successor in problem.getSuccessors(next_vertex.state):
        add_this_edge = True
        # search adjacency list of current vertex to ensure we haven't seen an edge with the successor
        for vert in next_vertex.adjacent_verts:
          if(vert.state == successor[0]): # if this edge is a duplicate, don't add
            add_this_edge = False
            continue
        successor_vert = graph.findVertOfState(successor[0])      # O(n), copy or reference returned?
        # add to graph if appropriate
        if(successor_vert == None): 
          successor_vert = graph.insertVertex(successor[0], next_vertex) # str type bug
        if(add_this_edge):
          graph.insertEdge(next_vertex, successor_vert, successor[1], successor[2])

      for vert in next_vertex.adjacent_verts:                     # duplicate code to top, let it go for now
        if(not vert.visited):
          # print vert.state, " was pushed to the stack --- from ", next_vertex.state
          vert.visited = True
          vert_queue.push(vert)
    # trace the path
    path_stk = util.Stack()
    while(next_vertex != start_vertex):
      path_stk.push(next_vertex.getBearing())
      next_vertex = next_vertex.parent
    # flip the path
    path = []
    while(not path_stk.isEmpty()):
      path.append(path_stk.pop())
    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    graph = util.Graph()
    edge_pq = util.PriorityQueue()
    start_vertex = graph.insertVertex(problem.getStartState(), None)
    start_vertex.visited = True # has the vertex been queued
    start_vertex.inCloud = True # has the vertex been dequeued
    start_vertex.minWeightToThisVert = 0
    root_edge = graph.insertEdge(None, start_vertex, 0, 0)
    edge_pq.push(root_edge, root_edge.weight)
  
    while(not edge_pq.isEmpty()):
      next_edge = edge_pq.pop()
      next_vertex = next_edge.getVertexOutsideCloud()
      # print "Edge popped:"
      # next_edge.printSelf()
      next_vertex.parent = next_edge.oppositeTo(next_vertex)
      next_vertex.inCloud = True
      # print "At ", next_vertex.state
      # print next_vertex.state, " was popped from the queue."
      if(problem.isGoalState(next_vertex.state)):
        break
      # insert newly discovered vertices and edges
      for successor in problem.getSuccessors(next_vertex.state):
        add_this_edge = True
        # search adjacency list of current vertex to ensure we haven't seen an edge with the successor
        for vert in next_vertex.adjacent_verts:
          if(vert.state == successor[0]): # if this edge is a duplicate, don't add
            add_this_edge = False
            continue
        successor_vert = graph.findVertOfState(successor[0])      # O(n), copy or reference returned?
        # add to graph if appropriate
        if(successor_vert == None): 
          successor_vert = graph.insertVertex(successor[0], next_vertex)
        if(add_this_edge):
          e = graph.insertEdge(next_vertex, successor_vert, successor[1], successor[2])
          # print "Added Edge to graph:"
          e.printSelf()

      for edge in next_vertex.edges:                     # duplicate code to top, let it go for now
        vert = edge.oppositeTo(next_vertex)
        if(vert != None):
          prev_accumulated_weight = vert.getPrevWeight()
          if(not vert.visited):
            vert.visited = True
            edge.weight += prev_accumulated_weight
            vert.minWeightToThisVert = edge.weight
            edge_pq.push(edge, edge.weight)
            # print vert.state, " was pushed to the queue with weight = ", edge.weight
          elif(edge.weight + prev_accumulated_weight < vert.minWeightToThisVert):
            # print "Min weight was ", vert.minWeightToThisVert, ", Now ", edge.weight
            edge.weight += prev_accumulated_weight
            vert.minWeightToThisVert = edge.weight
            vert.parent = next_vertex
            edge_pq.push(edge, edge.weight)
            # print vert.state, " was pushed to the queue ----"
    
    # trace the path
    path_stk = util.Stack()
    while(next_vertex != start_vertex):
      path_stk.push(next_vertex.getBearing())
      next_vertex = next_vertex.parent
    # flip the path
    path = []
    while(not path_stk.isEmpty()):
      path.append(path_stk.pop())
    return path
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
