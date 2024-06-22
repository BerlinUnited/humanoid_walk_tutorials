# Humanoid Walk Tutorials

Experiments and tutorials to create simple walking behavior on humanoid robots based on ideas of central pattern generators (CPG) and parallel kinematics (PK) assumptions.

## Simulation

For our experiments we use the Webots simulator:  
https://www.cyberbotics.com/

The aim of the tutorials is to solve the Humanoid Sprint Challenge:  
https://robotbenchmark.net/benchmark/humanoid_sprint/

The humanoid robot NAO:
https://cyberbotics.com/doc/guide/nao

## Approach

The humanoid Robot NAO has 25 joints (degrees of freedom), with 11 of them in its legs and the hip. The challenge is to control all the joints of the robot in a way that enables the robot to walk in a fast and stable manner. In the given scenario we focus on walking on a planar surface (no hills or slopes).

To simplify the task, we devise a simple *inverse kinematics* based on *parallel kinematics* assumptions. Instead of controlling a single joint, like a knee, we focus on controlling groups of joints that result in basic movements such as 
- contract a leg (z-axis)
- shift a foot forward (x-axis)
- shift a foot to the side (y-axis)
- turn a foot to a size (rotation on z-axis)
These basic movements allow us to construct the walk from the perspective of the feet, which is more intuitive.

To generate the walking pattern we use oscillations based on `sin`and `cos`. 
