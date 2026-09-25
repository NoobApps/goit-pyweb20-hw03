import time
from functools import wraps

def timer(fnc):
    @wraps(fnc)
    def wrapper(*args,**kwargs):
        t0 = time.perf_counter()
        res = fnc(*args, **kwargs)
        t1 = time.perf_counter()
        print(t1-t0)
        return res
    return wrapper

@timer
def factorize(*number):
    factors = []
    for num in number:
        factors.append ([x for x in range(1,num+1) if num%x == 0])
    return factors
    


a, b, c, d = factorize(128, 255, 99999, 10651060)

print(a, b, c)