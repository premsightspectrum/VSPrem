# Student Grade Manager

Social Eagle AI Program, Batch 13 · Week 1 · Day 2 assignment.

A terminal Python program that stores student marks, works out each student's grade,
and prints an aligned results table with the class average, highest and lowest mark.

## Run it

```
cd grade_manager
python grade_manager.py
```

Menu: `1` Add student · `2` Show results · `3` Quit

## Grading scale (boundaries inclusive)

| Mark | Grade |
|---|---|
| 90 to 100 | A |
| 80 to 89 | B |
| 70 to 79 | C |
| 60 to 69 | D |
| Below 60 | E |

## Design choices

**Storage:** a dictionary keyed by the lowercase student name, e.g.
`{"priya": {"name": "Priya", "mark": 92.0}}`. Lookups and duplicate checks are instant,
and "Priya" / "priya" are treated as the same student. On a duplicate name, the program
asks whether to update that student's mark instead of silently adding a second entry.

## Invalid input handling

| Input | Behaviour |
|---|---|
| Mark `105` or `-5` | Rejected: must be 0 to 100, asks again |
| Mark `abc` | Rejected: not a number (`try/except` on `float`), asks again |
| Empty mark | Rejected, asks again |
| Empty name | Cancels the add and returns to the menu |
| Name with digits | Rejected, asks again |
| Menu option other than 1/2/3 | Rejected, menu shown again |
| Show results with no students | Friendly message, no divide-by-zero |
| Ctrl+C / Ctrl+D | Exits cleanly instead of a traceback |

## Sample output

```
Name     Mark   Grade
---------------------
Priya      92       A
Arun       78       C
Divya      59       E
---------------------
Average: 76.3    Highest: 92    Lowest: 59
```
