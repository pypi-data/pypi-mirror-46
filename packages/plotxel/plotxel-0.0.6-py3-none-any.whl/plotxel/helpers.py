from math import log, floor

def smart_limits(data):
    rounding_factor = .4
    head_room = .3
    true_max = max(abs(min(data)), abs(max(data)))
    num_zeros = log(rounding_factor * true_max, 10)
    limits = [0, 0]
    if max(data) == 0:
        limits[1] = 0
    else:
        limits[1] = round(max(data) + head_room * true_max, floor(num_zeros) * (-1))
    if limits[1] > 0 and max(data) < 0:
        limits[1] = 0
    if min(data) == 0:
        limits[0] = 0
    else:
        limits[0] = round(min(data) - head_room * true_max, floor(num_zeros) * (-1))
    if limits[0] < 0 and min(data) > 0:
        limits[0] = 0
    return limits


def smart_ticks(data, limits=None):
    print(data)
    print(limits)
    if limits is None:
        limits = smart_limits(data)
    print(data)
    print(limits)
    # print('Limits are: %s'%limits)
    # Ticks should only be in divisers of 1, 2, 2.5 or 5 and any 10x multiple of those, e.g. 10, 20, 25
    # We will start with ~ 5 ticks, but later adjust for axis size. We will also move this function to be an axis
    # class function

    # first, determine how many orders of magnitude our data spans
    magnitudes = floor(log(limits[1]-limits[0], 10))

    # next divide our limits by that
    div_limits = [limit/(10**magnitudes) for limit in limits]

    # manual, verbose checking potential limits to see how many ticks we would get
    potential_ticks = [.1, .2, .25, .5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100]
    num_ticks = [floor((div_limits[1]-div_limits[0])/pt) for pt in potential_ticks]


    for i, num_tick in enumerate(num_ticks):
        # even though it says 3 to 5 allowed ticks, it could actually be actually 4 to 8
        if (num_tick >= 4) & (num_tick <= 6):
            tick = potential_ticks[i]
            break

    # print("Tick value: %s %s times"%(tick*10**magnitudes, num_tick))
    # next, find the minimum tick value that matches out convention of allowable tick numbers
    tick = tick*10**magnitudes

    # check if our limit falls directly on the first tick. This would give a float rounding error
    # if the difference between the tick and modulo is 3 orders of magnitude smaller than we expect, it's a rounding error

    if log(tick - limits[0] % tick, 10) < (magnitudes-3):
        first_tick = limits[0]

    else:
        first_tick = limits[0] - limits[0] % tick
    if first_tick < limits[0]:

        first_tick += tick

    #print('first tick is as such: ', limits, first_tick)
    #propogate our ticks from there
    ticks = [first_tick]
    max_tick = first_tick

    while True:
        max_tick += tick
        #print(max_tick, limits[1])
        if max_tick > limits[1]:
            break
        else:
            ticks.append(max_tick)
    #print(ticks)
    return ticks