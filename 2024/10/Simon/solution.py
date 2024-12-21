import sys
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from collections import deque

def read_map():
    """
    Replace this function with your actual puzzle input reading logic.
    For example, you might read lines from a file or stdin.
    Return a list of strings or a list of list-of-ints.
    """
    lines = loadfile("input.txt")
    grid = [list(map(int, list(line.strip()))) for line in lines]
    return grid

def neighbors(r, c, rows, cols):
    """Yield valid 4-direction neighbors."""
    for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_reachable_nines(grid, start_r, start_c):
    """
    From the trailhead at (start_r, start_c), find all distinct positions
    of height=9 reachable by taking steps that increment height by exactly 1 each time.
    Return a set of reachable 9-positions (row,col).
    """
    rows, cols = len(grid), len(grid[0])
    start_height = grid[start_r][start_c]
    assert start_height == 0, "Trailhead must be height 0."

    # We'll do a BFS that only moves from height h to h+1
    visited = set()
    queue = deque()
    queue.append((start_r, start_c, 0))  # (row, col, current_height=0)
    visited.add((start_r, start_c, 0))

    reachable_nines = set()

    while queue:
        r, c, h = queue.popleft()
        # If we are on a position with height 9, record it
        if h == 9:
            reachable_nines.add((r, c))
            # No reason to continue from a 9, because you can't go to height 10
            continue

        # Explore valid neighbors (height must be h+1)
        for nr, nc in neighbors(r, c, rows, cols):
            if grid[nr][nc] == h + 1:
                # If not visited with that next height
                if (nr, nc, h+1) not in visited:
                    visited.add((nr, nc, h+1))
                    queue.append((nr, nc, h+1))

    return reachable_nines

def solve():
    # 1) Read the map
    grid = read_map()
    rows, cols = len(grid), len(grid[0])

    # 2) Find all trailheads (positions with height=0)
    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    # 3) For each trailhead, find how many distinct 9s are reachable
    total_score = 0
    for (r, c) in trailheads:
        reachable_nines = find_reachable_nines(grid, r, c)
        score = len(reachable_nines)
        total_score += score

    # 4) Print or return the final answer
    print("Sum of the scores of all trailheads:", total_score)

if __name__ == "__main__":
    solve()
