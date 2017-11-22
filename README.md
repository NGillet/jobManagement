# jobManagement

Simple python classes to manage large set of jobs on cluster. Can be used as a library with the .py .

/!\ For the moment it is more or less hard coded for CURIE, but may be easily adapted for other cluster (e.g. Marconi, PizDaint, Titan...)

## Getting Started



### Prerequisites

It just require classical python (3) packages.

```
import numpy as np
import os, sys
import pickle
from time import time ### for loading bar
from collections import OrderedDict ### for ordered parametter files
from ast import literal_eval ### for automatic casting at file reading
```

### Installing

Just git clone it. 

```
git clone https://github.com/NGillet/jobManagement.git
```

Then adapth the GLOBAL variable in jobManagement.py

```
DATA_FOLDER = "where to put the simulation folder, ALSO WHERE THE LAUNCH SCRIPT IS USED!"
IC_FOLDER = "where to put the simulation folder, ALSO WHERE THE LAUNCH SCRIPT IS USED!"
SRC_FOLDER = "SOURCE CODE FOLDER"
EXEC_NAME = "executable name"
SIM_NAME_TEMPLATE = "SIMULATION TEMPLATE NAME, USEFUL IN CASE OF DATABASE"
```

it also suppose the ceertain files are present in DATA_FOLDER:
- emmaexec              
- job_emma                
- param.run               
- param.run.grid_output   
- param.run.list_aexp     
- param.run.part_output 

## Usage exemple

```
### ONE JOB 

test_job = job( SIM_NAME='mySimulation' ) 
### the folder 'mySimulation' is created in DATA_FOLDER
### and useful files are copied
test_job.print_job() ### print job info
test_job.launch() ### submit the job in the cluster queue

### to read an existing simulation file
test_job2 = job( SIM_NAME='mySimulation', existing=True )
test_job2.update_job() ### update the status of the job on the cluster (RUNNING, PENDDING, FINISH...)
test_job2.print_job()

### FOR A DATABASE
myList = listOfJobs( 3, existing=True ) ### will create or read 3 jobs folder
myList_load.print_list( ) ### print all jobs info

save( myList )
myList_load = load()

myList_load.update() ### update all job status
myList_load.print_list( )
myList_load.launch_restart() ### restart all jobs that need a restart

### PARAMS TUNNING
### parameter file can be tune for all jobs, as a dictinnary
test_job.params['level_coarse'] = 9
test_job.params.write_params() ### write the file, with the update poarameter
myList.list_of_jobs.params['level_coarse'] = 11
myList.list_of_jobs.params.write_params()
```

## Authors

* **Nicolas Gillet** From initial work of **Nicolas Deparis** (https://github.com/NicolasDeparis)

## Acknowledgments

* This code is inspired and adapted from some code of **Nicolas Deparis** 
* I recommande his github for more useful code (https://github.com/NicolasDeparis)
