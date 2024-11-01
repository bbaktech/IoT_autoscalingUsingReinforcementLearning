import random
import RLAgent
from config import MAX_SIMULATION_TIME
from devices import Cloud, EdgeDevice, FogDevice, Job,logentry, cs,tt,STATE
from config import ClusterRs,jobQ,EdgeRs,numOfEDs,numOfFDs,deletedClusterRs
import random

class Environment:
    def __init__(self) :
        self.job_sl_no = 0
        self.no_cluster_id = 0
        self.no_edge_id = 0

    def createLoad(self,s_time,Slot):
        jobQ.clear()
        for device in EdgeRs:
            job = device.CreateUploadJob()
            if job is not None:
                job.setSlotNo(Slot)
                job.setSubmitime(s_time)
                job.setSerial(self.job_sl_no )
                self.job_sl_no += 1
                #task is added to TaskQueue
                jobQ.append(job)

    def ArangeLoad(self):
            no_jobs = len(jobQ)
            if no_jobs > 0:
                i = 0
                while i< no_jobs:
                    for fr in ClusterRs:
                        for j in range(fr.no_core):
                            job = jobQ[i]
                            job.fd_devid = fr.id
                            i += 1
                            if i==no_jobs:
                                break
                        if i==no_jobs:
                            break
                    if i< no_jobs :
                        job = jobQ[i]
                        job.fd_devid = ClusterRs[0].id
                        i += 1

    def CreateClusters(self,fds):
        ClusterRs.clear()
        for i in range(fds):                
            fr = FogDevice (self.no_cluster_id,"ClusterFR:"+str(self.no_cluster_id))
            self.no_cluster_id += 1
            ClusterRs.append(fr)

    def CreateEdgeDevises(self,eds):
        EdgeRs.clear()
        self.no_edge_id = 0
        for j in range(eds):
            #create edge device connected to random cluster 
            i = random.randint(0,len(ClusterRs)-1)
            FR = ClusterRs[i]
            if FR is not None:
                ed = EdgeDevice(self.no_edge_id, "EdgeD_"+str(FR.id)+"_"+str(self.no_edge_id))
                self.no_edge_id += 1
                #set the cluster id to newly created edge
                ed.setClusterId(FR.id)
                EdgeRs.append(ed)
    
    def GetFogResource(self, f_id):
            for fr in ClusterRs:
                if fr.id == f_id :
                    return fr
            return None

    def RemoveCluster(self, cl_id):
        #remove fog resource i
        cl = self.GetFogResource(cl_id)
        deletedClusterRs.append(cl)
        ClusterRs.remove(cl)
        cl_indx = random.randint(0, len(ClusterRs)-1)
        n_cl_id = ClusterRs[cl_indx].id
        #distribute edgesto other clusters
        for ed in EdgeRs:
            if ed.connected_cl_id == cl_id :
                #move edge to new cluster n_cl_id
                ed.setname(str(n_cl_id))
                ed.setClusterId(n_cl_id)
                #set the cluster id to newly created edge             

    def AddCluster(self):
        #add new fog resource and half edges of cl_id should be diricted to new fog
        fr = FogDevice (self.no_cluster_id, "ClusterFR:"+str(self.no_cluster_id))
        self.no_cluster_id += 1
        ClusterRs.append(fr)

    #pls add edge id
    def ReconnectEdge(self, edgeid, clsid):
        for ed in EdgeRs:
                if ed.id == edgeid:
                    ed.setClusterId(clsid)
                    
    #new edge will be connected to   cl_id  
    def AddEdge(self, cl_id = 0):
        eds = len(EdgeRs)
        ncls = len(ClusterRs)
        ed = EdgeDevice(self.no_edge_id, "EdgeD_"+str(cl_id)+"_"+str(self.no_edge_id))
        self.no_edge_id +=1
        #set the cluster id to newly created edge
        ed.setClusterId(cl_id)
        EdgeRs.append(ed)

    def RemoveEdge(self, edg_id):
        r_ed = None
        for ed in EdgeRs:
            if ed.id == edg_id:
                r_ed = ed        
        EdgeRs.remove(r_ed)
