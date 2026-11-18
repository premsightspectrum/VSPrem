"""
Daily Report Bot - Social Eagle Gen AI Architect Program, Assignment 1.

Drives the real mouse and keyboard (PyAutoGUI) to:
  1. Open Chrome and load a public weather page (wttr.in, plain-text output)
  2. Copy the weather reading from the page
  3. Open a new Google Sheet (used instead of desktop Excel)
  4. Type a header row and a new row: date & time, weather, comment
  5. Rename the sheet to daily_report_YYYY-MM-DD
  6. Save a screenshot of the final sheet
  7. Download the sheet as .xlsx and move it into this folder

Windows + Chrome only. Chrome must be signed in to a Google account.
Hands off the mouse and keyboard while it runs.
Emergency stop: slam the mouse into any screen corner (FAILSAFE).
"""

import re
import shutil
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pygetwindow as gw   # installed with pyautogui on Windows
import pyperclip           # installed with pyautogui

# ---------- settings ----------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5          # small pause after every action

CITY = "Chennai"
WEATHER_URL = f"https://wttr.in/{CITY}?format=%l:+%t+%C"   # e.g. "Chennai: +27°C Partly cloudy"
SHEETS_URL = "https://sheets.new"

PROJECT_DIR = Path(__file__).resolve().parent
DOWNLOADS = Path.home() / "Downloads"

NOW = datetime.now()                      # generated at run time, never typed by hand
TODAY = NOW.strftime("%Y-%m-%d")          # 2026-11-19
TIMESTAMP = NOW.strftime("%Y-%m-%d %H:%M:%S")
REPORT_NAME = f"daily_report_{TODAY}"


# ---------- helpers ----------
def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}")


def paste_text(text):
    """Type via clipboard. pyautogui.write() can't type symbols like the degree sign."""
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


def wait_for_window(title_part, timeout):
    """Wait until a window whose title contains title_part exists, then focus it."""
    end = time.time() + timeout
    while time.time() < end:
        windows = [w for w in gw.getWindowsWithTitle(title_part) if w.title]
        if windows:
            win = windows[0]
            try:
                if win.isMinimized:
                    win.restore()
                win.activate()
            except Exception:
                pass  # Windows sometimes raises even when activation worked
            time.sleep(1)
            return win
        time.sleep(0.5)
    raise TimeoutError(f"No window containing '{title_part}' appeared within {timeout}s")


def go_to(url):
    pyautogui.hotkey("ctrl", "l")      # focus the address bar
    pyautogui.write(url, interval=0.02)
    pyautogui.press("enter")


def search_sheets_menu(text):
    """Google Sheets 'Search the menus' (Alt+/): reach any menu item by name, no coordinates needed."""
    pyautogui.hotkey("alt", "/")
    time.sleep(1)
    pyautogui.write(text, interval=0.05)
    time.sleep(1.5)
    pyautogui.press("enter")
    time.sleep(1)


# ---------- steps ----------
def open_chrome():
    log("Opening Chrome...")
    pyautogui.press("win")
    time.sleep(1.5)
    pyautogui.write("chrome", interval=0.05)
    time.sleep(1.5)
    pyautogui.press("enter")
    wait_for_window("Google Chrome", timeout=20)
    pyautogui.hotkey("win", "up")       # maximise so positions are predictable
    time.sleep(1)


def fetch_weather():
    log(f"Loading weather for {CITY}...")
    go_to(WEATHER_URL)

    # The page may load slowly, so retry copying until real data appears.
    width, height = pyautogui.size()
    for attempt in range(1, 11):
        time.sleep(2)
        pyautogui.click(width // 2, height // 2)   # make sure the page (not the address bar) has focus
        pyperclip.copy("")
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        text = pyperclip.paste().strip()
        if "°" in text:
            log(f"Copied: {text}")
            return text
        log(f"  attempt {attempt}: page not ready yet")
    raise RuntimeError("Could not copy weather data from the page")


def make_comment(weather):
    match = re.search(r"([+-]?\d+)\s*°", weather)
    if not match:
        return "Check conditions before heading out"
    temp = int(match.group(1))
    if temp >= 35:
        return "Very hot - stay indoors and hydrate"
    if temp >= 28:
        return "Warm - fine for short outdoor tasks"
    if temp >= 18:
        return "Pleasant - good for outdoor activities"
    return "Cool - carry a jacket"


def open_new_sheet():
    log("Opening a new Google Sheet...")
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    go_to(SHEETS_URL)
    wait_for_window("Google Sheets", timeout=40)
    time.sleep(5)                        # let the grid finish loading
    pyautogui.press("esc")
    pyautogui.hotkey("ctrl", "home")     # go to cell A1


def fill_rows(rows):
    log("Typing rows into the sheet...")
    for row in rows:
        for i, value in enumerate(row):
            paste_text(value)
            # Tab moves right; Enter after the last cell returns to column A on the next row
            pyautogui.press("tab" if i < len(row) - 1 else "enter")
    time.sleep(1)


def rename_sheet():
    log(f"Renaming sheet to {REPORT_NAME}...")
    search_sheets_menu("Rename")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(REPORT_NAME, interval=0.03)
    pyautogui.press("enter")
    time.sleep(2)


def take_screenshot():
    pyautogui.press("esc")
    pyautogui.hotkey("ctrl", "home")
    time.sleep(1)
    path = PROJECT_DIR / f"{REPORT_NAME}.png"
    pyautogui.screenshot(str(path))
    log(f"Screenshot saved: {path.name}")
    return path


def download_xlsx():
    log("Downloading as .xlsx...")
    started = time.time()
    search_sheets_menu("Microsoft Excel")      # File > Download > Microsoft Excel (.xlsx)

    # Wait for Chrome to finish the download (it uses .crdownload until complete).
    end = time.time() + 60
    while time.time() < end:
        new_files = [f for f in DOWNLOADS.glob("*.xlsx") if f.stat().st_mtime >= started - 2]
        if new_files:
            newest = max(new_files, key=lambda f: f.stat().st_mtime)
            time.sleep(1)
            dest = PROJECT_DIR / f"{REPORT_NAME}.xlsx"
            if dest.exists():
                dest.unlink()                  # replace an earlier run from the same day
            shutil.move(str(newest), str(dest))
            log(f"Excel file saved: {dest.name}")
            return dest
        time.sleep(1)
    raise TimeoutError("The .xlsx download did not appear in Downloads within 60s")


# ---------- main ----------
def check_dependencies():
    """Screenshots need Pillow; fail fast with a clear message instead of mid-run."""
    try:
        import PIL  # noqa: F401
    except ImportError:
        raise SystemExit("Pillow is missing. Run:  pip install pillow   then start the bot again.")


def step(name, func, *args):
    """Run one step and report exactly which step failed."""
    try:
        return func(*args)
    except pyautogui.FailSafeException:
        raise
    except Exception as err:
        raise RuntimeError(f"Step '{name}' failed: {err}") from err


def main():
    check_dependencies()
    log("Starting in 5 seconds. Hands off! Move the mouse to a screen corner to abort.")
    time.sleep(5)

    step("open Chrome", open_chrome)
    weather = step("fetch weather", fetch_weather)
    comment = make_comment(weather)

    step("open Google Sheet", open_new_sheet)
    step("fill rows", fill_rows, [
        ["Date & Time", f"Weather ({CITY})", "Comment"],
        [TIMESTAMP, weather, comment],
    ])
    step("rename sheet", rename_sheet)
    step("screenshot", take_screenshot)
    step("download .xlsx", download_xlsx)

    log("Done.")
    print(f"\n  Date & Time : {TIMESTAMP}\n  Weather     : {weather}\n  Comment     : {comment}")


if __name__ == "__main__":
    try:
        main()
    except pyautogui.FailSafeException:
        print("\nAborted: mouse moved to a screen corner.")
    except Exception as err:
        print(f"\nBot stopped: {err}")
