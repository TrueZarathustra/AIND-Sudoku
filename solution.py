assignments = []


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
main_diagonal_unit = [r+c for r, c in zip(rows, cols)]
second_diagonal_unit = [r+c for r, c in zip(reversed(rows), cols)]
diagonales = [main_diagonal_unit, second_diagonal_unit]
unitlist = row_units + column_units + square_units + diagonales
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


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


'''
print(unitlist)
print()
print(units)

[['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
'B8', 'B9'], ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['D1', 'D2', 'D3', 'D4', 'D5',
'D6', 'D7', 'D8', 'D9'], ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['F1', 'F2', 'F3',
'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['H1',
'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I
9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G
2', 'H2', 'I2'], ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['A4', 'B4', 'C4', 'D4', 'E
4', 'F4', 'G4', 'H4', 'I4'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['A6', 'B6', 'C
6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'], ['A
8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9'
, 'I9'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6'
, 'C4', 'C5', 'C6'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'], ['D1', 'D2', 'D3', 'E1'
, 'E2', 'E3', 'F1', 'F2', 'F3'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['D7', 'D8'
, 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'], ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'],
 ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7',
'I8', 'I9'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['I1', 'H2', 'G3', 'F4', 'E5',
'D6', 'C7', 'B8', 'A9']]

{'A1': [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1',
 'G1', 'H1', 'I1'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A1', 'B2', 'C3', 'D4',
 'E5', 'F6', 'G7', 'H8', 'I9']], 'A2': [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A2
', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2',
 'C3']], 'A3': [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A3', 'B3', 'C3', 'D3', 'E3
', 'F3', 'G3', 'H3', 'I3'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']], 'A4': [['A1', '
A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4
'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']], 'A5': [['A1', 'A2', 'A3', 'A4', 'A5', '
A6', 'A7', 'A8', 'A9'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['A4', 'A5', 'A6', '
B4', 'B5', 'B6', 'C4', 'C5', 'C6']], 'A6': [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', '
C5', 'C6']], 'A7': [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A7', 'B7', 'C7', 'D7',
 'E7', 'F7', 'G7', 'H7', 'I7'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']], 'A8': [['A1
', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8',
 'I8'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']], 'A9': [['A1', 'A2', 'A3', 'A4', 'A5
', 'A6', 'A7', 'A8', 'A9'], ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9'], ['A7', 'A8', 'A9
', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'B1
': [['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1
', 'H1', 'I1'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']], 'B2': [['B1', 'B2', 'B3', '
B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['A1', '
A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9
']], 'B3': [['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A3', 'B3', 'C3', 'D3', 'E3', '
F3', 'G3', 'H3', 'I3'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']], 'B4': [['B1', 'B2',
 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'],
['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']], 'B5': [['B1', 'B2', 'B3', 'B4', 'B5', 'B6',
 'B7', 'B8', 'B9'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['A4', 'A5', 'A6', 'B4',
 'B5', 'B6', 'C4', 'C5', 'C6']], 'B6': [['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A6
', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5',
 'C6']], 'B7': [['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A7', 'B7', 'C7', 'D7', 'E7
', 'F7', 'G7', 'H7', 'I7'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']], 'B8': [['B1', '
B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8
'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7
', 'B8', 'A9']], 'B9': [['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['A9', 'B9', 'C9', '
D9', 'E9', 'F9', 'G9', 'H9', 'I9'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']], 'C1': [
['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', '
H1', 'I1'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']], 'C2': [['C1', 'C2', 'C3', 'C4',
 'C5', 'C6', 'C7', 'C8', 'C9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['A1', 'A2',
 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']], 'C3': [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
 'C9'], ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3',
 'C1', 'C2', 'C3'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']], 'C4': [['C1', 'C2', 'C3
', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'], ['A4
', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']], 'C5': [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7
', 'C8', 'C9'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['A4', 'A5', 'A6', 'B4', 'B5
', 'B6', 'C4', 'C5', 'C6']], 'C6': [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A6', '
B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6
']], 'C7': [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A7', 'B7', 'C7', 'D7', 'E7', '
F7', 'G7', 'H7', 'I7'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'], ['I1', 'H2', 'G3', '
F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'C8': [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', '
C8', 'C9']], 'C9': [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A9', 'B9', 'C9', 'D9',
 'E9', 'F9', 'G9', 'H9', 'I9'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']], 'D1': [['D1
', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
 'I1'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']], 'D2': [['D1', 'D2', 'D3', 'D4', 'D5
', 'D6', 'D7', 'D8', 'D9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['D1', 'D2', 'D3
', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']], 'D3': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9
'], ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1
', 'F2', 'F3']], 'D4': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'], ['A4', 'B4', 'C4', '
D4', 'E4', 'F4', 'G4', 'H4', 'I4'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['A1', '
B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']], 'D5': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', '
D8', 'D9'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['D4', 'D5', 'D6', 'E4', 'E5', '
E6', 'F4', 'F5', 'F6']], 'D6': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'], ['A6', 'B6',
 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'],
['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'D7': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6',
 'D7', 'D8', 'D9'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'], ['D7', 'D8', 'D9', 'E7',
 'E8', 'E9', 'F7', 'F8', 'F9']], 'D8': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'], ['A8
', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8',
 'F9']], 'D9': [['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'], ['A9', 'B9', 'C9', 'D9', 'E9
', 'F9', 'G9', 'H9', 'I9'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']], 'E1': [['E1', '
E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1
'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']], 'E2': [['E1', 'E2', 'E3', 'E4', 'E5', '
E6', 'E7', 'E8', 'E9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['D1', 'D2', 'D3', '
E1', 'E2', 'E3', 'F1', 'F2', 'F3']], 'E3': [['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'],
['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', '
F2', 'F3']], 'E4': [['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A4', 'B4', 'C4', 'D4',
 'E4', 'F4', 'G4', 'H4', 'I4'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']], 'E5': [['E1
', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
 'I5'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6',
 'G7', 'H8', 'I9'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'E6': [['E1', 'E2', 'E3
', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['D4
', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']], 'E7': [['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7
', 'E8', 'E9'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'], ['D7', 'D8', 'D9', 'E7', 'E8
', 'E9', 'F7', 'F8', 'F9']], 'E8': [['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A8', '
B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9
']], 'E9': [['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A9', 'B9', 'C9', 'D9', 'E9', '
F9', 'G9', 'H9', 'I9'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']], 'F1': [['F1', 'F2',
 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],
['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']], 'F2': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6',
 'F7', 'F8', 'F9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['D1', 'D2', 'D3', 'E1',
 'E2', 'E3', 'F1', 'F2', 'F3']], 'F3': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['A3
', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2',
 'F3']], 'F4': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['A4', 'B4', 'C4', 'D4', 'E4
', 'F4', 'G4', 'H4', 'I4'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['I1', 'H2', 'G3
', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'F5': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9
'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4
', 'F5', 'F6']], 'F6': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['A6', 'B6', 'C6', '
D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['A1', '
B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']], 'F7': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', '
F8', 'F9'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'], ['D7', 'D8', 'D9', 'E7', 'E8', '
E9', 'F7', 'F8', 'F9']], 'F8': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['A8', 'B8',
 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']],
 'F9': [['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['A9', 'B9', 'C9', 'D9', 'E9', 'F9',
 'G9', 'H9', 'I9'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']], 'G1': [['G1', 'G2', 'G3
', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['G1
', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']], 'G2': [['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7
', 'G8', 'G9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['G1', 'G2', 'G3', 'H1', 'H2
', 'H3', 'I1', 'I2', 'I3']], 'G3': [['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['A3', '
B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3
'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'G4': [['G1', 'G2', 'G3', 'G4', 'G5', '
G6', 'G7', 'G8', 'G9'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'], ['G4', 'G5', 'G6', '
H4', 'H5', 'H6', 'I4', 'I5', 'I6']], 'G5': [['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],
['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', '
I5', 'I6']], 'G6': [['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['A6', 'B6', 'C6', 'D6',
 'E6', 'F6', 'G6', 'H6', 'I6'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']], 'G7': [['G1
', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
 'I7'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6',
 'G7', 'H8', 'I9']], 'G8': [['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['A8', 'B8', 'C8
', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']], 'G9
': [['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9
', 'H9', 'I9'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']], 'H1': [['H1', 'H2', 'H3', '
H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['G1', '
G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']], 'H2': [['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', '
H8', 'H9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['G1', 'G2', 'G3', 'H1', 'H2', '
H3', 'I1', 'I2', 'I3'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']], 'H3': [['H1', 'H2',
 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'],
['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']], 'H4': [['H1', 'H2', 'H3', 'H4', 'H5', 'H6',
 'H7', 'H8', 'H9'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'], ['G4', 'G5', 'G6', 'H4',
 'H5', 'H6', 'I4', 'I5', 'I6']], 'H5': [['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['A5
', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5',
 'I6']], 'H6': [['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['A6', 'B6', 'C6', 'D6', 'E6
', 'F6', 'G6', 'H6', 'I6'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']], 'H7': [['H1', '
H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7
'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']], 'H8': [['H1', 'H2', 'H3', 'H4', 'H5', '
H6', 'H7', 'H8', 'H9'], ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['G7', 'G8', 'G9', '
H7', 'H8', 'H9', 'I7', 'I8', 'I9'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']], 'H9': [
['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', '
H9', 'I9'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']], 'I1': [['I1', 'I2', 'I3', 'I4',
 'I5', 'I6', 'I7', 'I8', 'I9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['G1', 'G2',
 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']],
 'I2': [['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2',
 'G2', 'H2', 'I2'], ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']], 'I3': [['I1', 'I2', 'I3
', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['G1
', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']], 'I4': [['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7
', 'I8', 'I9'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'], ['G4', 'G5', 'G6', 'H4', 'H5
', 'H6', 'I4', 'I5', 'I6']], 'I5': [['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A5', '
B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6
']], 'I6': [['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A6', 'B6', 'C6', 'D6', 'E6', '
F6', 'G6', 'H6', 'I6'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']], 'I7': [['I1', 'I2',
 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'],
['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']], 'I8': [['I1', 'I2', 'I3', 'I4', 'I5', 'I6',
 'I7', 'I8', 'I9'], ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['G7', 'G8', 'G9', 'H7',
 'H8', 'H9', 'I7', 'I8', 'I9']], 'I9': [['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A9
', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8',
 'I9'], ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]}
'''