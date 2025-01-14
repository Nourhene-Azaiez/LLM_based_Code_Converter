from functools import lru_cache
import random

PI_CONSTANT = 3.14159
MAX_ITER = 10

def debug(func):
    """A decorator that prints function calls"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

class Circle:
    instances_created = 0
    
    def __init__(self, radius):
        self.radius = radius
        Circle.instances_created += 1
    
    @classmethod
    def total_instances(cls):
        return cls.instances_created

# Main block demonstrating different function calls and data handling
if __name__ == "__main__":
    # Class usage
    circle = Circle(5)
    print(f"Total instances: {Circle.total_instances()}")