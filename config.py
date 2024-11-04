#simulation Time
MAX_SIMULATION_TIME = 30000

#cloud server attributes
CLOUD_COST_UNIT_TIME = 0.01
CLOUD_CPU_SPEED = 48000

#FOG ENERGY COST
FD_ENERGY_PER_SLOT = 2
MAX_REWARD = 100

#capacity
FD_CAPACITY1 = 10
FD_CAPACITY3 = 10
FD_CAPACITY5 = 10

#CPU speed instructions per second
CPU_SPEED1 = 2000
CPU_SPEED2 = 2000
CPU_SPEED3 = 2000

#latency
LATENCY_CS_FR = 50
LATENCY_ED_FR = 2

#three types of jobs
#job types
NORMAL_ALERTS   = 1
EMERGENCY_ALERTS = 2
RECOMENDATIONS  =  3

#number of instructions (in bytes) in each job Type
NO_INSTRUCTIONS1 = 40000
NO_INSTRUCTIONS2 = 40000
NO_INSTRUCTIONS3 = 40000

#job data size
DATA_SIZE1 = 1000
DATA_SIZE2 = 1000
DATA_SIZE3 = 1000

SLOT_TIME =  NO_INSTRUCTIONS3 / CPU_SPEED1

#number of Cluster-Fog devices 
numOfFDs = 3
#number of Edge devices per cluster
numOfEDs = 100

#create task list with empty 
jobQ = []
ClusterRs = []
EdgeRs =[]
deletedClusterRs =[]

state_list = []
action_list = ['UP', 'DOWN', 'NONE','BALANCE']
