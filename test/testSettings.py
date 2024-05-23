import cProfile
import pstats
import unittest
from services.main import main

class TestSettings:
    profiling = False #Set to false for new test

    def wrapper(self, returnData, function, *myargs, **mykwargs):
        try:
            returnData.append(function(*myargs, **mykwargs))
        except TypeError:
            print('bad args passed to func.')

    
    def profile_main(self, function, params):
        # Profile the 'main' function
        returnData = []
        cProfile.runctx(f"self.wrapper(returnData, {function.__name__}, {params})", globals(), locals(), "profile_stats.prof")
        
        returnValue = returnData[0]
        # Load and print the profiling statistics
        stats = pstats.Stats("profile_stats.prof")
        stats.sort_stats("cumulative").print_stats(30)

        # Call main again to get the Alert object for further testing
        return returnValue
