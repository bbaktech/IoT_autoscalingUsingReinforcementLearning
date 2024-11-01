import os
import random

import numpy as np
import RLAgent
from config import DATA_SIZE1, FD_CAPACITY1, MAX_REWARD, MAX_SIMULATION_TIME, NO_INSTRUCTIONS1, NORMAL_ALERTS, SLOT_TIME,FD_ENERGY_PER_SLOT
from config import ClusterRs,jobQ,EdgeRs,numOfEDs,numOfFDs,state_list,action_list,deletedClusterRs
from devices import Cloud, EdgeDevice, FogDevice, Job,logentry, cs,tt,slotTT,STATE
from IoTEnvironment import Environment

output_dir = "model_output/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

env = Environment()
env.CreateClusters(fds = numOfFDs)

print("Cluster-Fds (FogDevices)")
for device in  ClusterRs:
    print("   "+device.name +"  Cores:"+str(device.no_core) + "    CPU Speed:" + str(device.cpu_speed) )
# print("Edge Devices " )
# for device in EdgeRs:
#     print ("   "+device.name + "(Connected to ClusterFR:"+ str(device.connected_cl_id) + ")")

#learning agent state_size(1.number of fog nodes, 2. number of jobs)
state_size = 2
Slot = 0
sim_time = 0.
sl_no = 0
slot_avg_delay = 0.
batch_size = 32
agent = RLAgent.DQNAgent(state_size = 2, action_size= len(action_list))
#agent.load_mdl()

print("Simulation Started")

while MAX_SIMULATION_TIME > sim_time:
    slot_avg_delay = 0. #used to write to file
    Slot+=1

    #clean buffer of cluster-fog devises to receive tasks
    for device in ClusterRs:
        device.clean()
    cs.clear()
    slotTT.clear()
    no_edge_devices =  random.randint(50,100)
    env.CreateEdgeDevises(eds = no_edge_devices)
    
    #CREATE LOAD
    env.createLoad(sim_time, Slot)

    #1.  call RL Agent to get action by giving STATE and LOAD
    #present state
    state = []
    state.append(len(ClusterRs))
    state.append(len(jobQ))
    p_state = np.reshape(state, [1, state_size])
    action = agent.act(p_state)

    #WRITE UPDAPRESENT STATE SUGGESTED ACTION TO LOG
    msg = "\nSlot No:"+str(Slot)+ " Jobs:"+str(len(jobQ))  + ' number of clusters:'+ str(len(ClusterRs)) +"\n"+ action_list[action]
    #write slot number to slot_log file
    logentry.WriteStringToSlotsLog(msg)

    #2.  Take action accoring to RL Agent suggestion
    if action_list[action] == 'UP':
        env.AddCluster()
        env.ArangeLoad()
        print('UP')
    elif action_list[action] == 'DOWN':
        print('DOWN')
        no_cls = len(ClusterRs)
        if no_cls > 1:
            sr_cl = random.randint(0, no_cls-1)
            env.RemoveCluster(ClusterRs[sr_cl].id)
        env.ArangeLoad()
    elif action_list[action] == 'BALANCE':
        print('BALANCE')
        env.ArangeLoad()
    else:
        print('NONE')

    #new state 
    state = []
    state.append(len(ClusterRs))
    state.append(len(jobQ))
    n_state = np.reshape(state, [1, state_size])

    #WRITE UPDATED STATE TO LOG
    msg = '\nUpdated number of clusters:'+ str(len(ClusterRs)) +"\n"
    logentry.WriteStringToSlotsLog(msg)

    #3.  Execute the tasks in current slot
    logentry.WriteStringToSlotsLog("-------------------------------------------------------------\n")
    if len(jobQ) > 0:
        for job in jobQ:
            FR = env.GetFogResource(job.fd_devid)
            FR.ExecutesTask(job)

    #4. send feedback / reward  to RL Agent
    enery_parm = FD_ENERGY_PER_SLOT * len(ClusterRs)
    latency_parm = slotTT.AvgTaskCompetionTime()
    #reward2 = abs(100 - reward2 /22.0 *100)

    reward = MAX_REWARD - (enery_parm + latency_parm)
    agent.remember(p_state, action, reward, n_state)

    jobQ.clear()
    for device in ClusterRs:
        device.ComputeSlotLoad()
    cs.WriteSlotSummary()
    
    #WRITE REWARD TO LOG
    msg = 'Avg Eenergy:'+str(enery_parm)+ '  Avg completion time:' + str(latency_parm) + '  Reward:' + str(reward) + '\n'
    logentry.WriteStringToSlotsLog(msg)

    sim_time = sim_time+ SLOT_TIME
    #write the summary of execution of task at each slot to slot_summary log file
    if len(agent.memory) > batch_size:
        agent.train(batch_size) 
    if Slot % 100 == 0:
        agent.save("weights_"
                + "{:04d}".format(Slot) + ".weights.h5")

print("Simulation Completed")
print("-----------Results--------------------")
print("Total Simulation Time:"+ str(MAX_SIMULATION_TIME))
print("Total Number of Slots:"+ str(Slot))		
tt.PrintTimeDetails()
print()

for device in ClusterRs:
    device.PrintResult(Slot )
    print()
for device in deletedClusterRs:
    device.PrintResult(Slot )
    print()

cs.PrintNoTasksExecuted()
print()

print("\nYou could see:")
print("              " + logentry.fnameJobs+ " for details on each job ")
print("              " + logentry.fnameSlots + " for summary of each slot")
print("---------------------------------------");	
