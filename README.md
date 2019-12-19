# Sudoku

Command Line Sudoku Solver containing one logical and one brute force solver for Python 3

### Load sudoku from test file and solve

To solve an existing sudoku (e.g. one of the example puzzles) please use the following commands

```
import solver

solver.load_and_solve('s15a')
solver.load_and_solve('s15a', brute_force=True)
```

The default solver is the logical one, it is not guaranteed to converge.
To use brute_force solver please set flag.

### Enter sudoku via command line and solve

To solve a custom solver please use the following commands

```
import solver

solver.enter_and_solve()
solver.enter_and_solve(brute_force=True)
```

The solver will let you enter your sudoku via the command line. Please use the number keys or space for empty cell
