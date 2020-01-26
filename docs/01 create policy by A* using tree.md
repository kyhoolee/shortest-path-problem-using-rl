## Using A* algorithm to create policy
### Creating policy by using traditional A* algorithm
* Traditional A* algorithm is applied to graph 
* Since structure of graph is unknown, **drawing graph from root node** and A* simulation will be performed simultaneously(image below)
  - Compute h(n) by using neural network to output node states value
  - Each node has 6 edges
  - 30 simulations are done for creating 1 policy
    - 30 close nodes are selected(without root node)

<img src="https://user-images.githubusercontent.com/43307537/73133181-7e6bec80-4068-11ea-8e42-f15f913b5697.jpg" width="100%" height="100%" title="px(픽셀) 크기 설정" alt="container bay"></img>  
  #
* Create policy of root nodes state by counting close nodes(image below)

<img src="https://user-images.githubusercontent.com/43307537/73133188-8fb4f900-4068-11ea-8b79-bb0cc58e01c1.jpg" width="80%" height="80%" title="px(픽셀) 크기 설정" alt="container bay"></img>  

|child node(action)|1|2|3|4|5|6|  
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|  
|number of connected nodes|2|3|5|12|4|4|  
|pi|0.0667|0.1|0.1667|0.4|0.1333|0.1333|  

### Problem and cause with using traditional A* algorithm
* Takes too much time with drawing graph
* Image below shows process of drawing graph and comparing for same states(red square) which is main reason for time delay

<img src="https://user-images.githubusercontent.com/43307537/73133367-ffc47e80-406a-11ea-8f93-3e185d1de7bf.jpg" width="100%" height="100%" title="px(픽셀) 크기 설정" alt="container bay"></img>  
  #
### Solution for time delay
#### Skip comparing for same states
* If comparing for same states is omitted, the drawing becomes tree like image below

<img src="https://user-images.githubusercontent.com/43307537/73133473-60a08680-406c-11ea-923e-87eab931182e.jpg" width="100%" height="100%" title="px(픽셀) 크기 설정" alt="container bay"></img>  
  #
#### Result of created policy
* Policy created by A* algorithm using tree is no different from policy created by graph(image below)

<img src="https://user-images.githubusercontent.com/43307537/73133502-d573c080-406c-11ea-96b4-860cf4eb3f86.jpg" width="100%" height="100%" title="px(픽셀) 크기 설정" alt="container bay"></img>  
  #

#### Time decrease
* Table below show reduction of time
* The simulation conditions 
    - node has maximum 56 edges
    - 1,000 simulations are done
      - 1,000 close nodes are selected when creating 1 policy for root node

||total time taken(s)|number of generated nodes|
|:-|:-:|:-:|
|graph|1,610|12,637|
|**tree**|**10**|32,872|  




