## Solve sparse reward 
### Cause
* When number of nodes and edges are big, it is very difficult to find the path to target node from initial node
  - This problem is noticeable especially in the early episodes when network training is insufficient
  - Theoretically if number of actions are unlimited, then it is possible to find the path but it is very inefficient
* High difficulty of finding path will result in sparse reward  

<img src="https://user-images.githubusercontent.com/43307537/73133718-f4278680-406f-11ea-997d-c079e4685952.jpg" width="80%" height="80%" title="example of generating pi through A star simulation" alt="container bay"></img>  
  #

### Solution
#### In this project adjusting difficulty is used, so turn sparse reward into dense reward
* Adjust distance between initial node and target node according to training progress(image below)
  - Low difficulty
    - In early episodes distance between initial node and target node is close together
  - High difficulty
    - In latter episodes distance between initial node and target node is far away


<img src="https://user-images.githubusercontent.com/43307537/73133951-6c437b80-4073-11ea-95d3-16239b5bfcbb.jpg" width="80%" height="80%" title="example of generating pi through A star simulation" alt="container bay"></img>  
  #

#### adjusting difficulty method for training
* Select target node and execute random actions in each nodes state to select initial node
  - As number of random actions increase difficulty will also increase
  - In the early episodes training few random actions are executed
  - When training episodes increases the random actions will also increase 



<img src="https://user-images.githubusercontent.com/43307537/73134013-76b24500-4074-11ea-9c4e-2a2aadc292ef.jpg" width="80%" height="80%" title="example of generating pi through A star simulation" alt="container bay"></img>  
  #

#### By using adjusting difficulty method for training, I was able to find path between initial node and target node























