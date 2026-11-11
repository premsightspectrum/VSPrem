"""
Student Grade Manager - Social Eagle AI Program, Week 1 Day 2.

Storage choice: a dictionary keyed by the student's name in lowercase.
- Lookups and duplicate checks are instant (no scanning a list).
- "Priya" and "priya" count as the same student, so the same person
  can't be added twice by accident. If the name already exists, the
  user is asked whether to update that student's mark.
- Each value keeps the name as typed (for display) plus the mark.
"""

students = {}  # "priya" -> {"name": "Priya", "mark": 92.0}


def get_grade(mark):
    """Convert a mark (0-100) to a grade. Boundaries are inclusive."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def ask_name():
    """Ask for a name until a non-empty one is given. Returns None to cancel."""
    while True:
        name = input("Student name (or press Enter to cancel): ").strip()
        if not name:
            return None
        if any(ch.isdigit() for ch in name):
            print("  ! A name shouldn't contain numbers. Try again.")
            continue
        return " ".join(name.split())  # collapse extra spaces


def ask_mark():
    """Ask for a mark until a valid number between 0 and 100 is given."""
    while True:
        raw = input("Mark (0-100): ").strip()
        if not raw:
            print("  ! Mark can't be empty.")
            continue
        try:
            mark = float(raw)
        except ValueError:
            print(f"  ! '{raw}' is not a number. Enter a value like 78 or 82.5.")
            continue
        if not 0 <= mark <= 100:
            print(f"  ! {raw} is out of range. Marks must be between 0 and 100.")
            continue
        return mark


def ask_yes_no(question):
    """Return True for yes, False for no. Keeps asking until it gets one."""
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  ! Please type y or n.")


def add_student():
    name = ask_name()
    if name is None:
        print("  Cancelled.")
        return

    key = name.lower()
    if key in students:
        existing = students[key]
        print(f"  '{existing['name']}' already exists with mark {fmt(existing['mark'])}.")
        if not ask_yes_no("  Update their mark?"):
            print("  No changes made.")
            return

    mark = ask_mark()
    students[key] = {"name": name, "mark": mark}
    print(f"  Saved: {name} - {fmt(mark)} ({get_grade(mark)})")


def fmt(mark):
    """Show 92 instead of 92.0, but keep 82.5 as 82.5."""
    return str(int(mark)) if mark == int(mark) else f"{mark:.1f}"


def show_results():
    if not students:
        print("  No students yet. Add one first (option 1).")
        return

    width = max(len("Name"), max(len(s["name"]) for s in students.values())) + 2

    print()
    print(f"{'Name':<{width}}{'Mark':>6}{'Grade':>8}")
    print("-" * (width + 14))
    for s in students.values():
        print(f"{s['name']:<{width}}{fmt(s['mark']):>6}{get_grade(s['mark']):>8}")
    print("-" * (width + 14))

    marks = [s["mark"] for s in students.values()]
    average = sum(marks) / len(marks)
    print(f"Average: {average:.1f}    Highest: {fmt(max(marks))}    Lowest: {fmt(min(marks))}")
    print()


def main():
    print("=== Student Grade Manager ===")
    while True:
        print("\n1. Add student\n2. Show results\n3. Quit")
        choice = input("Choose 1, 2 or 3: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_results()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print(f"  ! '{choice}' is not an option. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Goodbye!")
