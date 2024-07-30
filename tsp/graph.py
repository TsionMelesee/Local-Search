class Graph:
    def __init__(self):
        self.map = dict()
    
    def __backTrack(self , path : dict , end : any) -> list:
        current = end
        result = []
        while current != None:
            result.append(current)
            current = path[current]
        return result[-1::-1]

    def numOfNodes(self) -> int:
        return len(self.map)
    
    def copy(self):
        '''Returns a copy of the graph'''
        newGraph = Graph()
        newGraph.map = self.map 
        return newGraph
    
    def createNode(self , node : any) -> None:  
        self.map[node] = set()

    def addEdge(self , startNode : any , destinationNode : any , cost : float = 1.0 , directed : bool = False) -> None:
        #check if the nodes have been created 
        if startNode not in self.map:
            self.createNode(startNode)
        if destinationNode not in self.map:
            self.createNode(destinationNode)

        #check and decide whether to create a directed/undirected edge between the nodes
        if directed:
            self.map[startNode].add((destinationNode , cost))
        else:
            self.map[startNode].add((destinationNode , cost))
            self.map[destinationNode].add((startNode , cost))

    def removeEdge(self , startNode : any , destinationNode : any , cost : float = 1.0) -> None:
        #determine if the edge is directed or not or if doesn't exist
        if (destinationNode , cost) in self.map[startNode] and (startNode , cost) in self.map[destinationNode]:
            #the edge is undirected
            self.map[startNode].remove((destinationNode , cost))
            self.map[destinationNode].remove((startNode , cost))

        elif destinationNode not in self.map or startNode not in self.map:
            raise Exception("Edge doesn't exist!") 
        
        else:
            #the edge is directed
            self.map[startNode].remove((destinationNode , cost))

    def getNeighbours(self , node : any) -> list:
        try:
            return self.map[node]
        except Exception as e:
            raise Exception("Node doesn't exist!")
  
    def search(self ,node : any) -> bool:
        return node in self.map
    
