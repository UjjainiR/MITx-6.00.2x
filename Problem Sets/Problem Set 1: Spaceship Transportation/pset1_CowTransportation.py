###########################
# 6.00.2x Problem Set 1: Space Cows

from pset1_partition_HELPER import get_partitions
import time
import collections

# ================================
# Part A: Transporting Space Cows
# ================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    shortest_trip = []
    cows_copy = cows.copy()
    sorted_cows = collections.OrderedDict(sorted(cows.items(), key=lambda k_v: k_v[1], reverse=True))   # Sorting cows in descending order of weight
    while cows_copy:
        current_trip = []
        current_weight = 0
        for cow in sorted_cows:
            if cow in cows_copy and (current_weight + sorted_cows[cow]) <= limit:
                current_trip.append(cow)
                current_weight += sorted_cows[cow]
                cows_copy.pop(cow)
        shortest_trip.append(current_trip)
    return shortest_trip


# Problem 2
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    shortest_trip, shortest_length = None, len(cows) + 1
    for current_trip in get_partitions(cows):
        if len(current_trip) > shortest_length:
            continue
        valid_trip = True
        for sub_trip in current_trip:
            sub_weight = sum(cows[cow] for cow in sub_trip)
            if sub_weight > limit:
                valid_trip = False
                break
        if valid_trip:
            shortest_trip = current_trip
            shortest_length = len(current_trip)
    return shortest_trip


# Problem 3
def compare_cow_transport_algorithms(cows, limit=10):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    print("The weight limit of the ship is:", limit,"\n")
  
    greedy_start = time.time()
    greedy_result = greedy_cow_transport(cows, limit)
    greedy_end = time.time()
    greedy_time = greedy_end - greedy_start
    print("The result of greedy algorithm is:\n", greedy_result)
    print("The number of trips obtained by greedy algorithm is:", len(greedy_result))
    print("The time taken by greedy algorithm is:", greedy_time, "\n")

    brute_force_start = time.time()
    brute_force_result = brute_force_cow_transport(cows, limit)
    brute_force_end = time.time()
    brute_force_time = brute_force_end - brute_force_start
    print("The result of brute force algorithm is:\n", brute_force_result)
    print("The number of trips obtained by brute force algorithm is:", len(brute_force_result))
    print("The time taken by brute force algorithm is:", brute_force_time, "\n")
