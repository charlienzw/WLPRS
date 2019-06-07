def paths2Instrs(paths, item_ids):
    '''Get the user friendly instruction from a path list'''
    # Dictionary indicating where to turn
    direct2turn = {('North', 'East'): 'Right', ('North', 'South'): 'Back', ('North', 'West'): 'Left',
                   ('East', 'North'): 'Left', ('East', 'South'): 'Right', ('East', 'West'): 'Back',
                   ('South', 'North'): 'Back', ('South', 'East'): 'Left', ('South', 'West'): 'Right',
                   ('West', 'North'): 'Right', ('West', 'East'): 'Back', ('West', 'South'): 'Left'}
    # Each path has a bunch on coordinates. Starts with the first coordinate.
    coord = paths[0][0]  # Start point
    next_coord = paths[0][1]
    direction = 'North'
    direction = getDirection(coord, next_coord, direction)
    print("Start at {}".format(coord))
    step_count = 0
    for idx, path in enumerate(paths):
        if len(path) == 1:
            print("Pick Up Item: {} at {}".format(item_ids[idx], next_coord))
            continue
        for i, coord in enumerate(path[:-1]):
            next_coord = path[i+1]
            next_direct = getDirection(coord, next_coord, direction)
            if direction == next_direct:
                step_count += 1
                continue
            else:
                turn_direct = direct2turn[(direction, next_direct)]
                print('Move Towards {}, For {} Steps, Until '.format(direction, step_count) +
                      'You Reach Point {} and Turn {} to {} Direction.'.format(coord, turn_direct, next_direct))
                step_count = 1  # Reset step count
                direction = next_direct
        if idx == len(paths) - 1:
            print("Move Towards {}, For {} Steps and End Your Tour at {}".format(direction, step_count, next_coord))
        else:
            print("Move Towards {}, For {} Steps, and Pick Up Item: {} at {}".format(direction, step_count, item_ids[idx], next_coord))
            step_count = 0


def getDirection(first_pt, next_pt, direction):
    if first_pt == next_pt:
        return direction
    is_north = next_pt == (first_pt[0], first_pt[1] + 1)
    is_east = next_pt == (first_pt[0] + 1, first_pt[1])
    is_south = next_pt == (first_pt[0], first_pt[1] - 1)
    is_west = next_pt == (first_pt[0] - 1, first_pt[1])
    if is_north:
        return 'North'
    elif is_east:
        return 'East'
    elif is_south:
        return 'South'
    elif is_west:
        return 'West'
    else:
        raise ValueError("The Given Two Points Are NOT One Step From One Another!!")


def generatePaths(num):
    start_pt = (0, 0)
    prev_ran = 0
    paths = []
    for i in range(num):
        path = [start_pt]
        path_len = random.randint(1, 15)
        for j in range(path_len):
            ran = random.randint(1, 100)
            if ran < 75:
                ran = prev_ran
            else:
                prev_ran = ran
            if ran % 4 == 0:
                rand_step = (start_pt[0], start_pt[1] + 1)
            elif ran % 4 == 1:
                rand_step = (start_pt[0] + 1, start_pt[1])
            elif ran % 4 == 2:
                rand_step = (start_pt[0], start_pt[1] - 1)
            else:
                rand_step = (start_pt[0] - 1, start_pt[1])
            path.append(rand_step)
            start_pt = rand_step
        paths.append(path)
    return paths


def generateIDs(num):
    item_ids = []
    for i in range(num):
        item_ids.append(random.randint(1, 1000))
    return item_ids


def main():
    num = 5
    paths = generatePaths(num)
    paths = paths[:3] + [[paths[3][0]]] + paths[3:]
    item_ids = generateIDs(num)
    for x in paths:
        print(x)
    print(item_ids)
    paths2Instrs(paths, item_ids)


if __name__ == '__main__':
    main()
