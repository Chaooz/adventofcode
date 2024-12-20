import sys
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from math import gcd

def count_antinodes(grid):
    """
    Given a grid (list of strings) representing the map of antennas,
    return the number of unique antinode locations within the map.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Record positions of each antenna by frequency
    antenna_positions = {}
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != '.':
                if ch not in antenna_positions:
                    antenna_positions[ch] = []
                antenna_positions[ch].append((r, c))

    antinodes = set()

    # For each frequency, consider all pairs of antennas
    for freq, positions in antenna_positions.items():
        if len(positions) < 2:
            # Only one antenna of this frequency, no antinodes from this frequency
            continue

        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                dx = r2 - r1
                dy = c2 - c1
                g = gcd(dx, dy)
                # Reduced direction vector (dr, dc)
                dr = dx // g
                dc = dy // g

                # We have a line defined by (r1, c1) and direction (dr, dc).
                # We want all integer points (r1 + k*dr, c1 + k*dc) that lie within the grid.
                
                # Determine the range for k.
                # For rows: 0 <= r1 + k*dr < rows
                # For cols: 0 <= c1 + k*dc < cols
                # Solve these inequalities for k depending on the sign of dr and dc.

                def range_for_dimension(pos, step, limit):
                    # pos + k*step in [0, limit)
                    if step == 0:
                        # Then pos must be in range, otherwise no points
                        if 0 <= pos < limit:
                            # This dimension doesn't restrict k, return infinite range
                            return -float('inf'), float('inf')
                        else:
                            # No points possible
                            return 1, 0  # empty interval
                    else:
                        start = 0
                        end = limit - 1
                        # Solve inequalities:
                        # 0 <= pos + k*step < limit
                        # -pos <= k*step < limit - pos
                        # (-pos)/step <= k < (limit - pos)/step (handle sign of step)
                        low_bound = (-pos) / step
                        high_bound = (limit - pos - 1) / step if step > 0 else (limit - pos - 1) / step
                        
                        if step > 0:
                            return (low_bound, high_bound)
                        else:
                            # If step is negative, swap low and high due to direction
                            return (high_bound, low_bound)

                row_range = range_for_dimension(r1, dr, rows)
                col_range = range_for_dimension(c1, dc, cols)

                # We must take the intersection of these k-ranges
                low_k = max(row_range[0], col_range[0])
                high_k = min(row_range[1], col_range[1])

                # k must be an integer, so adjust bounds to integers
                k_start = int(-(-low_k // 1)) if low_k > 0 else int(low_k)  # ceil if low_k positive
                # Another way: use math.ceil(low_k), but to avoid import:
                from math import ceil, floor
                k_start = ceil(low_k)
                k_end = floor(high_k)

                for k in range(k_start, k_end + 1):
                    r_pos = r1 + k*dr
                    c_pos = c1 + k*dc
                    # Check bounds just in case
                    if 0 <= r_pos < rows and 0 <= c_pos < cols:
                        antinodes.add((r_pos, c_pos))

    return len(antinodes)

# Example usage with the given puzzle input:
sample_grid = loadfile('sample_input.txt')
actual_grid = loadfile('input.txt')

sample_result = count_antinodes(sample_grid)
print("Number of unique antinode locations:", sample_result)
actual_result = count_antinodes(actual_grid)
print("Number of unique antinode locations:", actual_result)
