import sys

from util.common import try_prog
from util.common import onerange

def genProg(steps_num):
    result = ""
    
    result += "(define A::(-> int int int))\n" # Value of a_i after t steps
    
    var_num = 8
    goal = 157
    
    # The initial value of a_i is i (1-indexed)
    result += "(assert (and "
    for v in onerange(var_num):
        result += "(= (A %d 0) %d) " % (v, v+1)
    result += "))\n"
    
    # 
    result += "(assert (and "
    for t in range(steps_num):
        result += "(or "
        for v in onerange(var_num):
            if v > 1 and v < var_num:
                result += "(and "
                
                # The chosen one to take a step
                result += "(= (A %d %d) (+ (A %d %d) (A %d %d))) " % (v, t+1, v-1, t, v+1, t)
                
                # The rest must stay immutable
                for u in onerange(var_num):
                    if v is u:
                        continue
                    result += "(= (A %d %d) (A %d %d))" % (u, t+1, u, t)
                
                result += ")"
        result += ")"
    result += "))\n"
    
    result += "(assert (or "
    for v in onerange(var_num):
        result += "(= (A %d %d) %d)" % (v, steps_num, goal)
    result += "))\n"
    
    result += "(check)\n"
    result += "(show-model)\n"
        
    return result


def search_sat_prog():
    lowerbound = 1
    upperbound = 50
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
    #prog_str = genProg(3)
    #print prog_str
    #print try_prog(prog_str)[1]
    
    search_sat_prog()
    
    #result, output = try_prog(prog_str)
    
    #print result
    #print output
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
