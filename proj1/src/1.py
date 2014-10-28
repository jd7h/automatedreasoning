import sys

def genProg():
    result = ""
    
    obj_num = 5
    supply = [4, 20, 8, 10, 5]
    weights = [700, 800, 1000, 1500, 100]
    
    assert obj_num == len(weights)
    assert obj_num == len(supply)
    
    truck_num = 6
    max_pallet = 8
    max_weight = 7800
    
    result += "(define Pallets::(-> int int int))\n"
    
    # A truck can not carry negative amount of pallets
    result += "(assert (and "
    for t in range(truck_num):
        for o in range(obj_num):
            result += "(<= 0 (Pallets %d %d)) " % (t, o)
    
    result += "))\n"
    
    # Each truck can only carry max_pallet count pallets
    for t in range(truck_num):
        result += "(assert (>= %d (+ " % max_pallet
        for o in range(obj_num):
            result += "(Pallets %d %d) " % (t, o)
        result += ")))\n"
    
    # The sum of the weight of any truck may not be higher than max_weight
    for t in range(truck_num):
        result += "(assert (>= %d (+ " % max_weight
        for o in range(obj_num):
            result += "(* (Pallets %d %d) %d) " % (t, o, weights[o])
        result += ")))\n"
    
    # There may not be prittles (1) and crottles(3) in the same truck
    for t in range(truck_num):
        result += "(assert (not (and "
        result += "(> (Pallets %d 1) 0) " % t
        result += "(> (Pallets %d 3) 0) " % t
        result += ")))\n"
    
    # Two trucks max may carry skipples (2)
    result += "(assert (>= 2 (+ "
    for t in range(truck_num):
        result += "(ite (> (Pallets %d 2) 0) 1 0) " % t
    result += ")))\n"
    
    # All the pallets in Supply must be delivered
    for o in range(obj_num):
        if supply[o] is not None:
            result += "(assert (= %d (+ " % supply[o]
            
            for t in range(truck_num):
                result += "(Pallets %d %d) " % (t, o)
            
            result += ")))\n"
    
    result += "(check)\n"
    result += "(show-model)\n"
    
    return result

def main():
    print genProg()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
