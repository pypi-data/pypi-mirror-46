# JassBot

## Useful commands
##### Start tensorboard:
    
    tensorboard --logdir log
    
#### SSH to remote machine with port forwarding for viewing the tensorboard
    
    ssh -L 6006:127.0.0.1:6006 -i ~/.ssh/diufpc29 joel@diufpc29
    
#### Setup environment
- install conda
- create environment with python 3.7.3 `conda create --name project python=3.7.3`
- activate environment `conda activate project`
- install requirements `pip install -r requirements.txt`
- (export environment `conda env export > environment.yml`)

or

- install from environment.yml `conda env create -f environment.yml`


## Run experiment
`python experiment.py`
