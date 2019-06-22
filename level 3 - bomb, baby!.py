"""
    Prepare the Bunnies' Escape
    ===========================
    
    You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny prisoners, but once they're free of the prison blocks, the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions.
    
    You have maps of parts of the space station, each starting at a prison exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the prison is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1).
    
    Write a function solution(map) that generates the length of the shortest path from the prison door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.
    
    Languages
    =========
    
    To provide a Python solution, edit solution.py
    To provide a Java solution, edit Solution.java
    
    Test cases
    ==========
    Your code should pass the following test cases.
    Note that it may also be run against hidden test cases not shown here.
    
    -- Python cases --
    Input:
    solution.solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])
    Output:
    7
    
    Input:
    solution.solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
    Output:
    11
    
    -- Java cases --
    Input:
    Solution.solution({{0, 1, 1, 0}, {0, 0, 0, 1}, {1, 1, 0, 0}, {1, 1, 1, 0}})
    Output:
    7
    
    Input:
    Solution.solution({{0, 0, 0, 0, 0, 0}, {1, 1, 1, 1, 1, 0}, {0, 0, 0, 0, 0, 0}, {0, 1, 1, 1, 1, 1}, {0, 1, 1, 1, 1, 1}, {0, 0, 0, 0, 0, 0}})
    Output:
    11
"""
def solution(x, y):
    cycle = '0'
    
    def str_add(s1,s2):
        carry = 0
        l = max(len(s1),len(s2))
        s1 = '0'*(l-len(s1))+s1
        s2 = '0'*(l-len(s2))+s2
        
        ans = ''
        
        for i in range(l-1,-1,-1):
            ans = str((int(s1[i])+int(s2[i])+carry)%10)+ans
            carry = (int(s1[i])+int(s2[i])+carry)//10
            
        if carry == 1:
            ans = '1' + ans
        
        return ans
        
    def str_minus(s1,s2):
        carry = 0
        l = len(s1)
        s2 = '0'*(l-len(s2))+s2
        s = ''
        
        for i in range(l-1,-1,-1):
            if int(s1[i])+carry>=int(s2[i]):
                s = str(int(s1[i])+carry-int(s2[i])) + s
                carry = 0
            else:
                s = str(10+int(s1[i])+carry-int(s2[i])) + s
                carry = -1

        ans = s.lstrip('0')
        
        return ans if ans else '0'
                
    
    def str_divide(s1,s2):
        s = ''
        l1, l2 = len(s1), len(s2)
        res = s1[:l2-1]
        i = l2-1
        ratio = ''
        
        while i<l1:
            while i<l1 and not str_leq(s2,res):
                res += s1[i]
                i += 1
                ratio += '0'
                
            last = 0
            while str_leq(s2,res):
                if i == l1 and res == '1':
                    ratio = ratio[:-1]+str(last)
                    return res, s2, ratio
                res = str_minus(res,s2)
                last += 1
                
            ratio = (ratio[:-1]+str(last)).lstrip('0')
            ratio = ratio if ratio else '0'
            
        return res,s2, ratio
    
    def str_leq(s1,s2):
        if len(s1)<len(s2): return True
        if len(s1)>len(s2): return False
        return s1<=s2
        
    def str_order(s1,s2):
        if str_leq(s1,s2): return s1, s2
        else: return s2, s1
        
    x,y = str_order(x,y)
    
    while str_leq('2',x) or str_leq('2',y) and x!='0' and y!='0':
        x,y,ratio = str_divide(y,x)
        cycle = str_add(cycle,ratio)
        
    return cycle if x==y=='1' else "impossible"
    
 
        
    

x,y = '405134234234231112324123423','734234234'
print(solution(x,y))
