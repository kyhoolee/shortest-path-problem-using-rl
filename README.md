# shortest-path-problem-using-rl
solve shortest path problem through reinforcement learning and A* algorithm using tree

### Summary
Find the shortest path using reinforcement learning when graph is unknown  
Create policy by applying the A* algorithm using tree  
Solve sparse reward problem by adjusting search difficulty  

  #
## Shortest path problem
Unlike the solving general shortest path problem, the structure of the graph is unknown  
All nodes in the graph can be initial node and target node  
Goal is to find the shortest path from initial node to target node  

<img src="https://user-images.githubusercontent.com/43307537/73132640-254c8a80-4061-11ea-867a-a31a0923d89c.gif" width="80%" height="80%" title=" " alt="container bay"></img>  

  #
## Apply reinforcement learning
* Each node has information about the state  
  - Each node in the graph has a different state
* The edge connecting 2 different nodes becomes action  
  - Repeat executing action to each state of nodes and reach target node
  - Selecting action(a1) from nodes state(s0) will move to another nodes state(s1) as shown below
  
<img src="https://user-images.githubusercontent.com/43307537/73132633-1239ba80-4061-11ea-863a-3cce951236f5.jpg" width="25%" height="25%" title=" " alt="container bay"></img>  


  #
## Create policy by A* algorithm using tree
* Create policy using A* algorithm
  - Reference to creating policy using MCTS in Alphago zero
* Due to applying tradintional A* algorithm to unknown graph, it takes long time
  - The A* algorithm is be applied to tree instead of graph
  - Reduced time significantly

  #
## Solve sparse reward problem
* As the number of nodes and edges increases, it becomeS difficult to reach one target node(sparse reward)
* Sparse reward is big problem because the reward is essential in reinforcement learning
* Increase success episode by adjusting search difficulty according to learning progress

  #
## Application
* Apply proposed finding shortest path algorithm to container stockyard premarshalling


