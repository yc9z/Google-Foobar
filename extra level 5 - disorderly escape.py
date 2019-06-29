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
