#!/bin/python
import os
import fnmatch
from subprocess import Popen, PIPE

subjects = {26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 44, 45, 46, 47, 48, 54, 56, 59, 61, 63, 64} 
tasks = 4

data = {}
for subj in subjects:
    data[subj] = {}
    for i in range(1,tasks+1):
        data[subj][i] = []
    print "subject :", subj
    for file in os.listdir('../data/subj'+str(subj)):
        for i in range(1,tasks+1):
            if fnmatch.fnmatch(file, str(subj)+'_*_'+str(i)+'.data'):
                print "task ",i," file:", file
                trial_number = file.split("_")[1]
                output_file = open('./output/'+str(subj)+"_"+trial_number+"_"+str(i)+".out")
                for line in output_file:
                    line = line.strip()
                    if line.startswith("Feature"):
                        weights = [ float(x) if len(x) > 0 else 0 for x in line.split(":")[1].split(",") ]
                        weights.append(trial_number)
                data[subj][i].append(weights)

    for i in range(1,tasks+1):
        print "Task", i
        for idx in range(len(data[subj][i])):
            weights = data[subj][i][idx]
            total_weight = 0
            for j in range(4):
                total_weight += abs(weights[j])
            for j in range(4):
                data[subj][i][idx][j] /= total_weight 
        for weights in data[subj][i]:
            print weights

    for i in range(1,tasks+1):
        # 1,2,3 -> 4
        # 1,2,4 -> 3
        # 1.3.4 -> 2
        # 2.3,4 -> 1
        print "Eavluating Task", i
        for idx in range(len(data[subj][i])):
            weights = [0.0,0.0,0.0,0.0] # data[subj][i][idx]
            base_trial_number = data[subj][i][idx][-1] 
            for idx2 in range(len(data[subj][i])):
                if idx2 != idx:
                    for w in range(4): # iterate through weights
                        weights[w] += data[subj][i][idx2][w]
            for w in range(4): # iterate through weights
                weights[w] /= 3.0
            p = Popen(['./test_reward', str(subj), str(base_trial_number), str(i), str(weights[0]), str(weights[1]), str(weights[2]), str(weights[3])],stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            print out
            output_file = open('./three_fold_test/'+str(subj)+"_"+str(base_trial_number)+"_"+str(i)+".out", "w")
            output_file.write(out)
            output_file.close()
                    
                    
