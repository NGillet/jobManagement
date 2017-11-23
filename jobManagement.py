
# coding: utf-8

# In[ ]:

import numpy as np
import os, sys
import pickle
from time import time ### for loading bar

from collections import OrderedDict

from ast import literal_eval ### for automatic casting at file reading


# In[ ]:

def mkdir(path):
    try :
        os.mkdir(path)
    except OSError:
        pass


# In[ ]:

def loadbar( i, Ntot, tin ):
    titerAvg = (time() - tin) / (i+1)
    sys.stdout.write('\r')
    sys.stdout.write( "[%-20s] %.1f%%"%('='*int((i+1)*100./Ntot/5),(i+1)*100./Ntot) )
    sys.stdout.write( ", %.1f s/iter, remain %.1f s, exec %.1f s"%( titerAvg, titerAvg*(Ntot-i-1), time()-tin ) )
    sys.stdout.flush()


# In[ ]:

SCRIPT = 'NEFERTEM' # "curie"

if SCRIPT=='NEFERTEM':
    DATA_FOLDER = "/amphora/nicolas.gillet/grid_LHS/" 
    IC_FOLDER = "/amphora/nicolas.gillet/ICs/B10_128/ics_emma/level_007"
    SRC_FOLDER = "~/EMMA"
    EXEC_NAME = "emmacpu"
    SIM_NAME_TEMPLATE='sim_'
    
if SCRIPT=='curie':
    DATA_FOLDER = "/ccc/cont005/home/ra3945/gilletnj/SCRATCHDIR/grid_LHS/" ### where to put the simulation folder, ALSO WHERE THE LAUNCH SCRIPT IS USED!
    IC_FOLDER = "/ccc/cont005/home/ra3945/gilletnj/WORKDIR/ICs/B7_256/ics_emma/level_008" ### initail condition folder
    SRC_FOLDER = "/ccc/cont005/home/ra3945/gilletnj/EMMA" ### SOURCE CODE FOLDER
    EXEC_NAME = "emmacpu" ### executable name
    
    SIM_NAME_TEMPLATE='sim_' ### SIMULATION TEMPLATE NAME, USEFUL IN CASE OF DATABASE


# In[ ]:

class parameter_class( OrderedDict ):
    """
    Class to read/write the param.run file
    
    input:
        - FOLDER   : str , the simulation folder containning/will contain the param.run file
        - existing : bool, if the file already exist and had to be read, default=False
    use:
    > param = parameter_class( FOLDER, existing=existing )
    > # edit a param e.g.
    > param["overdensity_cond"] = 100
    > param.write_params() # overwrite the existing param.run file
    """
    
    def __init__( self, FOLDER, existing=False, *arg, **kw ):
        super(parameter_class, self).__init__(*arg, **kw)
        
        self.FOLDER = FOLDER
        
        self._read_param_file( existing=existing )
        
        
    def _read_param_file( self, existing=False ):
        if existing:
            fileName = self.FOLDER+"/param.run"
        else:
            fileName = DATA_FOLDER+"/param.run"
            
        with open( fileName, "r" ) as file:
            
            for line in file:
                if line[0] == '#':
                    pass
                else:
                    try:
                        self[ line.split()[0] ] = literal_eval( line.split()[1] )
                    except ValueError:
                        self[ line.split()[0] ] = line.split()[1]
                        
                    
    def write_params( self ):
        """
        overwrite the existing param.run file
        """
        with open( self.FOLDER+"/param.run", "w" ) as file:
            
            file.write( "##==MemoryManagement========\n")   
            
            file.write( "max_number_of_octs %d\n"%(self['max_number_of_octs']) )
            file.write( "max_number_of_part %d\n" %(self['max_number_of_part']) )
            file.write( "mpi_buffer_size %d\n"%(self['mpi_buffer_size']) )
            
            file.write( "##==TimestepManagement=======\n" )
            
            file.write( "output_frequency %d\n"%(self['output_frequency']) )
            file.write( "dt_dump %d\n"%(self['dt_dump']) )
            file.write( "max_nuber_of_steps %d\n"%(self['max_nuber_of_steps']) )
            file.write( "time_step_max  %1.1e\n"%(self['time_step_max']) )
            file.write( "tmax_or_amax %g\n"%(self['tmax_or_amax']) )
            
            file.write( "##==AMRGrid==================\n")
            
            file.write( "level_coarse %d\n"%(self['level_coarse']) )
            file.write( "level_max %d\n"%(self['level_max']) )
            file.write( "amr_thresh %d\n"%(self['amr_thresh']) )
            file.write( "n_smooth %d\n"%(self['n_smooth']) )
            
            file.write( "##==DM=======================\n")
            
            file.write( "dm_res %d\n"%(self['dm_res']) )
            file.write( "dx_res %g\n"%(self['dx_res']) )
            
            file.write( "##==PoissonSolver============\n")
            
            file.write( "max_number_of_relaxation_poisson %d\n"%(self['max_number_of_relaxation_poisson']) )
            file.write( "poisson_accuracy %g\n"%(self['poisson_accuracy']) )
            file.write( "mgrid_lmin %d\n"%(self['mgrid_lmin']) )
            file.write( "mgrid_nvcycles %d\n"%(self['mgrid_nvcycles']) )
            file.write( "mgrid_nsmooth %d\n"%(self['mgrid_nsmooth']) )
            
            file.write( "##==Restart==================\n")
            
            file.write( "restart_snap %d\n"%(self['restart_snap']) )
            
            file.write( "##==ThreadManagement======\n")
            
            file.write( "grav_stencil_size %d\n"%(self['grav_stencil_size']) )
            file.write( "cons_stencil_size %d\n"%(self['cons_stencil_size']) )
            file.write( "max_subcycles %d\n"%(self['max_subcycles']) )
            file.write( "nthread %d\n"%(self['nthread']) )
            file.write( "nstream %d\n"%(self['nstream']) )
            file.write( "ompthreads %d\n"%(self['ompthreads']) )
            
            file.write( "##==RadTransfert============\n")
            
            file.write( "clight %g\n"%(self['clight']) )
            file.write( "dens_threshold %g\n"%(self['dens_threshold']) )
            file.write( "temp_threshold %g\n"%(self['temp_threshold']) )
            file.write( "src_int %g\n"%(self['src_int']) )
            file.write( "fesc %f\n"%(self['fesc']) )
            file.write( "atomic_file %s\n"%(self['atomic_file']) )
            
            file.write( "##==StarFormation============\n")
            
            file.write( "overdensity_cond %f\n"%(self['overdensity_cond']) )
            file.write( "density_cond %f\n"%(self['density_cond']) )
            file.write( "efficiency %f\n"%(self['efficiency']) )
            file.write( "tlife_rad %g\n"%(self['tlife_rad']) )
            file.write( "mass_res %d\n"%(self['mass_res']) )
            
            file.write( "##==SuperNovae===============\n")
            
            file.write( "feedback_eff %f\n"%(self['feedback_eff']) )
            file.write( "feedback_kin_frac %f\n"%(self['feedback_kin_frac']) )
            file.write( "feedback_mass_return %f\n"%(self['feedback_mass_return']) )
            file.write( "feddback_egy %g\n"%(self['feddback_egy']) )
            file.write( "feedback_tlife %g\n"%(self['feedback_tlife']) )
            file.write( "feedback_wind %f\n"%(self['feedback_wind']) )
            
            file.write( "##==Movie====================\n")
            
            file.write( "lmap %d\n"%(self['lmap']) )
            file.write( "mode %s\n"%(self['mode']) )
            file.write( "xmin %d\n"%(self['xmin']) )
            file.write( "xmax %d\n"%(self['xmax']) )
            file.write( "ymin %d\n"%(self['ymin']) )
            file.write( "ymax %d\n"%(self['ymax']) )
            file.write( "zmin %d\n"%(self['zmin']) )
            file.write( "zmax %d\n"%(self['zmax']) )


# In[ ]:

class job():
    """
    Class to manage jobs to build large database
    
    input:
        - SIM_NAME : str , name of the simulation = name of run = name of the folder, default='default'
        - existing : bool, will load the job from the savefile, default=False
        - comments : str , default=""
    use:
    > myJob = job( SIM_NAME='default', existing=False, comments="" )
    > myJob.print_job() 
    > myJob.launch()
    > myJob.update_job()
    """
    #job_ID = -1
    #SIM_NAME = 'default'
    #FOLDER = 'default'
    #status = 'NOT' ### NOT: do not exist, PEN, RUN, ABT: had run but not finish, FIN
    #restart = False ### need a restart ?
    
    def __init__( self, SIM_NAME='default', existing=False, comments="" ):
        ### 
        self.job_ID = -1
        self.SIM_NAME = SIM_NAME
        self.FOLDER = DATA_FOLDER + self.SIM_NAME
        self.status = 'NOT' ### PEN, RUN, FIN, ABT, NOT
        self.restart = False
        self.comments = comments
        self.params = parameter_class( self.FOLDER, existing=existing )
        
        ### new job 
        ### init the folder
        if( not(existing) ):
            mkdir( self.FOLDER )
            mkdir("%s/data/"%(self.FOLDER))
            self._copy_param()
            os.system( "ln -s %s %s/"%(IC_FOLDER, self.FOLDER ) )

            self._write_slurm_sub() 
            self.params.write_params()
        
        ### old job 
        ### load status
        if( existing ):
            self._read_job_ID()
            self.update_job()
        
    def print_job( self, header=True ):
        """
        print job info
        header : bool, print the column names, default=True
        """
        if header :
            print( "ID          NAME        STATUS  RESTART  COMMENT" )
        print( "%d     %s     %s     %r     %s"%(self.job_ID,self.SIM_NAME,self.status,self.restart,self.comments) )
        
    def _copy_param( self ):   
        """
        init the simulation folder
        suppose that all the param.run files are in ./ when the code is used
        HARD CODED emmacpu
        """
        try :    
            os.system( "ln -s %s %s/SRC"%(SRC_FOLDER, self.FOLDER ) )
            #os.system("cp %s/SRC/param.run %s/data/"%(self.FOLDER,self.FOLDER) )
            #os.system("cp %s/SRC/param.run %s"%(self.FOLDER,self.FOLDER) )
            #os.system("cp %s/SRC/param.run.grid_output %s"%(self.FOLDER,self.FOLDER) )
            #os.system("cp %s/SRC/param.run.part_output %s"%(self.FOLDER,self.FOLDER) )
            #os.system("cp %s/SRC/param.run.list_aexp %s"%(self.FOLDER,self.FOLDER) )
            #os.system("cp %s/SRC/param.mk %s/SRC/"%(FOLDER))
            os.system("cp %s/param.run %s/data/"%(self.FOLDER,self.FOLDER) )
            os.system("cp %s/param.run %s"%(self.FOLDER,self.FOLDER) )
            os.system("cp %s/param.run.grid_output %s"%(self.FOLDER,self.FOLDER) )
            os.system("cp %s/param.run.part_output %s"%(self.FOLDER,self.FOLDER) )
            os.system("cp %s/param.run.list_aexp %s"%(self.FOLDER,self.FOLDER) )
            os.system("cp %s/param.mk %s/SRC/"%(FOLDER))
            ### and copy the exec 
            os.system("cp %s/SRC/emmacpu %s"%(self.FOLDER,self.FOLDER) )
        except OSError:
            print( "JOB : %s, copy_param error"%(self.SIM_NAME) )
        
    def _write_slurm_sub( self ):
        """
        write the submitting file
        for the moment hard coded for CURIE, and a specific type of jobs
        """
        with open(self.FOLDER+"/job_emma", "w") as file:
            file.write( "#!/bin/bash\n")
            file.write( "#MSUB -r %s           ### NAME\n"%(self.SIM_NAME) )
            #file.write( "# #MSUB -N 2                 ### NUMBER OF NODE (16 core per NODE)\n")
            file.write( "#MSUB -n 512                 ### NUMBER OF CORE\n")
            file.write( "#MSUB -T 86400               ### TIME IN s (max 4h)\n")
            file.write( "#MSUB -o out.log\n")             
            file.write( "#MSUB -e err.log\n")
            file.write( "#MSUB -q standard\n")
            file.write( "#MSUB -A ra3945\n")
            file.write( "set -x\n")
            file.write( "cd ${BRIDGE_MSUB_PWD}\n")
            file.write( "ccc_mprun ./emmacpu param.run > run.log\n")
        
    def _read_job_ID( self ):
        """
        read the job_ID file, when it has been lauched
        """
        
        #num_lines = sum(1 for line in open('myfile.txt'))
        
        with open( '%s/job_ID'%(self.FOLDER), 'r' ) as file:
            ### read all the line until the last one which is the last submitjob
            for l in file:
                #l = file.readline()
                pass
            new_job_ID = int( l.split()[3] )
            # print(new_job_ID)
            self.job_ID = new_job_ID
            
    def update_job( self ):
        """
        update the job's status and the need-restart-flag
        allow to to follow the jobs throught time
        """
        self._read_job_ID()
        new_status = self._get_status()
        self.status = new_status ### PEN, RUN, FIN, ABT, NOT
        if new_status=='ABT' :
            self.restart = True
        else:
            self.restart = False
    
    def _get_status( self ):
        """
        return the job's status from the logfile and the jobs list
        """
        log_flag = self._read_log()
        mpp_out  = self._read_mpp()
        
        self.comments = ''
        
        if log_flag==0 : ### job finish
            return 'FIN'
        
        elif log_flag==1 : ### log file exist, job not finish
            ### job RUN or ABT or PEN(from a restart)
            if mpp_out==0 :
                return 'RUN'
            elif mpp_out==1 :
                return 'PEN'
            elif mpp_out==2 :
                return 'ABT'
            
        elif log_flag==2: ### log file dont exist, job not submited or pending
            ### job NOT or PEN
            if mpp_out==1 :
                return 'PEN'
            elif mpp_out==2: 
                return 'NOT'
            elif mpp_out==3:
                self.comments = 'LOOK BY HAND : \'ccc_mpp -u gilletnj\''
                return 'ERR'
            
        elif log_flag==3: ### log file exist, memory error detected ABT
            ### but the job can be PEN also !
            is_job_memError = os.popen( 'grep \'ERROR === Allocated\' ' + self.FOLDER+'/run.log' )
            theErrorline = is_job_memError.readline().split()
            if len(theErrorline)>1 :
                if theErrorline[3] == 'grid':
                    self.comments = 'grid mem error'
                if theErrorline[3] == 'part':
                    self.comments = 'part mem error'
            if mpp_out==1 :
                return 'PEN'
            elif mpp_out==2: 
                return 'ABT'
            elif mpp_out==3:
                return 'ERR'
             
    def _read_log( self ):
        """
        look at the log file of the simulation
        0 : job finish FIN
        1 : job RUN or ABT (no memory error)
        2 : job didnt run NOT or pending in queue PEN
        3 : job memory error detected memABT
        """
        if os.path.isfile( self.FOLDER+'/run.log' ):
            ### log file exist
            ### so the run has been running (at least) once
            is_job_finnish = os.popen( 'grep \'Done ..... in\' ' + self.FOLDER+'/run.log' )
            theline = is_job_finnish.readline()
            if len(theline)>1 :
                return 0
            else:
                ### job not finish
                ### still running or aborted ?
                ### check for memory error (part or grid)
                is_job_memError = os.popen( 'grep \'ERROR === Allocated\' ' + self.FOLDER+'/run.log' )
                theErrorline = is_job_memError.readline()
                if len(theErrorline)>1 :
                    return 3 ### memory error detected
                else:
                    return 1 ### no memory error detected, job RUN or ABT
        else:
            ### log file do not exist
            ### job is NOT or PEN ?
            return 2
            
    def _read_mpp( self, mpp_out=None ):
        """
        extract for list of jobs the status 
        input:
            - mpp_out: os.popen, return of the mpp command, default='None'
                       useful for list of jobs
        return:
            0 : job in list, RUN
            1 : job in list, PEN
            2 : job not in list, ABT or FIN
            3 : job in list but other status (suspended ?)
        """
        ### look at PEN, RUN
        if mpp_out==None:
            mpp_out = os.popen( "ccc_mpp -u gilletnj" )
        dummy = mpp_out.readline()
        flag_job_in = False
        for line in mpp_out:
                if len( line.split() ) > 1:
                    ID = int(line.split()[2])
                    status = line.split()[6]
                    if self.job_ID == ID:
                        #self.status = status 
                        if status=='RUN':
                            return 0
                        elif status=='PEN':
                            return 1
                        else:
                            return 3
        return 2
    
    def _read_out():
        """USELESS"""
        ### look at CANCELLED or COMPLETED
        with open(self.FOLDER+"/out.log", "r") as file:
            for i in range(25):
                line = file.readline().split()
            status = line[10]
            if STATUS=='COMPLETED':
                return 0
            if status=='CANCELLED':
                return 1
            
    def _find_restart_number( self ):
        """
        find the number of the backup file 0 or 1 to allow a restart
        """
        restartNumFile = os.popen( "ls -lrth %s/data/bkp/ | tail -1"%(self.FOLDER) )
        theline = restartNumFile.readline()
        if len(theline.split()) <1:
            return 0 ### no backup file!
        else:
            print( theline.split() )
            return int( theline.split()[8][9] )
        
    def launch( self ):
        """
        launch the job on the cluster
        /!\ for the moment it is hard coded for CURIE
        """
        ### TODO modify here the param init 
        ### should not be done here but outside!
        ### overdensity_cond=45, feedback_eff=0, efficiency=0
        
        restart_snap = self._find_restart_number()        
        self.params['restart_snap']=restart_snap=restart_snap
        ### make sure the param.run file is up to date
        self.params.write_params()
        
        here = os.popen( 'pwd' )
        here_str = here.readline()[:-1]
        ### get to the folder to launch the simulation
        os.chdir( self.FOLDER )
        os.system( "ccc_msub job_emma >> job_ID" )
        ### get back to the original location
        os.chdir( here_str )
            
        #self._read_job_ID()
        #self.status = 'PEN' ### by default the job should be pending at the submission 

        self.update_job() ### here the job should be pending (PEN), 
        ### it my take some time to the system to actualyse the job list
        ### to test


# In[ ]:

class listOfJobs():
    """
    Class to manage a list of jobs, to build large database
    
    input:
        - NUMBER_OF_SIMS : int , number of simulation of the database
        - existing       : bool, the simulations forlder already exist and have to be read only!, default=False
        - comments       : bool, load the list of jobs from a save file, default=True
    use:
    > myJob.update() 
    > myJob.launch()
    > myJob.update_job()
    
    > myList = listOfJobs( NUMBER_OF_SIMS, existing=False, load=True )
    > myList.print_list( )
    > save( myList, fileName='listOFJobs_save.pickle' )
    > myList_load = load( fileName='listOFJobs_save.pickle' )
    > myList_load.SIM_NAME
    > myList_load.print_list( )
    """
    def __init__( self, NUMBER_OF_SIMS, existing=False, load=True ):
        
        self.SIZE_OF_NAMES = 128 ### hard coded string size for names 
        
        self.NUMBER_OF_SIMS = NUMBER_OF_SIMS
        self.list_of_jobs = np.ndarray( (NUMBER_OF_SIMS,), dtype=np.object )
        
        #self.list_job_ID   = np.ndarray( (NUMBER_OF_SIMS,), dtype=np.int )
        #self.list_SIM_NAME = np.chararray( (NUMBER_OF_SIMS,), itemsize=self.SIZE_OF_NAMES )
        #self.list_FOLDER   = np.chararray( (NUMBER_OF_SIMS,), itemsize=self.SIZE_OF_NAMES )
        #self.list_status   = np.chararray( (NUMBER_OF_SIMS,), itemsize=self.SIZE_OF_NAMES )
        #self.list_restart  = np.ndarray( (NUMBER_OF_SIMS,), dtype=np.bool )
        #self.list_comments = np.chararray( (NUMBER_OF_SIMS,), itemsize=self.SIZE_OF_NAMES )
        
        ### USELESS
        #if( existing ):
        #    self._existing( SIM_NAME=SIM_NAME_TEMPLATE )
        
        ### init the list of jobs
        tin = time()
        for s in range(self.NUMBER_OF_SIMS):
            self.list_of_jobs[s] = job( SIM_NAME=SIM_NAME_TEMPLATE+'%03d'%(s), existing=existing )
            loadbar( s, self.NUMBER_OF_SIMS, tin )
            
            
    def __getattr__( self, key ):
        if   key == 'job_ID':
            return np.array( [ self.list_of_jobs[s].job_ID for s in range(self.NUMBER_OF_SIMS) ] )
        elif key == 'SIM_NAME':
            return np.array( [ self.list_of_jobs[s].SIM_NAME for s in range(self.NUMBER_OF_SIMS) ] )
        elif key == 'FOLDER':
            return np.array( [ self.list_of_jobs[s].FOLDER for s in range(self.NUMBER_OF_SIMS) ] )
        elif key == 'status':
            return np.array( [ self.list_of_jobs[s].status for s in range(self.NUMBER_OF_SIMS) ] )
        elif key == 'restart':
            return np.array( [ self.list_of_jobs[s].restart for s in range(self.NUMBER_OF_SIMS) ] )
        elif key == 'comments':
            return np.array( [ self.list_of_jobs[s].comments for s in range(self.NUMBER_OF_SIMS) ] )
        raise AttributeError(key)

    def _existing( self, SIM_NAME=SIM_NAME_TEMPLATE ):
        """
        USELESS
        To create a list of jobs from an already created database
        input:
            - SIM_NAME : str, the template of the simulations' folders name, default=SIM_NAME_TEMPLATE (/!\see global variable)
        """
        tin = time()
        for s in range(self.NUMBER_OF_SIMS):
            self.list_of_jobs[s] = job( SIM_NAME=SIM_NAME+'%03d'%(s), existing=True )
            
            #self.list_job_ID[s]    = self.list_of_jobs[s].job_ID
            #self.list_SIM_NAME[s]  = self.list_of_jobs[s].SIM_NAME
            #self.list_FOLDER[s]    = self.list_of_jobs[s].FOLDER
            #self.list_status[s]    = self.list_of_jobs[s].status
            #self.list_restart[s]   = self.list_of_jobs[s].restart
            #self.list_comments[s]  = self.list_of_jobs[s].comments
            
            loadbar( s, self.NUMBER_OF_SIMS, tin )
            
    def update( self ):
        """
        update the jobs status by reading the log files and demand the list of running/pending jobs on the cluster
        TODO: this may be long beacause it will do it for each jobs, where the job list (e.g. ccc_mpp -u gilletnj) may be ask just once for all jobs
        """
        print("UPDATE JOB LIST")
        tin = time()
        ### get once mpp return for all jobs
        mpp_out = self._get_mpp()
        for s in range(self.NUMBER_OF_SIMS):
            self.list_of_jobs[s].update_job( mpp_out=mpp_out )
            #self.list_status[s]    = self.list_of_jobs[s].status
            #self.list_restart[s]   = self.list_of_jobs[s].restart
            
            loadbar( s, self.NUMBER_OF_SIMS, tin )
            
    def _get_mpp( self ):
        """
        return the mpp command, 
        """
        ### look at PEN, RUN
        mpp_out = os.popen( "ccc_mpp -u gilletnj" )        
        return mpp_out
            
    def print_list( self, only_restart=False, only_finish=False, only_NOT=False ):
        """
        print all jobs info in columns 
        options:
            - only_restart: bool, only runs that need a restart, default=False
            - only_finish : bool, only runs that are finish, default=False
            - only_NOT    : bool, only runs that have not been running, default=False
        """
        print_all = not(only_restart) and not(only_finish) and not(only_NOT)
        
        print( "ID          NAME        STATUS  RESTART      COMMENT" )
        for s in range(self.NUMBER_OF_SIMS):
            
            if only_restart and self.list_of_jobs[s].restart :
                self.list_of_jobs[s].print_job( header=False )
                
            elif only_finish and self.list_of_jobs[s]=='FIN' :
                self.list_of_jobs[s].print_job( header=False )
                
            elif only_NOT and self.list_of_jobs[s]=='NOT' :
                self.list_of_jobs[s].print_job( header=False )
            
            elif print_all:
                self.list_of_jobs[s].print_job( header=False )
                
    def find_job( self, job_ID ):
        """
        return the job associated to the job_ID
        input:
            - job_ID: int, job ID
        return:
            - job (see Class job)
            - -1 if no corresponding ID
        TODO: find something better than -1 in case of no ID found
        """
        for s in range(self.NUMBER_OF_SIMS):
            if self.list_of_jobs[s].job_ID == job_ID :
                return self.list_of_jobs[s]
        return -1
    
    def launch_restart( self ):
        ### first update jobs status
        self.update()
        ### then restart all jobs that need to be restarted
        count = 0
        for s in range(self.NUMBER_OF_SIMS):
            if self.list_of_jobs[s].restart :
                self.list_of_jobs[s].launch()
                count += 1
        print( '%d jobs restarted'%count )
        
######
######
### TODO: is it possible to do this INSIDE the Class listOfJobs ?
def save( listOfJobs, fileName='listOFJobs_save.pickle' ):
    """
    save a list of job
    input:
        - listOfJobs: Class listOfJobs object, save the list in a pickle
        - fileName  : str                    , name of the pickle file, default='listOFJobs_save.pickle'
    """
    pickle.dump( listOfJobs, open(fileName,'wb') )
        
def load( fileName='listOFJobs_save.pickle' ):
    """
    load a list of job (see Class listOfJobs) from a pickle file
    input:
        - fileName  : str, name of the pickle file, default='listOFJobs_save.pickle'
    return:
        - Class listOfJobs object
    """
    return pickle.load( open(fileName,'rb') )


# In[ ]:

# myList = listOfJobs( 3, existing=True )
# myList.list_SIM_NAME
# save( myList )
# myList_load = load()
# myList_load.list_SIM_NAME
# myList_load.print_list( )
# myList.print_list( )

# test_job = job( SIM_NAME='simu_2' )
# test_job.print_job()
# test_job._read_log()
# test_job2 = job( SIM_NAME='sim_000', existing=True )
# test_job2.print_job()

