import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        execution_time = end - start
        print(f"{func.__name__} took {execution_time:.2f} seconds")

        return result, execution_time
    return wrapper