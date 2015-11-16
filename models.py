class DistanceVector:
    '''
    Our Distance-Vector Data Structure.
    Simple. Objects have 2 fields:
        1) nexthop    : neighbour we send the packet to
        2) cost       : estimated min. cost
    '''
    def __init__(self,nexthop,cost):
        self.nexthop        = nexthop
        self.cost           = cost

    def getcost(self):
        return self.cost

    def gethop(self):
        return self.nexthop

    def updatevector(self,cost,hop):
        self.cost   =cost
        self.nexthop=hop

        

class RoutingTable:
    '''
    Routing Table for our router X.
    It stores the distance-vectors for the router X.
    Also, stores the distance-vectors for neighbors.

    Note: Items not found in the table are treated
    as if they have INFINITY cost.
    '''
    INFINITY                = 64

    def __init__(self, base, nodes):
        '''
        initialization:
            the routes from the .cfg files are added to the initial routing table.
            rest of the routes are considered INFINITY
        '''
        self.distance_vectors       = {}
        self.distance_vectors[base] = {}
        for x,c in nodes:
            self.distance_vectors[base][x] = DistanceVector(base,c)


    def addtable(self,index):
        self.distance_vectors[index] = {}

    #d-v update helper func
    def update_vector(self, node, index, cost, nhop):
        '''
        update the cost, next hop in the routing table.
        this is where we print the change/inserts as per requirements.
        '''
        if (node not in self.distance_vectors):
            self.distance_vectors[node] = {}
        if index not in self.distance_vectors[node]:
            self.distance_vectors[node][index] = DistanceVector(nhop,cost)
            print('({0} - dest: {1} cost: {2} nexthop: {3})'.format(node,index,cost,nhop))
            return True
        elif ((self.distance_vectors[node][index].getcost()!=cost) or (self.distance_vectors[node][index].gethop()!=nhop)):
            self.distance_vectors[node][index].updatevector(cost,nhop)
            print('({0} - dest: {1} cost: {2} nexthop: {3})'.format(node,index,cost,nhop))
            return True
        return False

    def gettable(self,node):
        '''
        return routing table for a neighbor/node.
        '''
        return self.distance_vectors[node]

    def getvector(self, node, index):
        '''
            cost = 0 when source=destination
            cost = INFINITY when Dx(y) not found in table.
        '''
        if (index == node):
            d = DistanceVector(node,0)
            return d
        if index not in self.distance_vectors[node]:
            d = DistanceVector(node,INFINITY)
            return d
        else:
            return self.distance_vectors[node][index]

    #self-explanatory
    def deletevector(self,node,index):
        if index in self.distance_vectors[node]:
            del self.distance_vectors[node][index]


    #router-level d-v update.
    def updatedistancevector(self, v, nodes):
        '''
         Update Dv(x) for all x in nodes
        '''
        changed = False
        for x,c in nodes.items():
            changes = self.update_vector(v,x,c)
            changed = changes or changed
        return changed


class Node:
    '''
    Router Nodes: Base Router + Neighbor Routers all
    objects of this class.
    3 vars:
        1) node: name
        2) cost: min cost from base router
        3) nexthop: base router's next hop

    '''
    INFINITY                = 64

    def __init__(self,node,cost=INFINITY):
        self.node                   = node
        self.cost                   = cost
     
    def updatecost(self,cost):
        '''
        node cost is important for neighbors
        '''
        if(self.cost!=cost):
            self.cost=cost
            return True
        return False

    def getcost(self):
        return self.cost


class Router:
    '''

        Router Class (at node x):
        NEEDS to contain these information:
            1) Cost c(x,v) for all attached neighbor v
            2) Routing Table:
                2a) This Router's Distance-Vector to all destinations.
                2b) D-V for all neighbor in neighborhood to all dests.
            3) List of neighbors
            4) List of nodes

        Each Node has:
            1) Name
            2) Cost
            3) Nexthop



    '''
    def __init__(self, node, neighbors,poisoned=False):
        self.name       = node
        self.node       = Node(node,0)
        self.nodes      = {}
        self.neighbors  = []
        self.poisoned   = poisoned
        self.table      = RoutingTable(node, neighbors)
        
        for node,cost in neighbors:
            self.neighbors.append(node)
            self.nodes[node] = Node(node,cost=cost)
            self.table.addtable(node)

    def addnode(self,base,node):
        if (node[0] not in self.nodes):
            self.nodes[node[0]] = Node(node[0],cost=node[1])

    
    def removenode(self,node):
        del self.nodes[node]

    def routerupdate(self, base, message):
        '''
        handler for the U messages
            1) split into chunks
            2) make a list of distination,cost
            3) add nodes to router's node list
            4) update the distance vector after list
               is compilled.
        '''
        routes  = []
        chunks  = message.split()
        size    = len(chunks)
        for i in range(1,int((size/2)+1)):
            node = chunks[(i-1)*2]
            cost = chunks[((i-1)*2)+1]
            routes.append(node,cost)
            self.addnode(node)
        return self.table.updatedistancevector(base,routes)

    def getdistancevector(self):
        return self.table.gettable(self.name)

    def getneighbors(self):
        '''
        return a list of neighbor names
        '''
        return neighbors

    def getnode(self,name):
        '''
        return a node
        <may not be a neighbor>
        '''
        if name in self.nodes:
            return self.nodes[name]
        return False

    def linkcostupdate(self, base, message):
        '''
        handler for the L messages
        assuming always right format.
        '''
        chunks = message.split()
        if len(chunks)!=3:
            print('invalid link cost updater message')
            return
        return self.nodes[chunks[1]].updatecost(int(chunks[2]))

    def runbellmanford(self):
        '''
        Main D-V update algo: (Bellman-Ford)
            Dx(y) = MINv{ C(x,v) + Dv(y) } for each y in self.nodes
        where   N is the set of all routers.
                x is the base router.
                V is the set of all neighboring routers. (v belongs to self.neighbors)
        '''
        tablechanged = False
        for y in self.nodes:
            if (y.node != self.name): #to make sure not the base router
                Dx_y            = self.table.getvector(self.name,y.node) #current Dx(y)
                mincost         = Dx_y.getcost()
                minhop          = Dx_y.gethop()
                for v in self.neighbors and v!=self.name:
                    Cx_v        = self.nodes[v].getcost()
                    Dv_y        = self.table.getvector(v,y.node)
                    costv       = Cx_v + Dv_y.getcost()
                    if costv<mincost:
                        mincost = costv
                        minhop  = v
                if (Dx_y.getcost()!=mincost):
                    self.table.update_vector(self.name,y.node,mincost,minhop)
                    tablechanged = True
        return tablechanged
                    
    def printhandle(self,message):
        '''
        Handler of P messages:
            1) if no parameters: prints all routing tables
                1a) this is implemented recursively. because why not?
            2) max of 1 parameter d
                d: to print neighbor d's routing table

        '''
        chunk = message.split()
        if len(chunk)==1:
            print('Routing Table for Base Router:')
            self.printhandle('P '+self.name)
            for n in self.neighbors:
                print('Routing Table for neighbor '+n)
                self.printhandle('P '+n)
            pass
        else:
            print('     ',end="")
            dests = []
            costs = []
            for ind,vector in self.table.gettable(chunk[1]).items():
                dests.append(ind)
                costs.append(vector)
            for ind in dests:
                print(ind,end="   ")
            print('')
            print(chunk[1],end="    ")
            for vec in costs:
                if (vec.cost>=64):
                    print('~',end="   ")
                else:
                    print(vec.cost,end="   ")
            print('')
            print('')
