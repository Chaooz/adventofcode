import sys
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from collections import defaultdict

def read_map():
    """
    Replace with code reading your *actual* puzzle input.
    For demonstration, we'll just return a small sample grid.
    """
    lines = loadfile("input.txt")
    grid = [list(map(int, list(line))) for line in lines]
    return grid

def neighbors(r, c, rows, cols):
    """4-directional neighbors."""
    for (dr, dc) in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def compute_ways(grid):
    """
    Return a 2D array 'ways' of the same shape as grid,
    where ways[r][c] = number of distinct 0→9 paths from (r,c) to any height=9 cell.
    """
    rows, cols = len(grid), len(grid[0])
    # We'll use memoization. ways[r][c] = None means "not computed yet".
    ways = [[None]*cols for _ in range(rows)]

    def dfs(r, c):
        """Compute ways[r][c] via DFS + memo."""
        if ways[r][c] is not None:
            # Already computed
            return ways[r][c]
        
        h = grid[r][c]
        # Base case
        if h == 9:
            ways[r][c] = 1
            return 1
        
        # Recursive case
        total_paths = 0
        for nr, nc in neighbors(r, c, rows, cols):
            if grid[nr][nc] == h + 1:  # Must be exactly 1 higher
                total_paths += dfs(nr, nc)

        ways[r][c] = total_paths
        return total_paths

    # Compute ways[r][c] for every cell (lazy approach: 
    # call dfs only on needed cells, or preemptively on all).
    for r in range(rows):
        for c in range(cols):
            if ways[r][c] is None:
                dfs(r, c)

    return ways

def solve():
    grid = read_map()
    rows, cols = len(grid), len(grid[0])

    # 1) Precompute ways[r][c]: the number of distinct 0→9 paths starting at (r,c)
    ways_grid = compute_ways(grid)

    # 2) Identify all trailheads (height=0), sum up ways for them
    total_rating = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                # The rating of this trailhead is ways_grid[r][c]
                # i.e., how many distinct 0→9 paths start here
                total_rating += ways_grid[r][c]
    
    print("Sum of the ratings of all trailheads:", total_rating)

if __name__ == "__main__":
    solve()
