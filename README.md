# Distance Vector Routers Simulation

This project uses Bellman-Ford Algorithm to update routing tables for neighbouring Routers. This is completely implemented in Python. 

// Structure:

    router.py : main program file
    
    models.py : functions and class definitions
    
                Router Class has implementation of 
                
                Bellman-Ford.
                
    utils.py  : DGRAM socket setup
    
                DGRAM connected socket setup
                
                broadcast cost to given server
                

USAGE: ./python router.py directory router_name [-p]

include: -p for poisioned reverse. Enjoy.
