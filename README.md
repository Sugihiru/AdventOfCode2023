# AdventOfCode2023
My solutions for the Advent of Code 2023 edition 

This is done in Python3, tested with Python 3.11.0 but most of it should run in other Python versions without too much problems.

The architecture is mostly the same between each exercice. There's a directory for each day, each one containing a `main.py`.

Inside each `main.py`, there's at least two classes, one for each part of an exercice. Sometimes, they share common code so `Part02` will inherit from `Part01`, sometimes it won't. Each class includes its own set of tests methods, all of them are prefixed with `test_{function_name}`. Tests are added if needed and are not meant to be exhaustive at all, but only serves to help debugging the program in the context of the AoC input.

You can run each file using `python3 main.py` inside its folder. It will automatically run the tests, and display the result for part 1 and part 2 if there's an `input.txt` file inside the folder of the script.
