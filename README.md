# Mini Sudoku (4x4) — Python CLI Game

A tiny, terminal-based Sudoku designed for my technical portfolio. It generates uniquely solvable 4×4 puzzles, lets you play with simple commands, and can give hints or solve the puzzle for you.

## Features
- 4×4 Sudoku with **unique-solution** puzzles
- **Hint**, **Check**, **Reset**, **New**, **Solve** commands
- Prevents edits to given clues
- Pure Python (no external libraries)

## How to Run
1. Make sure you have **Python 3.8+** installed.
2. Open a terminal where the file is located and run:
   ```bash
   python3 mini_sudoku.py
   ```
   (On Windows you may use `py mini_sudoku.py`.)

## How to Play
- The board shows rows (r1–r4) and columns (c1–c4). Empty cells are `.`
- Enter moves as `row col value`, for example:
  ```
  2 3 4
  ```
- Available commands:
  - `hint`  — fill one correct empty cell
  - `check` — validate current board state
  - `solve` — auto-solve the puzzle
  - `reset` — return to the starting puzzle
  - `new`   — generate a new puzzle
  - `help`  — show all commands
  - `q`     — quit

## Suggested Portfolio Description
**Mini Sudoku (4x4) — Python CLI Game**  
A lightweight Sudoku game built in pure Python. Implements a backtracking solver, unique-solution puzzle generation, and a simple command-line interface with move validation, hints, and auto-solve. Built to demonstrate algorithmic thinking (backtracking, constraint checks) and clean CLI UX.

## Optional: Add a Screenshot
Run the game and take a screenshot of the terminal for your portfolio.

## License
MIT
