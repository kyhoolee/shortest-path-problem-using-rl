## Apply to pre-marshalling
Pre-marshalling is a project in my other github repository

### Container pre-marshalling
* Container sorting operation within bay in container terminal
* The container to be sorted is located only in the stack of bay
* Maximum tier and stack are fixed
* Each container has release date

<img src="https://user-images.githubusercontent.com/43307537/73134087-82ead200-4075-11ea-8085-f1a3908d2ab8.jpg" width="100%" height="100%" title="example of generating pi through A star simulation" alt="container bay"></img>  

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

<img src="https://user-images.githubusercontent.com/43307537/73134167-d14ca080-4076-11ea-9d60-aa5848036a13.jpg" width="100%" height="100%" title="example of generating pi through A star simulation" alt="container bay"></img>  
  #
  
### Goal of applying proposed method to pre-marshalling

#### Find path between 2 specific nodes states(initial node, target node) 
  
<img src="https://user-images.githubusercontent.com/43307537/73134564-1a9eef00-407b-11ea-9f93-7eccff0d2a64.jpg" width="60%" height="60%" title="example of generating pi through A star simulation" alt="container bay"></img>  
  #

<img src="https://user-images.githubusercontent.com/43307537/73134505-8765b980-407a-11ea-8460-ea74b66f43c8.gif" width="70%" height="70%" title="example of generating pi through A star simulation" alt="container bay"></img>  

  #

### Result





















