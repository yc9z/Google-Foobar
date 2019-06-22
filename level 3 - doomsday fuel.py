"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

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
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases -- 
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
"""


import functools

def solution(m):
    
    def stable(row):
        for n in row:
            if n != (0,1):
                return False
        return True
        
    def frac_mult(x,y):
        x1,x2 = x
        y1,y2 = y
        
        num = x1*y1
        denom = x2*y2
        
        d = gcd(num,denom)
        
        return (num//d,denom//d)
   
    def conv_to_frac_and_del_self(row,i):
        l = len(row)
        n = sum(row) - row[i]
        if n == 0: return [(0,1)]*l
        
        for j in range(l):
            d = gcd(row[j],n)
            row[j] = (row[j]//d,n//d)
            
        row[i] = (0,1)
        
        return row
        
    def frac_to_int(lst):
        D = 1
        l = len(lst)
        ints = [0]*l
        
        for _,b in lst:
            D = lcm(D,b)
            
        for i in range(l):
            a,b = lst[i]
            ints[i] = D//b*a
        
        d = functools.reduce(gcd,ints)
     
        for i in range(l):
            ints[i] = ints[i]//d
                
        return ints+[D//d]
        
    def lcm(a,b):
        return a*b//gcd(a,b)
    
    def gcd(a,b):
        a,b = min(a,b),max(a,b)
        if a == 0: return b
        if a>0: return gcd(b%a,a)
        
    def frac_add(x,y):
        x1,x2 = x
        y1,y2 = y
        num,denom = x1*y2+x2*y1, x2*y2
        d = gcd(num,denom)
        return (num//d, denom//d)

    def clear_self(i,row):
        if row[i] == (0,1): return row
        x,y = row[i]
        u,v = frac_add((1,1),(-x,y))
        
        for j in range(len(row)):
            if i != j:
                row[j] = frac_mult(row[j],(v,u))

        row[i] = (0,1)
        return row
            

    def substitute(i,j,r1,r2):
        l = len(r1)
        
        for k in range(l):
            if k != i:
                r2[k] = frac_add(r2[k],frac_mult(r1[k],r2[i]))

        r2[i] = (0,1)
        clear_self(j,r2)

        return r2
            
    
    l = len(m)
    
    for i in range(l):
        m[i] = conv_to_frac_and_del_self(m[i],i)

    stables = [i for i in range(l) if stable(m[i])]

    if 0 in stables: return [1]+[0]*(l-1)+[1]
        
    for i in range(l):
        if i not in stables:
            for j in range(l):
                if i!=j: m[j] = substitute(i,j,m[i],m[j])
    
    end = [m[0][i] for i in range(l) if i in stables]
    
    ans = frac_to_int(end)
    
    return ans

m = [[0, 0, 0, 0, 1, 0], \
     [0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0]]
print(solution(m))
 
