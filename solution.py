from utils import *


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    def naked_twins_single_unit(unit, values=values):
        # finds all naked twins in the particular unit. Eliminates unneccecary values from unit

        def remove_twins(unit, twins, values=values):
            # When the naked twin is found in some unit - eliminates twin's values from the unit
            for u in unit:
                if values[u] != twins:
                    values[u] = values[u].replace(twins[0], '').replace(twins[1], '')
            return values

        # find all naked twins
        twins = list(set([values[i] for i in unit for j in unit if ( (values[i]==values[j]) and (len(values[i])==2) and (i!=j) )]))

        for twin in twins:
            values = remove_twins(unit, twin)

        return values

    for u in unitlist:
        values = naked_twins_single_unit(u)

    return values



def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    def check_done(values):
        for b in boxes:
            if len(values[b]) > 1:
                return False
        return True

    # reduce the puzzle
    values = reduce_puzzle(values)

    if values is False:
        return False

    if check_done(values):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    min_box = ''
    min_len = 10
    for b in boxes:
        if (len(values[b]) < min_len) and (len(values[b]) > 1):
            min_len = len(values[b])
            min_box = b

    # use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in values[min_box]:
        new_values = values.copy()
        new_values[min_box] = v
        attempt = search(new_values)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
