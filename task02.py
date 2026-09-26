import time
from functools import wraps
from multiprocessing import Pool, cpu_count


def perftimer(fnc):
    @wraps(fnc)
    def wrapper(*args,**kwargs):
        t0 = time.perf_counter()
        res = fnc(*args, **kwargs)
        t1 = time.perf_counter()
        print(f'{fnc.__name__} function work hard for {t1-t0:.3f} seconds')
        return res
    return wrapper


def factorize_worker(num: int):
    return [x for x in range(1, num+1) if num%x == 0]


def factorize_mp(*number):
    with Pool(cpu_count()) as pool:
        factors = pool.map(factorize_worker,number)
        return factors
        

@perftimer
def factorize(*number):
    factors = []
    for num in number:
        factors.append ([x for x in range(1,num+1) if num%x == 0])
    return factors
    


a, b, c, d = factorize_mp(128, 255, 99999, 10651060)
# e = factorize_s(12345679)
# print(a, b, c)

# print(e)