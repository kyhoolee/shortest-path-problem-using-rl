## Apply to pre-marshalling
Pre-marshalling is a project in my other github repository

### Container pre-marshalling
* Container sorting operation within bay in container terminal
* The container to be sorted is located only in the stack of bay
* Maximum tier and stack are fixed
* Each container has release date

<img src="https://user-images.githubusercontent.com/43307537/73134087-82ead200-4075-11ea-8085-f1a3908d2ab8.jpg" width="100%" height="100%" title="container terminal" alt="container bay"></img>  

  #
### State and action of reinforcement learning for pre-marshalling
* State
  - Each container stacked with release date in bay is a state
  - Stacked state is represented by array 
    - Each numbers in cell is release date(1 is fastest)
    - Empty cell is empty space
  - Image below is state of 3X3 bay with 6 containers
* Action
  - Moving a container on top of selected stack to top of another stack is a action
  -Image below show [1,3] action
    - Moving container on top of stack 1 to top of stack 3

<img src="https://user-images.githubusercontent.com/43307537/73134167-d14ca080-4076-11ea-9d60-aa5848036a13.jpg" width="100%" height="100%" title="state and action for pre-marshalling" alt="container bay"></img>  
  #
  
### Goal of applying proposed method to pre-marshalling

#### Find path between 2 specific nodes states(initial node, target node) 
  
<img src="https://user-images.githubusercontent.com/43307537/73134564-1a9eef00-407b-11ea-9f93-7eccff0d2a64.jpg" width="60%" height="60%" title="" alt="container bay"></img>  


<img src="https://user-images.githubusercontent.com/43307537/73134505-8765b980-407a-11ea-8460-ea74b66f43c8.gif" width="70%" height="70%" title="" alt="container bay"></img>  

  #

### Result for 3X3, 2 different shipping dates, 6 containers
- 200 different nodes  
- 12 actions

<img src="https://user-images.githubusercontent.com/43307537/73136451-285f6f00-4091-11ea-8a24-cb7775d7f27b.gif" width="15%" height="15%" title="state history" alt="container bay"></img> 

<img src="https://user-images.githubusercontent.com/43307537/73136447-1f6e9d80-4091-11ea-9b9d-9aef84a516ef.jpg" width="40%" height="40%" title="initial nodes state and target nodes state" alt="container bay"></img>  

<img src="https://user-images.githubusercontent.com/43307537/73136455-31504080-4091-11ea-87a7-b3a9a5bc5a62.jpg" width="100%" height="100%" title="graph and path" alt="container bay"></img> 

  #
  
### Result for 3X3, 3 different shipping dates, 6 containers
- 900 different nodes  
- 12 actions

<img src="https://user-images.githubusercontent.com/43307537/73136566-60b37d00-4092-11ea-99c8-430a2f152662.gif" width="15%" height="15%" title="state history" alt="container bay"></img> 

<img src="https://user-images.githubusercontent.com/43307537/73136571-690bb800-4092-11ea-9144-f3f78962f429.jpg" width="40%" height="40%" title="initial nodes state and target nodes state" alt="container bay"></img>  

<img src="https://user-images.githubusercontent.com/43307537/73136573-7163f300-4092-11ea-9d4c-39d344f0d243.jpg" width="100%" height="100%" title="graph and path" alt="container bay"></img> 

  #
  
### Result for 3X3, 6 different shipping dates, 6 containers
- 7200 different nodes
- 14 actions

<img src="https://user-images.githubusercontent.com/43307537/73136581-7c1e8800-4092-11ea-9150-def0c2af2674.gif" width="15%" height="15%" title="state history" alt="container bay"></img> 

<img src="https://user-images.githubusercontent.com/43307537/73136585-8476c300-4092-11ea-83a2-0aff1bd8e8bb.jpg" width="40%" height="40%" title="initial nodes state and target nodes state" alt="container bay"></img>  

<img src="https://user-images.githubusercontent.com/43307537/73136589-8b053a80-4092-11ea-9b6c-b1dc4d1f9ac9.jpg" width="100%" height="100%" title="graph and path" alt="container bay"></img> 

  #
  









