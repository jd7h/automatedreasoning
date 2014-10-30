import sys

from util.common import try_prog

def genProg():
    def runtime(i):
        return i+5+1

    result = ""
    
    result += "(define Status::(-> int int int))\n"
    
    job_num = 3
    time = 10
    
    # Job status is {0,1,2}
    result += "(assert (and "
    for j in range(job_num):
        for t in range(time):
            result += "(>= (Status %d %d) 0) (<= (Status %d %d) 2) " % (j, t, j, t)
    result += "))\n"
    
    #the running time of job j is j+5
    #als Status j t-1 == 0 en Statuis j t == 1 DAN voor alle t' met t' <= t+j+5 geldt dat Status j t' == 1
    result += "(assert (and \n"
    for j in range(job_num):
        r = runtime(j)
        result += "(or \n"
        for t in range(time - r + 1):
            result += "(and "
            
            # Before the start, the job is not running
            for tt in range(t):
                result += "(= (Status %d %d) 0) " % (j,tt)
            
            # After start, the job is running    
            for tt in range(r):
                result += "(= (Status %d %d) 1) " % (j,t+tt)
            
            # After done running, the job is completed, and stays completed until end of scope
            for tt in range(time - t - r): # Time we have, minus time we did not do anything, minus time the job takes to run
                result += "(= (Status %d %d) 2) " % (j,t+r+tt)
            
            result += ")\n"
        result += ")\n"
    result += "))\n" 
    
    result += "(check)\n"
    result += "(show-model)\n"
    
    
    return result

def main():
    prog_str = genProg()
    print prog_str
    
    result, output = try_prog(prog_str)
    
    print result
    print output
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
