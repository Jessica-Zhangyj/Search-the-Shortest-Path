#!/usr/bin/python3

import json
from typing import List, Optional

import graderUtil
import util
from mapUtil import (
    CityMap,
    checkValid,
    createGridMap,
    createUSTCMap,
    createHefeiMap,
    getTotalCost,
    locationFromTag,
    makeGridLabel,
    makeTag,
)

grader = graderUtil.Grader()
submission = grader.load("submission")


def extractPath(startLocation: str, search: util.SearchAlgorithm) -> List[str]:
    """
    Assumes that `solve()` has already been called on the `searchAlgorithm`.

    We extract a sequence of locations from `search.path` (see util.py to better
    understand exactly how this list gets populated).
    """
    return [startLocation] + search.actions


def printPath(
    path: List[str],
    waypointTags: List[str],
    cityMap: CityMap,
    outPath: Optional[str] = "path.json",
):
    doneWaypointTags = set()
    for location in path:
        for tag in cityMap.tags[location]:
            if tag in waypointTags:
                doneWaypointTags.add(tag)
        tagsStr = " ".join(cityMap.tags[location])
        doneTagsStr = " ".join(sorted(doneWaypointTags))
        # print(f"Location {location} tags:[{tagsStr}]; done:[{doneTagsStr}]")
    print(f"Total distance: {getTotalCost(path, cityMap)}")

    # (Optional) Write path to file, for use with `visualize.py`
    if outPath is not None:
        with open(outPath, "w") as f:
            data = {"waypointTags": waypointTags, "path": path}
            json.dump(data, f, indent=2)


# Instantiate the USTC Map as a constant --> just load once!
USTCMap = createUSTCMap()

########################################################################################
# Problem 0: Grid City

grader.add_manual_part("0a", max_points=2, description="minimum cost path")
grader.add_manual_part("0b", max_points=3, description="UCS basic behavior")
grader.add_manual_part("0c", max_points=3, description="UCS search behavior")

########################################################################################
# Problem 1a: Modeling the Shortest Path Problem.


def t_1a(
    cityMap: CityMap,
    startLocation: str,
    endTag: str,
    expectedCost: Optional[float] = None,
):
    """
    Run UCS on a ShortestPathProblem, specified by
        (startLocation, endTag).
    Check that the cost of the minimum cost path is `expectedCost`.
    """
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(submission.ShortestPathProblem(startLocation, endTag, cityMap))
    path = extractPath(startLocation, ucs)
    grader.require_is_true(checkValid(path, cityMap, startLocation, endTag, []))
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, getTotalCost(path, cityMap))



grader.add_basic_part(
    "1a-1-basic",
    lambda: t_1a(
        cityMap=createGridMap(3, 5),
        startLocation=makeGridLabel(0, 0),
        endTag=makeTag("label", makeGridLabel(2, 2)),
        expectedCost=4,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="shortest path on small grid",
)

grader.add_basic_part(
    "1a-2-basic",
    lambda: t_1a(
        cityMap=createGridMap(30, 30),
        startLocation=makeGridLabel(20, 10),
        endTag=makeTag("x", "5"),
        expectedCost=15,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="shortest path with multiple end locations",
)

grader.add_hidden_part(
    "1a-3-hidden",
    lambda: t_1a(
        cityMap=createGridMap(100, 100),
        startLocation=makeGridLabel(0, 0),
        endTag=makeTag("label", makeGridLabel(99, 99)),
    ),
    max_points=0.25,
    max_seconds=1,
    description="shortest path with larger grid",
)

# Problem 1a (continued): full USTC map...
grader.add_basic_part(
    "1a-4-basic",
    lambda: t_1a(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "the_original_north_gate"), USTCMap),
        endTag=makeTag("landmark", "middle_campus_gym"),
        expectedCost=852.2058138603107,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="basic shortest path test case (1a-4)",
)

grader.add_basic_part(
    "1a-5-basic",
    lambda: t_1a(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "3rd_teaching_building"), USTCMap),
        endTag=makeTag("landmark", "5th_teaching_building"),
        expectedCost=1752.6386148413285,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic shortest path test case (1a-5)",
)

grader.add_basic_part(
    "1a-6-basic",
    lambda: t_1a(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "also_west_lake"), USTCMap),
        endTag=makeTag("landmark", "8348"),
        expectedCost=669.8629567842597,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic shortest path test case (1a-6)",
)

grader.add_hidden_part(
    "1a-7-hidden",
    lambda: t_1a(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        endTag=makeTag("landmark", "1958"),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden shortest path test case (1a-7)",
)

grader.add_hidden_part(
    "1a-8-hidden",
    lambda: t_1a(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        endTag=makeTag("landmark", "1958"),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden shortest path test case (1a-8)",
)

########################################################################################
# Problem 1b: Custom -- Plan a Route through USTC


def t_1b_custom():
    """Given custom ShortestPathProblem, output path for visualization."""
    problem = submission.getUSTCShortestPathProblem()
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    path = extractPath(problem.startLocation, ucs)
    printPath(path=path, waypointTags=[], cityMap=USTCMap)
    grader.require_is_true(
        checkValid(path, USTCMap, problem.startLocation, problem.endTag, [])
    )


grader.add_basic_part(
    "1b-custom",
    t_1b_custom,
    max_points=1,
    max_seconds=10,
    description="customized shortest path through USTC",
)


########################################################################################
# Problem 1c: Externalities
grader.add_manual_part("1c", max_points=0, description="externalities of algorithm")


########################################################################################
# Problem 2a: Modeling the Waypoints Shortest Path Problem.


def t_2ab(
    cityMap: CityMap,
    startLocation: str,
    endTag: str,
    waypointTags: List[str],
    expectedCost: Optional[float] = None,
):
    """
    Run UCS on a WaypointsShortestPathProblem, specified by
        (startLocation, waypointTags, endTag).
    """
    ucs = util.UniformCostSearch(verbose=0)
    problem = submission.WaypointsShortestPathProblem(
        startLocation,
        waypointTags,
        endTag,
        cityMap,
    )
    ucs.solve(problem)
    grader.require_is_true(ucs.pathCost is not None)
    path = extractPath(startLocation, ucs)
    grader.require_is_true(
        checkValid(path, cityMap, startLocation, endTag, waypointTags)
    )
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, getTotalCost(path, cityMap))



grader.add_basic_part(
    "2a-1-basic",
    lambda: t_2ab(
        cityMap=createGridMap(3, 5),
        startLocation=makeGridLabel(0, 0),
        waypointTags=[makeTag("y", 4)],
        endTag=makeTag("label", makeGridLabel(2, 2)),
        expectedCost=8,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="shortest path on small grid with 1 waypoint",
)

grader.add_basic_part(
    "2a-2-basic",
    lambda: t_2ab(
        cityMap=createGridMap(30, 30),
        startLocation=makeGridLabel(20, 10),
        waypointTags=[makeTag("x", 5), makeTag("x", 7)],
        endTag=makeTag("label", makeGridLabel(3, 3)),
        expectedCost=24.0,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="shortest path on medium grid with 2 waypoints",
)

grader.add_hidden_part(
    "2a-3-hidden",
    lambda: t_2ab(
        cityMap=createGridMap(100, 100),
        startLocation=makeGridLabel(0, 0),
        waypointTags=[
            makeTag("x", 90),
            makeTag("x", 95),
            makeTag("label", makeGridLabel(3, 99)),
            makeTag("label", makeGridLabel(99, 3)),
        ],
        endTag=makeTag("y", 95),
    ),
    max_points=1,
    max_seconds=1,
    description="shortest path with 4 waypoints and multiple end locations",
)

# Problem 2a (continued): full USTC map...
grader.add_basic_part(
    "2a-4-basic",
    lambda: t_2ab(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "the_original_north_gate"), USTCMap),
        waypointTags=[makeTag("landmark", "gold_mine")],
        endTag=makeTag("landmark", "middle_campus_gym"),
        expectedCost=989.9034719672583,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="basic waypoints test case (2a-4)",
)

grader.add_basic_part(
    "2a-5-basic",
    lambda: t_2ab(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "statue_of_GuoMoruo"), USTCMap),
        waypointTags=[
            makeTag("landmark", "1958"),
            makeTag("landmark", "Ruzi_Niu"),
            makeTag("landmark", "the_original_north_gate"),
        ],
        endTag=makeTag("landmark", "5th_teaching_building"),
        expectedCost=1491.8058210940926,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="basic waypoints test case (2a-5)",
)

grader.add_basic_part(
    "2a-6-basic",
    lambda: t_2ab(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "3rd_teaching_building"), USTCMap),
        waypointTags=[
            makeTag("amenity", "library"),
            makeTag("amenity", "coffee"),
        ],
        endTag=makeTag("landmark", "2nd_teaching_building"),
        expectedCost=1691.71034788004,
    ),
    max_points=0.25,
    max_seconds=0.1,
    description="basic waypoints test case (2a-6)",
)

grader.add_hidden_part(
    "2a-7-hidden",
    lambda: t_2ab(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        waypointTags=[
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
        ],
        endTag=makeTag("landmark", "1958"),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden waypoints test case (2a-7)",
)

grader.add_hidden_part(
    "2a-8-hidden",
    lambda: t_2ab(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        waypointTags=[
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
        ],
        endTag=makeTag("landmark", "1958"),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden waypoints test case (2a-8)",
)

grader.add_hidden_part(
    "2a-9-hidden",
    lambda: t_2ab(
        cityMap=USTCMap,
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        waypointTags=[
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
        ],
        endTag=makeTag("landmark", "1958"),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden waypoints test case (2a-9)",
)

########################################################################################
# Problem 2b: Maximum states with waypoints
grader.add_manual_part("2b", max_points=2, description="max states with waypoints")


########################################################################################
# Problem 2b: Custom -- Plan a Route with Unordered Waypoints through USTC


def t_2b_custom():
    """Given custom WaypointsShortestPathProblem, output path for visualization."""
    problem = submission.getUSTCWaypointsShortestPathProblem()
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    path = extractPath(problem.startLocation, ucs)
    printPath(path=path, waypointTags=problem.waypointTags, cityMap=USTCMap)
    grader.require_is_true(
        checkValid(
            path,
            USTCMap,
            problem.startLocation,
            problem.endTag,
            problem.waypointTags,
        )
    )


grader.add_basic_part(
    "2b-custom",
    t_2b_custom,
    max_points=1,
    max_seconds=10,
    description="customized shortest path with waypoints through USTC",
)

########################################################################################
# Problem 2d: Ethical Considerations
grader.add_manual_part("2d", max_points=0, description="ethical considerations")


########################################################################################
# Problem 3a: A* to UCS reduction


# To test your reduction, we'll define an admissible (but fairly unhelpful) heuristic
class ZeroHeuristic(util.Heuristic):
    """Estimates the cost between locations as 0 distance."""
    def __init__(self, endTag: str, cityMap: CityMap):
        self.endTag = endTag
        self.cityMap = cityMap

    def evaluate(self, state: util.State) -> float:
        return 0.0


def t_3a(
    cityMap: CityMap,
    startLocation: str,
    endTag: str,
    expectedCost: Optional[float] = None,
):
    """
    Run UCS on the A* Reduction of a ShortestPathProblem, specified by
        (startLocation, endTag).
    """
    # We'll use the ZeroHeuristic to verify that the reduction works as expected
    zeroHeuristic = ZeroHeuristic(endTag, cityMap)

    # Define the baseProblem and corresponding reduction (using `zeroHeuristic`)
    baseProblem = submission.ShortestPathProblem(startLocation, endTag, cityMap)
    aStarProblem = submission.aStarReduction(baseProblem, zeroHeuristic)

    # Solve the reduction via a call to `ucs.solve` (similar to prior tests)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(aStarProblem)
    path = extractPath(startLocation, ucs)
    grader.require_is_true(checkValid(path, cityMap, startLocation, endTag, []))
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, getTotalCost(path, cityMap))



grader.add_basic_part(
    "3a-1-basic",
    lambda: t_3a(
        cityMap=createGridMap(3, 5),
        startLocation=makeGridLabel(0, 0),
        endTag=makeTag("label", makeGridLabel(2, 2)),
        expectedCost=4,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="A* shortest path on small grid",
)

grader.add_basic_part(
    "3a-2-basic",
    lambda: t_3a(
        cityMap=createGridMap(30, 30),
        startLocation=makeGridLabel(20, 10),
        endTag=makeTag("x", "5"),
        expectedCost=15,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="A* shortest path with multiple end locations",
)

grader.add_hidden_part(
    "3a-3-hidden",
    lambda: t_3a(
        cityMap=createGridMap(100, 100),
        startLocation=makeGridLabel(0, 0),
        endTag=makeTag("label", makeGridLabel(99, 99)),
    ),
    max_points=1,
    max_seconds=1,
    description="A* shortest path with larger grid",
)


########################################################################################
# Problem 3c: "straight-line" heuristic for A*


def t_3c_heuristic(
    cityMap: CityMap,
    startLocation: str,
    endTag: str,
    expectedCost: Optional[float] = None,
):
    """Targeted test for `StraightLineHeuristic` to ensure correctness."""
    heuristic = submission.StraightLineHeuristic(endTag, cityMap)
    heuristicCost = heuristic.evaluate(util.State(startLocation))
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, heuristicCost)



grader.add_basic_part(
    "3c-heuristic-1-basic",
    lambda: t_3c_heuristic(
        cityMap=createGridMap(3, 5),
        startLocation=makeGridLabel(0, 0),
        endTag=makeTag("label", makeGridLabel(2, 2)),
        expectedCost=3.145067466556296,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic straight line heuristic unit test",
)

grader.add_hidden_part(
    "3c-heuristic-2-hidden",
    lambda: t_3c_heuristic(
        cityMap=createGridMap(100, 100),
        startLocation=makeGridLabel(0, 0),
        endTag=makeTag("label", makeGridLabel(99, 99)),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden straight line heuristic unit test",
)


# Initialize a `StraightLineHeuristic` using `endTag3c` and the `USTCMap`
endTag3c = makeTag("landmark", "the_original_north_gate")
if grader.selectedPartName in [
    "3c-astar-1-basic",
    "3c-astar-2-basic",
    "3c-astar-3-hidden",
    "3c-astar-4-hidden",
    None,
]:
    USTCStraightLineHeuristic = submission.StraightLineHeuristic(
        endTag3c, USTCMap
    )


def t_3c_aStar(
    startLocation: str, heuristic: util.Heuristic, expectedCost: Optional[float] = None
):
    """Run UCS on the A* Reduction of a ShortestPathProblem, w/ `heuristic`"""
    baseProblem = submission.ShortestPathProblem(startLocation, endTag3c, USTCMap)
    aStarProblem = submission.aStarReduction(baseProblem, heuristic)

    # Solve the reduction via a call to `ucs.solve` (similar to prior tests)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(aStarProblem)
    path = extractPath(startLocation, ucs)
    grader.require_is_true(checkValid(path, USTCMap, startLocation, endTag3c, []))
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, getTotalCost(path, USTCMap))



grader.add_basic_part(
    "3c-astar-1-basic",
    lambda: t_3c_aStar(
        startLocation=locationFromTag(makeTag("landmark", "east_campus_library"), USTCMap),
        heuristic=USTCStraightLineHeuristic,
        expectedCost=584.1959167886437,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic straight line heuristic A* on USTC map (3c-astar-1)",
)


grader.add_basic_part(
    "3c-astar-2-basic",
    lambda: t_3c_aStar(
        startLocation=locationFromTag(makeTag("landmark", "1958-WEST"), USTCMap),
        heuristic=USTCStraightLineHeuristic,
        expectedCost=1456.285516098703,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic straight line heuristic A* on USTC map (3c-astar-2)",
)


grader.add_hidden_part(
    "3c-astar-3-hidden",
    lambda: t_3c_aStar(
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        heuristic=USTCStraightLineHeuristic,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden straight line heuristic A* on USTC map (3c-astar-3)",
)


grader.add_hidden_part(
    "3c-astar-4-hidden",
    lambda: t_3c_aStar(
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        heuristic=USTCStraightLineHeuristic,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden straight line heuristic A* on USTC map (3c-astar-4)",
)


########################################################################################
# Problem 3e: "no waypoints" heuristic for A*


def t_3e_heuristic(
    startLocation: str, endTag: str, expectedCost: Optional[float] = None
):
    """Targeted test for `NoWaypointsHeuristic` -- uses the full USTC map."""
    heuristic = submission.NoWaypointsHeuristic(endTag, USTCMap)
    heuristicCost = heuristic.evaluate(util.State(startLocation))
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, heuristicCost)



grader.add_basic_part(
    "3e-heuristic-1-basic",
    lambda: t_3e_heuristic(
        startLocation=locationFromTag(makeTag("landmark", "gold_mine"), USTCMap),
        endTag=makeTag("landmark", "also_west_lake"),
        expectedCost=1389.0591548910463,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic no waypoints heuristic unit test",
)

grader.add_hidden_part(
    "3e-heuristic-1-hidden",
    lambda: t_3e_heuristic(
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        endTag=makeTag("amenity", "coffee"),
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="hidden no waypoints heuristic unit test w/ multiple end locations",
)


# Initialize a `NoWaypointsHeuristic` using `endTag3e` and the `USTCMap`
endTag3e = makeTag("amenity", "coffee")
if grader.selectedPartName in [
    "3e-astar-1-basic",
    "3e-astar-2-basic",
    "3e-astar-3-hidden",
    "3e-astar-3-hidden",
    None,
]:
    USTCNoWaypointsHeuristic = submission.NoWaypointsHeuristic(
        endTag3e, USTCMap
    )


def t_3e_aStar(
    startLocation: str,
    waypointTags: List[str],
    heuristic: util.Heuristic,
    expectedCost: Optional[float] = None,
):
    """Run UCS on the A* Reduction of a WaypointsShortestPathProblem, w/ `heuristic`"""
    baseProblem = submission.WaypointsShortestPathProblem(
        startLocation, waypointTags, endTag3e, USTCMap
    )
    aStarProblem = submission.aStarReduction(baseProblem, heuristic)

    # Solve the reduction via a call to `ucs.solve` (similar to prior tests)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(aStarProblem)
    path = extractPath(startLocation, ucs)
    grader.require_is_true(
        checkValid(path, USTCMap, startLocation, endTag3e, waypointTags)
    )
    if expectedCost is not None:
        grader.require_is_equal(expectedCost, getTotalCost(path, USTCMap))



grader.add_basic_part(
    "3e-astar-1-basic",
    lambda: t_3e_aStar(
        startLocation=locationFromTag(makeTag("landmark", "8348"), USTCMap),
        waypointTags=[
            makeTag("landmark", "also_west_lake"),
            makeTag("amenity", "library"),
            makeTag("landmark", "middle_campus_gym"),
        ],
        heuristic=USTCNoWaypointsHeuristic,
        expectedCost=2243.159033199371,
    ),
    max_points=0.5,
    max_seconds=0.1,
    description="basic no waypoints heuristic A* on USTC map (3e-astar-1)",
)


grader.add_basic_part(
    "3e-astar-2-basic",
    lambda: t_3e_aStar(
        startLocation=locationFromTag(makeTag("landmark", "Ruzi_Niu"), USTCMap),
        waypointTags=[
            makeTag("amenity", "coffee"),
            makeTag("amenity", "library"),
            makeTag("landmark", "also_west_lake"),
            makeTag("landmark", "the_original_north_gate"),
            makeTag("landmark", "3rd_teaching_building"),
        ],
        heuristic=USTCNoWaypointsHeuristic,
        expectedCost=2730.5277470807923,
    ),
    max_points=0.5,
    max_seconds=0.5,
    description="basic no waypoints heuristic A* on USTC map (3e-astar-2)",
)


grader.add_hidden_part(
    "3e-astar-3-hidden",
    lambda: t_3e_aStar(
        startLocation=locationFromTag(makeTag("landmark", "1958"), USTCMap),
        waypointTags=[
            makeTag("landmark", "1958"),
            makeTag("amenity", "coffee"),
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
            makeTag("landmark", "1958"),
        ],
        heuristic=USTCNoWaypointsHeuristic,
    ),
    max_points=1,
    max_seconds=0.1,
    description="hidden no waypoints heuristic A* on USTC map (3e-astar-3)",
)

grader.add_manual_part("3d", max_points=2, description="example of n waypointTags")

########################################################################################
# Problem 3f: -- Hefei Map

# Instantiate the Hefei Map as a constant --> just load once!
if grader.selectedPartName in [
    "3f-without_Heuristic",
    "3f-with_Heuristic",
    None,
]:
    HefeiMap = createHefeiMap()

def t_3f_without_Heuristic():
    problem = submission.getHefeiShortestPathProblem(HefeiMap)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    path = extractPath(problem.startLocation, ucs)
    printPath(path=path, waypointTags=[], cityMap=HefeiMap)
    grader.require_is_true(
        checkValid(path, HefeiMap, problem.startLocation, problem.endTag, [])
    )

grader.add_basic_part(
    "3f-without_Heuristic",
    t_3f_without_Heuristic,
    max_points=1,
    max_seconds=50,
    description="shortest path through Hefei",
)

def t_3f_with_Heuristic():
    problem = submission.getHefeiShortestPathProblem_withHeuristic(HefeiMap)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    path = extractPath(problem.startLocation, ucs)
    printPath(path=path, waypointTags=[], cityMap=HefeiMap)
    grader.require_is_true(
        checkValid(path, HefeiMap, problem.startLocation, problem.endTag, [])
    )

grader.add_basic_part(
    "3f-with_Heuristic",
    t_3f_with_Heuristic,
    max_points=1,
    max_seconds=50,
    description="shortest path through Hefei",
)

if __name__ == "__main__":
    grader.grade()
