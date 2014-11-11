import sys

from util.common import try_prog
from util.common import onerange

def genProg(time):
    def runtime(i):
        return i+5 # The paper uses 1-indexed jobs

    result = ""
    
    result += "(define Status::(-> int int int))\n"
    
    job_num = 12
    
    # Job status is {0,1,2}
    result += "(assert (and "
    for j in onerange(job_num):
        for t in range(time):
            result += "(>= (Status %d %d) 0) (<= (Status %d %d) 2) " % (j, t, j, t)
    result += "))\n"
    
    #the running time of job j is j+5
    result += "(assert (and \n"
    for j in onerange(job_num):
        r = runtime(j)
        result += "(or \n"
        for t in range(time - r + 1):
            result += "(and "
            
            # Before the start, the job is not running
            for tt in range(t):
                result += "(= (Status %d %d) 0) " % (j,tt)
            
            # After start, the job is running    
            for rt in range(r):
                result += "(= (Status %d %d) 1) " % (j,t+rt)
            
            # After done running, the job is completed, and stays completed until end of scope
            for tt in range(time - t - r): # Time we have, minus time we did not do anything, minus time the job takes to run
                result += "(= (Status %d %d) 2) " % (j,t+r+tt)
            
            result += ")\n"
        result += ")\n"
    result += "))\n" 
    
    result += "(assert (and \n"
    for t in range(time):
        # Job 3 may only start if jobs 1 and 2 have finished
        result += "(=> (= (Status 3 %d) 1) (and (= (Status 1 %d) 2) (= (Status 2 %d) 2)))" % (t, t, t)
        
        # Job 5 may only start if jobs 3 and 4 have finished
        result += "(=> (= (Status 5 %d) 1) (and (= (Status 3 %d) 2) (= (Status 4 %d) 2)))" % (t, t, t)
        
        # Job 7 may only start if jobs 3, 4 and 6 have finished
        result += "(=> (= (Status 7 %d) 1) (and (= (Status 3 %d) 2) (= (Status 4 %d) 2) (= (Status 6 %d) 2)))" % (t, t, t, t)
    
        # Job 8 may not start earlier than job 5
        result += "(=> (= (Status 8 %d) 1) (>= (Status 5 %d) 1))" % (t, t)
    
        # Job 9 may only start if jobs 5 and 8 have finished
        result += "(=> (= (Status 9 %d) 1) (and (= (Status 5 %d) 2) (= (Status 8 %d) 2)))" % (t, t, t)
    
        # Job 11 may only start if job 10 has finished
        result += "(=> (= (Status 11 %d) 1) (= (Status 10 %d) 2))" % (t, t)
    
        # Job 12 may only start if jobs 9 and 11 have finished
        result += "(=> (= (Status 12 %d) 1) (and (= (Status 9 %d) 2) (= (Status 11 %d) 2)))" % (t, t, t)
    
        # Job 5, 7 and 10 require a special equipment of which only on which only one copy is available, so no two of these jobs may run at the same time
        result += "(<= (+ (ite (= (Status 5 %d) 1) 1 0) (ite (= (Status 7 %d) 1) 1 0) (ite (= (Status 10 %d) 1) 1 0)) 1)" % (t, t, t)
        
    result += "))\n"
    
    result += "(check)\n"
    result += "(show-model)\n"
        
    return result


def search_sat_prog():
    lowerbound = 1
    upperbound = 100
    last_success_output = None
    
    while lowerbound != upperbound:
        i = lowerbound + (upperbound - lowerbound) / 2
        print "%d (%d, %d)" % (i, lowerbound, upperbound)
        result, output = try_prog(genProg(i))
        print result
        
        if result:
            last_success_output = output
            upperbound = i
        else:
            lowerbound = i+1
    
    print last_success_output
    
    return lowerbound  # Is equal to upperbound
    

def main():
    #prog_str = genProg(56)
    #print try_prog(prog_str)[1]
    
    search_sat_prog()
    
    #result, output = try_prog(prog_str)
    
    #print result
    #print output
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
