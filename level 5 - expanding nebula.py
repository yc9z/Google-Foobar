"""
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. But - oh no! - one of the escape pods has flown into a nearby nebula, causing you to lose track of it. You start monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. However, you do find that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine the previous state of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid. You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

For example, let's say the previous state of the grid (p) was:
.O..
..O.
...O
O...

To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
.O -> O
..

Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:
O. -> .
.O

Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
O.O
.O.
O.O

Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.  The answer will always be less than one billion (10^9).

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases -- 
Input:
Solution.solution({{true, true, false, true, false, true, false, true, true, false}, {true, true, false, false, false, false, true, true, true, false}, {true, true, false, false, false, false, false, false, false, true}, {false, true, false, false, false, false, true, true, false, false}})
Output:
    11567

Input:
Solution.solution({{true, false, true}, {false, true, false}, {true, false, true}})
Output:
    4

Input:
Solution.solution({{true, false, true, false, false, true, true, true}, {true, false, true, false, false, false, true, false}, {true, true, true, false, false, false, true, false}, {true, false, true, false, false, false, true, false}, {true, false, true, false, false, true, true, true}}
Output:
    254

-- Python cases -- 
Input:
solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
Output:
    11567

Input:
solution.solution([[True, False, True], [False, True, False], [True, False, True]])
Output:
    4

Input:
solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
Output:
    254
"""

import collections

def solution(g):

    def generate_all_two_squares():
        all_squares = []
            
        for x in one_arrays:
            for y in one_arrays:
                for z in one_arrays:
                    for w in one_arrays:
                        all_squares += [[[x,y],[z,w]]]

        return all_squares
        
    
    def generate_start():

        threes = []

        for top in [t for t in two_squares if next_gas(t) == sub[0][0]]:

            for right in [r for r in two_squares if r[0][0] == top[0][1] and r[1][0] == top[1][1] and next_gas(r) == sub[0][1]]:
                for bottom in [b for b in two_squares if b[0][0] == top[1][0] and b[0][1] == top[1][1] and next_gas(b) == sub[1][0]]:
                    for corner in [c for c in two_squares if c[0][0] == top[1][1] and c[0][1] == right[1][1] and c[1][0] == bottom[1][1] and next_gas(c) == sub[1][1]]:
                        three = [top[0]+[right[0][1]],top[1]+[right[1][1]],bottom[1]+[corner[1][1]]]
                        threes += [three]
                        
        return threes

    def next_gas(two_square):
        l = len(two_square)
        num = 0

        for row in two_square:
            for x in row:
                if x == True:
                    num += 1
        return True if num == 1 else False
        
    
    def next_pos(i,j,n,m):
        if j<m-2: return i, j+1
        if i<n-2: return i+1, 0
        return n-1,m-1


    def find_three_arrays():
        add_ons = []
        states = [True,False]
        
        for i in states:
            for j in states:
                for k in states:
                    add_ons += [(i,j,k)]
                    
        return add_ons


    def check_two_compatible(i,j):
        
        cur = sub[i][j]
        square = [[pre[i][j],pre[i][j+1]],[pre[i+1][j],pre[i+1][j+1]]]
        gas = next_gas(square)

        return cur == gas
    
        
    def find_pre(i,j,sub_id): # the left-top box of the two-box being considered
        n, m = len(sub), len(sub[0])
        
        if i == n-1 and j == m-1:
            right_side = tuple([pre[k][m] for k in range(n+1)])
            right_sides[sub_id][right_side] += 1
           
            if sub_id > 0:
                left_side = tuple([pre[k][0] for k in range(n+1)])
                left_sides[sub_id-1][left_side][right_side] += 1
                
            return

        elif i == j == 0:
            threes = generate_start()
            
            for three in threes:
                for k in range(3):
                    pre[k][:3] = three[k]
                    
                i_next,j_next = next_pos(i,j,n,m)
                find_pre(i_next,j_next,sub_id)
            
        elif i>0 and j>0:
            for new in one_arrays:
                pre[i+2][j+2] = new
                if check_two_compatible(i+1,j+1):
                    i_next,j_next = next_pos(i,j,n,m)
                    find_pre(i_next,j_next,sub_id)

        elif i == 0:
            for x,y,z in three_arrays:
                pre[0][j+2],pre[1][j+2],pre[2][j+2] = x,y,z
                
                can_use = True
                for k in range(0,2):
                    if not check_two_compatible(k,j+1):
                        can_use = False
                        
                if can_use:
                    i_next,j_next = next_pos(i,j,n,m)
                    find_pre(i_next,j_next,sub_id)

        elif j == 0:
            for x,y,z in three_arrays:
                pre[i+2][0],pre[i+2][1],pre[i+2][2] = x,y,z
                
                can_use = True
                for k in range(0,2):
                    if not check_two_compatible(i+1,k):
                        can_use = False
                        
                if can_use:
                    i_next,j_next = next_pos(i,j,n,m)
                    find_pre(i_next,j_next,sub_id)

    
        
    h, w = len(g), len(g[0])
    
    if w%3 == 1:
        num_subs = (w-1)//3
        sub_division_points = [0]+[i for i in range(4,w,3)]+[w]
    else:
        num_subs = (w-1)//3+1
        sub_division_points = [0]+[i for i in range((w-1)%3+1,w,3)]+[w]

    one_arrays = [True,False]
    two_squares = generate_all_two_squares()
    three_arrays = find_three_arrays()
    
    left_sides = [collections.defaultdict(collections.Counter) for i in range(num_subs)]
    right_sides = [collections.Counter() for i in range(num_subs)]

    for sub_id in range(num_subs):
        left_end,right_end = sub_division_points[sub_id],sub_division_points[sub_id+1]
        sub = [list(g[j][left_end:right_end]) for j in range(h)]
        pre = [['*']*(right_end-left_end+1) for i in range(h+1)]
        find_pre(0,0,sub_id)
        
    total = 0

    for i in range(num_subs-1):
        glued = collections.Counter()
        for side in right_sides[i]:
            for right in left_sides[i][side]:
                glued[right] += right_sides[i][side]*left_sides[i][side][right]
        right_sides[i+1] = glued

    return sum(right_sides[num_subs-1].values())

neb =[[True, False, True], [False, True, False], [True, False, True]]
print(solution(neb))

