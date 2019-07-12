'''
Challenge 5.1
Disorderly Escape
=================
Oh no! You've managed to free the bunny prisoners and escape Commander Lambdas exploding space station, but her team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll be shot out of the sky!
Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted her space station in the middle of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial bodies in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations each quadrant could possibly have, so that you can pick the optimal quadrant through which youll make your jump. 
There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid, configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations, if you exchange the position of any two columns or any two rows some number of times, youll find that all of those configurations are equivalent in that way - in grouping, rather than order.
Write a function answer(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations that can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states. Equivalency is defined as above: any two star grids with each celestial body in the same state where the actual order of the rows and columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width and height of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each grid, the number of states of those bodies is between 2 and 20, inclusive. The answer can be over 20 digits long, so return it as a decimal string.  The intermediate values can also be large, so you will likely need to use at least 64-bit integers.
For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent) or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.
00
00
In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or column would keep it in the same state.
00 00 01 10
01 10 00 00
1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 4 positions.  All four of the above configurations are equivalent.
00 11
11 00
2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply moves them between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row with two bodies in state 1, and two columns with one of each state.
01 10
01 10
2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because there's no way to transpose the grid.
01 10
10 01
2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent to each other.
01 10 11 11
11 11 01 10
3 noisy celestial bodies, similar to the case where only one of four is noisy.
11
11
4 noisy celestial bodies.
There are 7 distinct, non-equivalent grids in total, so answer(2, 2, 2) would return 7.
Languages
=========
To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java
Test cases
==========
Inputs:
    (int) w = 2
    (int) h = 2
    (int) s = 2
Output:
    (string) "7"
Inputs:
    (int) w = 2
    (int) h = 3
    (int) s = 4
Output:
    (string) "430"
'''


import collections

def solution(w, h, s):
    
    def factorial(n):
        ans = 1
        for i in range(1,n+1):
            ans *= i
            
        return ans
        
        
    def gcd(n,m):
        n,m = max(n,m), min(n,m)
        if not m: return n
        return gcd(m,n%m)
    
    # generate all types of permutaition of [1,..,n]
    # a type is of the form (a_1,a_2,...,a_k) where
    # a_i's are weakly increasing and are lenth of cycles
    def perm_type(n):
        dp = [[[] for j in range(n+1)] for i in range(n+1)]

        for m in range(1,n+1):
            for j in range(1,m+1):
                if j == m:
                    dp[m][j] = [[m]]
                else:
                    dp[m][j] = [t+[j] for b in range(1,j+1) for t in dp[m-j][b]]
        
        ans = []
        for i in range(1,n+1):
            ans += dp[n][i]
            
        return ans
            
    # count the number of permutations of a fixed type
    def count_type(typ,n):
        ans = factorial(n)
        num = collections.Counter(typ)
        
        for t in typ:
            ans //= t
        
        for m in num:
            ans //= factorial(num[m])
            
        return ans


    # count the number of cycles of the h*w lattice
    # when rows have permutation type1
    # and cols have have permutation type2
    def count_cycle_num(type1, type2):
        ans = 0
        
        for t1 in type1:
            for t2 in type2:
                ans += gcd(t1,t2)

        return ans
                
    # count the number of actions grouped by number of cycles    
    def count_actions(w,h):
        num_actions = [0]*(w*h)

        for type1 in perm_type(h):
            type1_num = count_type(type1,h)
            for type2 in perm_type(w):
                type2_num = count_type(type2,w)

                cycle_num = count_cycle_num(type1, type2)
                num_actions[cycle_num-1] += type1_num*type2_num
                
        return num_actions
    
        
    # Polya enumeration theorem
    def orbit_with_color(w,h,s):
        count = 0
        
        for c in range(1,w*h+1):
            count += s**c*num_actions[c-1]
        
        return count//(factorial(w)*factorial(h))


    num_actions = count_actions(w,h)
    
    return str(orbit_with_color(w,h,s))
            

w,h,s = 2, 2, 2
print(solution(w,h,s))
