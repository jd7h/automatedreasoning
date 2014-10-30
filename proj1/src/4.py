import sys

from util.common import try_prog

def genProg(steps_num):
    result = ""
    
    result += "(define A::(-> int int int))\n" # Value of a_i after t steps
    
    var_num = 8
    goal = 157
    
    # The initial value of a_i is i (1-indexed)
    result += "(assert (and "
    for v in range(var_num):
        result += "(= (A %d 0) %d) " % (v, v+1)
    result += "))\n"
    
    result += "(assert (and "
    for v in range(var_num):
        for t in range(steps_num):
            if v > 0 and v < var_num-1:
                result += "(or "
                result += "(= (A %d %d) (A %d %d))" % (v, t+1, v, t)
                result += "(= (A %d %d) (+ (A %d %d) (A %d %d))) " % (v, t+1, v-1, t, v+1, t)
                result += ") "
            else:
                result += "(= (A %d %d) (A %d %d))" % (v, t+1, v, t)
    result += "))\n"
    
    result += "(assert (or "
    for v in range(var_num):
        result += "(= (A %d %d) %d)" % (v, steps_num, goal)
    result += "))\n"
    
    result += "(check)\n"
    result += "(show-model)\n"
        
    return result


def search_sat_prog():
    lowerbound = 1
    upperbound = 10
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
    #prog_str = genProg(15)
    #print try_prog(prog_str)[1]
    
    search_sat_prog()
    
    #result, output = try_prog(prog_str)
    
    #print result
    #print output
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
