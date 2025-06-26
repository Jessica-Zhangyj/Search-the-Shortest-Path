from typing import List, Tuple

from mapUtil import (
    CityMap,
    computeDistance,
    createUSTCMap,
    createHefeiMap,
    locationFromTag,
    makeTag,
)
from util import Heuristic, SearchProblem, State, UniformCostSearch

# BEGIN_YOUR_CODE (You may add some codes here to assist your coding below if you want, but don't worry if you deviate from this.)



# END_YOUR_CODE

# *IMPORTANT* :: A key part of this assignment is figuring out how to model states
# effectively. We've defined a class `State` to help you think through this, with a
# field called `memory`.
#
# As you implement the different types of search problems below, think about what
# `memory` should contain to enable efficient search!
#   > Check out the docstring for `State` in `util.py` for more details and code.

########################################################################################
# Problem 1a: Modeling the Shortest Path Problem.


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `startLocation` to any location with the specified `endTag`.
    """

    def __init__(self, startLocation: str, endTag: str, cityMap: CityMap):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap
        
        

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return State(location=self.startLocation)
        raise NotImplementedError("Override me")
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this) 
        return self.endTag in self.cityMap.tags.get(state.location, set())
        raise NotImplementedError("Override me")
        # END_YOUR_CODE

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
        # The successors of a state are all the locations that can be reached from  
        neighbors = self.cityMap.distances.get(state.location, {})
        return [
            (neighbor, State(neighbor), distance)
            for neighbor, distance in neighbors.items()
        ] 
        raise NotImplementedError("Override me")
        # END_YOUR_CODE


########################################################################################
# Problem 1b: Custom -- Plan a Route through USTC


def getUSTCShortestPathProblem() -> ShortestPathProblem:
    """
    Create your own search problem using the map of USTC, specifying your own
    `startLocation`/`endTag`.

    Run `python mapUtil.py > readableUSTCMap.txt` to dump a file with a list of
    locations and associated tags; you might find it useful to search for the following
    tag keys (amongst others):
        - `landmark=` - Hand-defined landmarks (from `data/USTC-landmarks.json`)
        - `amenity=`  - Various amenity types (e.g., "coffee", "food")
    """
    cityMap = createUSTCMap()

    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    startLocation=locationFromTag(makeTag("landmark", "1958"), cityMap)
    endTag=makeTag("landmark", "1958-WEST")
    # END_YOUR_CODE
    return ShortestPathProblem(startLocation, endTag, cityMap)


########################################################################################
# Problem 2a: Modeling the Waypoints Shortest Path Problem.


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `startLocation` to any location with the specified `endTag` such that the path also
    traverses locations that cover the set of tags in `waypointTags`.

    Think carefully about what `memory` representation your States should have!
    """
    def __init__(
        self, startLocation: str, waypointTags: List[str], endTag: str, cityMap: CityMap
    ):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

        # We want waypointTags to be consistent/canonical (sorted) and hashable (tuple)
        self.waypointTags = tuple(sorted(waypointTags))

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return State(location=self.startLocation, memory=0)
        raise NotImplementedError("Override me")
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 1 lines of code, but don't worry if you deviate from this)
    
        return(
            self.endTag in self.cityMap.tags.get(state.location,set()) and
            state.memory == (1<<len(self.waypointTags))-1
        )
        raise NotImplementedError("Override me")
        # END_YOUR_CODE

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 13 lines of code, but don't worry if you deviate from this)
        successors = []
            
        for neighbor, distance in self.cityMap.distances.get(state.location,{}).items():
            newMemory = state.memory
            for i, tag in enumerate(self.waypointTags):
                if tag in self.cityMap.tags.get(neighbor, set()):
                    newMemory |= (1 << i)
            successors.append(
                (neighbor, State(neighbor,newMemory), distance)
            )
        return successors

        raise NotImplementedError("Override me")
        # END_YOUR_CODE


########################################################################################
# Problem 2b: Custom -- Plan a Route with Unordered Waypoints through USTC


def getUSTCWaypointsShortestPathProblem() -> WaypointsShortestPathProblem:
    """
    Create your own search problem using the map of USTC, specifying your own
    `startLocation`/`waypointTags`/`endTag`.

    Similar to Problem 1b, use `readableUSTCMap.txt` to identify potential
    locations and tags.
    """
    cityMap = createUSTCMap()
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    startLocation=locationFromTag(makeTag("landmark", "1958"), cityMap)
    endTag=makeTag("landmark", "1958-WEST")
    waypointTags=[makeTag("label",locationFromTag(makeTag("landmark","middle_campus_gym"),cityMap)), makeTag("label",locationFromTag(makeTag("landmark","also_west_lake"),cityMap))]
    
    #raise NotImplementedError("Override me")
    # END_YOUR_CODE
    return WaypointsShortestPathProblem(startLocation, waypointTags, endTag, cityMap)


########################################################################################
# Problem 3a: A* to UCS reduction

# Turn an existing SearchProblem (`problem`) you are trying to solve with a
# Heuristic (`heuristic`) into a new SearchProblem (`newSearchProblem`), such
# that running uniform cost search on `newSearchProblem` is equivalent to
# running A* on `problem` subject to `heuristic`.
#
# This process of translating a model of a problem + extra constraints into a
# new instance of the same problem is called a reduction; it's a powerful tool
# for writing down "new" models in a language we're already familiar with.


def aStarReduction(problem: SearchProblem, heuristic: Heuristic) -> SearchProblem:
    class NewSearchProblem(SearchProblem):
        def __init__(self):
            # BEGIN_YOUR_CODE (our solution is 3 line of code, but don't worry if you deviate from this)
            self.problem = problem
            self.heuristic = heuristic
            #raise NotImplementedError("Override me")
            self.startLocation=self.problem.startState().location
            self.endTag=self.problem.endTag
            self.cityMap=self.problem.cityMap
            # END_YOUR_CODE

        def startState(self) -> State:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return self.problem.startState()
            raise NotImplementedError("Override me")
            # END_YOUR_CODE

        def isEnd(self, state: State) -> bool:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return self.problem.isEnd(state)
            raise NotImplementedError("Override me")
            # END_YOUR_CODE

        def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
            # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
            successors = self.problem.successorsAndCosts(state)
            newSuccessors = []
            h_current=self.heuristic.evaluate(state)
            for action, newState, cost in successors:
                #修改代价
                h_new=self.heuristic.evaluate(newState)
                newCost=cost+h_new - h_current
                newSuccessors.append((action, newState, newCost))
                
            return newSuccessors
            raise NotImplementedError("Override me")
            # END_YOUR_CODE

    return NewSearchProblem()


########################################################################################
# Problem 3c: "straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
        > Hint: you might consider using `computeDistance` defined in `mapUtil.py`
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        self.endTag = endTag
        self.cityMap = cityMap

        # Precompute
        # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
        '''end_label=locationFromTag(self.endTag, self.cityMap)
        self.end_location = self.cityMap.geoLocations[end_label]'''
        self.end_locations=[
            location for location,tags in self.cityMap.tags.items()
            if endTag in tags and location in self.cityMap.geoLocations
        ]
        if not self.end_locations:
            raise ValueError(f"No locations found for tag: {self.endTag}")
        self.end_geolocations = [self.cityMap.geoLocations[location] for location in self.end_locations]
        #raise NotImplementedError("Override me")
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        current_geolocation = self.cityMap.geoLocations[state.location]
        # 判断当前位置是否在地图上  
        if current_geolocation is None or self.end_geolocations is None:
            return float("inf") 
        return min(
            computeDistance(current_geolocation, end_geolocation) for end_geolocation in self.end_geolocations
        )
        raise NotImplementedError("Override me")
        # END_YOUR_CODE


########################################################################################
# Problem 3e: "no waypoints" heuristic for A*



class NoWaypointsHeuristic(Heuristic):
    """
    Returns the minimum distance from `startLocation` to any location with `endTag`,
    ignoring all waypoints.
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        # Precompute
        # BEGIN_YOUR_CODE (our solution is 14 lines of code, but don't worry if you deviate from this)
        self.endTag = endTag
        self.cityMap = cityMap
        
        self.end_locations=[
            location for location, tags in self.cityMap.tags.items()
            if self.endTag in tags and location in self.cityMap.geoLocations
        ]
        
        if not self.end_locations:
            raise ValueError(f"No locations found for tag: {self.endTag}")
    
        
        #initialize search algorithm and distance cache
        self.ucs=UniformCostSearch(verbose=0)
        self.distance_cache={}
        
        self.all_distances={}
        for end_location in self.end_locations:
            problem=ShortestPathProblem(end_location, None , self.cityMap)
            self.ucs.solve(problem)
            
            for loc_state, cost in self.ucs.pastCosts.items():
                if loc_state.location not in self.all_distances or cost<self.all_distances[loc_state.location]:
                    self.all_distances[loc_state.location] = cost
               
        
        #raise NotImplementedError("Override me")
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)

        return self.all_distances.get(state.location, float('inf')) 
        
        raise NotImplementedError("Override me")
        # END_YOUR_CODE


########################################################################################
# Problem 3f: Plan a Route through Hefei with or without a Heuristic

def getHefeiShortestPathProblem(cityMap: CityMap) -> ShortestPathProblem:
    """
    Create a search problem using the map of Hefei
    """
    startLocation=locationFromTag(makeTag("landmark", "USTC"), cityMap)
    endTag=makeTag("landmark", "Chaohu")
    # BEGIN_YOUR_CODE (our solution is 1 lines of code, but don't worry if you deviate from this)
    return ShortestPathProblem(startLocation, endTag, cityMap)
    raise NotImplementedError("Override me")
    # END_YOUR_CODE

def getHefeiShortestPathProblem_withHeuristic(cityMap: CityMap) -> ShortestPathProblem:
    """
    Create a search problem with Heuristic using the map of Hefei
    """
    startLocation=locationFromTag(makeTag("landmark", "USTC"), cityMap)
    endTag=makeTag("landmark", "Chaohu")
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    endTag=makeTag("label",locationFromTag(endTag, cityMap))
    return aStarReduction(
        ShortestPathProblem(startLocation, endTag, cityMap),
        NoWaypointsHeuristic(endTag, cityMap)
    )
    raise NotImplementedError("Override me")
    # END_YOUR_CODE
