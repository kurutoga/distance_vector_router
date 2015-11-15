'''
update_vectors: 
    input: 
        vectors: current cost vector
        options: new cost options from neighbour
    output:
        none
    description:
        handles the 'Router update messages' protocol
'''
def update_vectors(costs,options,link):
    opts        = options.split()
    size        = len(opts)
    updated     = False
    
    for i in range(size/2):
        new_cost = link + int(opts[(i*2)+1])
        if costs[i*2] > new_cost:
            costs[i*2] = new_cost

            updated = True
    
    if (updated==True):
        update_neighbours(costs)





