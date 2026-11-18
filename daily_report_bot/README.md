# Daily Report Bot

Social Eagle Gen AI Architect Program · Assignment 1 (PyAutoGUI automation).

A PyAutoGUI bot that prepares a daily status report by driving Chrome and Google Sheets
with the real mouse and keyboard. Google Sheets is used in place of desktop Excel; the
sheet is downloaded as a genuine `.xlsx` file.

## What it does
1. Opens Chrome and loads a public weather page (`wttr.in/Chennai`)
2. Copies the temperature and conditions from the page
3. Opens a new Google Sheet (`sheets.new`)
4. Adds a row: run-time date & time, the fetched weather, an auto comment based on temperature
5. Renames the sheet to `daily_report_YYYY-MM-DD`
6. Saves a screenshot `daily_report_YYYY-MM-DD.png`
7. Downloads the sheet as `.xlsx` and moves it here as `daily_report_YYYY-MM-DD.xlsx`

## Run
```
pip install pyautogui
python daily_report_bot.py
```
Requirements: Windows, Chrome signed in to a Google account. Don't touch the mouse or keyboard while it runs.

## Reliability choices
- **Waiting:** polls for windows by title (`pygetwindow`) instead of fixed sleeps, with timeouts
- **Slow pages:** retries copying the weather up to 10 times until real data appears
- **Focus:** activates and maximises the Chrome window so screen positions are predictable
- **No screen coordinates in Sheets:** uses keyboard shortcuts and the Sheets menu search (Alt+/)
- **Symbols:** types through the clipboard, since `pyautogui.write()` can't type `°`
- **Safety:** `FAILSAFE` on; moving the mouse to a corner aborts the run
