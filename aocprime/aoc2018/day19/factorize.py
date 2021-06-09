#!/usr/bin/env python3
def quick_factors(n, start=1):
    factors = []
    for i in range(start, n+1):
        if n % i == 0:
            print(n,"/", i, "=>", n//i)
            factors.append(i)
    return factors
    

print(quick_factors(973), sum(quick_factors(973)))
print(quick_factors(10551373), sum(quick_factors(10551373)))
# Answer is: 12768192
