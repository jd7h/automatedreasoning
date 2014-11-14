import sys

from util.common import try_prog
from util.common import onerange

def genProg():
    result = ""
    
    # First parameter is shape_id
    result += "(define H::(-> int int))\n"
    result += "(define W::(-> int int))\n"
    result += "(define X::(-> int int))\n"
    result += "(define Y::(-> int int))\n"
    
    bounds = (10, 10)
    
    rectangle_lengths = [2, 3, 4, 5, 6, 7, 8, 9]
    squares = [(4, 4), (6, 6)]
    rectangles = [(1, l) for l in rectangle_lengths]
    
    shapes = squares + rectangles # shape_id is the index of the shape-tuple in this list
    
    
    # All shapes can be orientated horizontally or vertically, with dimensions W,H or H,W
    result += "(assert (and \n"
    for i in range(len(shapes)):
        shape_w, shape_h = shapes[i]
        
        if shape_w == shape_h: # Squares (superfluous constraint)
            result += "(and (= (W %d) %d) (= (H %d) %d))\n" % (i, shape_w, i, shape_h) # We tell Yices that shape i has the dimensions shape_w, shape_h.
        else:
            result += "(xor " # We tell Yices that shape i has the dimensions shape_w, shape_h OR shape_h, shape_w.
            result += "(and (= (W %d) %d) (= (H %d) %d))" % (i, shape_w, i, shape_h) 
            result += "(and (= (W %d) %d) (= (H %d) %d))" % (i, shape_h, i, shape_w)
            result += ")\n"
    result += "))\n"
    
    
    # All shapes must be within bounds
    result += "(assert (and \n"
    for i in range(len(shapes)):
        # x >= 0 && y >= 0
        result += "(>= (X %d) 0) " % i
        result += "(>= (Y %d) 0) " % i
        # x + w <= bound_w && y + h <= bound_h
        result += "(<= (+ (X %d) (W %d) 0) %d) " % (i, i, bounds[0])
        result += "(<= (+ (Y %d) (H %d) 0) %d) " % (i, i, bounds[1])
    result += "))\n"
    
    
    # All shapes may not overlap
    result += "(assert (not (or \n"
    for i in range(len(shapes)):
        for j in range(len(shapes)):
            if j >= i: # Need check whole matrix, except for itself
                continue
            
            shape_i_w, shape_i_h = shapes[i]
            shape_j_w, shape_j_h = shapes[j]
            
            # Do the shapes overlap?
            result += "(and \n" # Both x- and y-axis
            
            # x-axis
            result += "(or "
            # X_i <= X_j && X_j < X_i + W_i
            result += "(and (<= (X %d) (X %d)) (< (X %d) (+ (X %d) (W %d)))) " % (i, j, j, i, i)
            # X_i < X_j + W_j && X_j + W_j <= X_i + W_i
            result += "(and (< (X %d) (+ (X %d) (W %d))) (<= (+ (X %d) (W %d)) (+ (X %d) (W %d))))" % (i, j, j, j, j, i, i)
            
            # X_j <= X_i && X_i < X_j + W_j
            result += "(and (<= (X %d) (X %d)) (< (X %d) (+ (X %d) (W %d)))) " % (j, i, i, j, j)
            # X_j < X_i + W_i && X_i + W_i <= X_j + W_j
            result += "(and (< (X %d) (+ (X %d) (W %d))) (<= (+ (X %d) (W %d)) (+ (X %d) (W %d))))" % (j, i, i, i, i, j, j)
            result += ")\n"
            
            # y-axis
            result += "(or "
            # Y_i <= Y_j && Y_j < Y_i + H_i
            result += "(and (<= (Y %d) (Y %d)) (< (Y %d) (+ (Y %d) (H %d)))) " % (i, j, j, i, i)
            # Y_i < Y_j + H_j && Y_j + H_j <= Y_i + H_i
            result += "(and (< (Y %d) (+ (Y %d) (H %d))) (<= (+ (Y %d) (H %d)) (+ (Y %d) (H %d))))" % (i, j, j, j, j, i, i)
            
            # Y_j <= Y_i && Y_i < Y_j + H_j
            result += "(and (<= (Y %d) (Y %d)) (< (Y %d) (+ (Y %d) (H %d)))) " % (j, i, i, j, j)
            # Y_j < Y_i + H_i && Y_i + H_i <= Y_j + H_j
            result += "(and (< (Y %d) (+ (Y %d) (H %d))) (<= (+ (Y %d) (H %d)) (+ (Y %d) (H %d))))" % (j, i, i, i, i, j, j)
            result += ")\n"
            
            result += ")\n"
    
    result += ")))\n"
    
    
    # Find an example for which the following constraints are violated
    result += "(assert (not (and\n"
    
    # Rectangles 1x8 and 1x9 must be placed in parallel
    parallel_set = [8, 9]
    parallel_shapes = []
    
    # Find the shapes 1x8 and 1x9
    for i in range(len(shapes)):
        shape_w, shape_h = shapes[i]
        if not (shape_h in parallel_set and shape_w == 1):
            continue
        parallel_shapes.append(i)
    
    result += "(xor \n"
    
    # Vertical
    result += "(and \n"
    for i in parallel_shapes:
        shape_w, shape_h = shapes[i]
        result += "(and (= (W %d) %d) (= (H %d) %d))\n" % (i, shape_w, i, shape_h)
    result += ")\n"
    
    # Horizontal
    result += "(and \n"
    for i in parallel_shapes:
        shape_w, shape_h = shapes[i]
        result += "(and (= (W %d) %d) (= (H %d) %d))\n" % (i, shape_h, i, shape_w)
    result += ")\n"
    
    result += ")\n"
    
    
    # Not all non-square rectangles may be placed in parallel
    result += "(not (xor \n"
    
    # Vertical
    result += "(and \n"
    for i in range(len(shapes)):
        shape_w, shape_h = shapes[i]
        
        if shape_w == shape_h: # ignore square rectangles
            continue
        
        result += "(and (= (W %d) %d) (= (H %d) %d))\n" % (i, shape_w, i, shape_h)
    result += ")\n"
    
    # Horizontal
    result += "(and \n"
    for i in range(len(shapes)):
        shape_w, shape_h = shapes[i]
        
        if shape_w == shape_h: # ignore square rectangles
            continue
        
        result += "(and (= (W %d) %d) (= (H %d) %d))\n" % (i, shape_h, i, shape_w)
    result += ")\n"
    
    result += "))\n"
    
    result += ")))\n"
    
    
    result += "(check)\n"
    result += "(show-model)\n"
        
    return result


def main():
    prog_str = genProg()
    print prog_str
    print try_prog(prog_str)[1]
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
