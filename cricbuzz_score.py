"""
cricbuzz_score.py

Week 1 - Day 3 - Task 1
Capture a Live Cricket Score with Playwright

Indha program:
1. Playwright sync API use pannum.
2. Cricbuzz website-ai real browser-la open pannum.
3. Live score element-ai inspect panni kandupidikka configured selector-ai use pannum.
4. Fixed sleep use pannama Playwright wait_for_selector() use pannum.
5. Score text-ai terminal-la print pannum.
6. score.png screenshot save pannum.
7. Live match illaina clear-a message print pannum.
8. Headed mode-la first run panna mudiyum.
9. HEADLESS=true set pannina headless mode-la run panna mudiyum.

IMPORTANT:
- Assignment requirement prakaram selector page inspection moolama identify panna vendum.
- Cricbuzz UI/DOM changes aagumbodhu selector change aagalam.
- CRICBUZZ_SCORE_SELECTOR environment variable-la selector override panna mudiyum.
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


# ============================================================
# BLOCK 1 - BASIC CONFIGURATION
# ============================================================
# Indha block-la Cricbuzz URL, screenshot filename,
# selector wait timeout madhiri basic settings define panrom.
#
# Assignment-la fixed sleep use panna koodadhu nu specifically sollirukku.
# Adhanala timeout use pannrom; actual element varum vara Playwright wait pannum.

CRICBUZZ_URL = "https://www.cricbuzz.com/"
SCREENSHOT_FILE = Path("score.png")

# Browser-la live score element-ai Inspect panni kandupidicha selector-ai
# inga configure panna vendum.
#
# Default selector:
# Cricbuzz current DOM-la scorecard/live score elements-ku common-a
# use aagura scorecard class selector.
#
# IMPORTANT:
# Assignment asks us to find the selector ourselves by inspecting the page.
# So browser inspection-la verify pannitu indha value-ai update pannunga.
DEFAULT_SCORE_SELECTOR = ".cb-col.cb-col-100.cb-scrs-wrp"

# Environment variable use pannina code change pannama selector replace pannalaam.
SCORE_SELECTOR = os.getenv(
    "CRICBUZZ_SCORE_SELECTOR",
    DEFAULT_SCORE_SELECTOR
)

# HEADLESS false -> browser visible-a open aagum.
# Assignment first headed mode-la run panna sollirukku.
# HEADLESS=true -> browser background-la run aagum.
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Element wait timeout milliseconds.
# Idhu fixed sleep illa; required DOM element varum vara Playwright wait pannum.
WAIT_TIMEOUT_MS = 15000


# ============================================================
# BLOCK 2 - PRINT HEADER
# ============================================================
# Program start aagumbodhu terminal-la useful information print panrom.
# Idhu debugging-ku useful-a irukkum.

def print_startup_info():
    print("=" * 60)
    print("Cricbuzz Live Cricket Score - Playwright")
    print("=" * 60)
    print(f"URL       : {CRICBUZZ_URL}")
    print(f"Selector  : {SCORE_SELECTOR}")
    print(f"Headless  : {HEADLESS}")
    print("=" * 60)


# ============================================================
# BLOCK 3 - OPEN BROWSER AND CRICBUZZ
# ============================================================
# Playwright sync API use pannrom.
# Chromium browser launch pannitu Cricbuzz open pannrom.
#
# Assignment requirement:
# "Use Playwright's sync API to open cricbuzz.com."
#
# wait_until="domcontentloaded" use pannrom.
# Idhu page basic DOM ready aagum vara wait pannum.
# Live score-ku separate wait_for_selector() use pannrom.

def open_cricbuzz(page):
    print("[INFO] Opening Cricbuzz...")

    page.goto(
        CRICBUZZ_URL,
        wait_until="domcontentloaded",
        timeout=WAIT_TIMEOUT_MS
    )

    print("[INFO] Cricbuzz page loaded.")


# ============================================================
# BLOCK 4 - WAIT FOR LIVE SCORE ELEMENT
# ============================================================
# Idhu assignment-oda most important requirement.
#
# Fixed time sleep(5) use pannala.
# Instead, Playwright-kitta:
# "Indha selector-oda element DOM-la varum vara wait pannu"
# nu sollrom.
#
# Site slow-a irundhaalum element varum vara Playwright wait pannum.
# Timeout exceed aana no live score / selector issue nu handle pannrom.

def wait_for_score_element(page):
    print("[INFO] Waiting for live score element...")

    try:
        score_element = page.locator(SCORE_SELECTOR).first

        # Element visible-a varum vara wait pannrom.
        score_element.wait_for(
            state="visible",
            timeout=WAIT_TIMEOUT_MS
        )

        print("[INFO] Live score element found.")

        return score_element

    except PlaywrightTimeoutError:
        print("[WARN] Live score element was not found within timeout.")
        return None


# ============================================================
# BLOCK 5 - EXTRACT SCORE TEXT
# ============================================================
# Score element kidaichadhum inner_text() use panni
# browser-la visible-a irukkura score text-ai extract pannrom.
#
# Example:
# IND 287/4 (45.2 Ov)
#
# Empty text vandhaalum graceful-a handle pannrom.

def extract_score(score_element):
    if score_element is None:
        return None

    try:
        score_text = score_element.inner_text().strip()

    except Exception as error:
        print(f"[ERROR] Could not read score text: {error}")
        return None

    if not score_text:
        print("[WARN] Score element was found but contains no text.")
        return None

    return score_text


# ============================================================
# BLOCK 6 - SAVE SCREENSHOT
# ============================================================
# Assignment requirement:
# "Save a screenshot as score.png."
#
# Browser page visible-a irukkumbodhu complete page screenshot edukkrom.
# Screenshot current browser state-ai capture pannum.

def save_screenshot(page):
    print(f"[INFO] Saving screenshot: {SCREENSHOT_FILE}")

    page.screenshot(
        path=str(SCREENSHOT_FILE),
        full_page=True
    )

    print("[INFO] Screenshot saved successfully.")


# ============================================================
# BLOCK 7 - HANDLE NO LIVE MATCH
# ============================================================
# Cricbuzz page open aagalam, aana live match illama irukkalam.
# Appo program crash aagakoodadhu.
#
# Instead terminal-la clear message print pannitu
# screenshot save pannalaam.

def handle_no_live_score(page):
    print("=" * 60)
    print("NO LIVE SCORE FOUND")
    print("=" * 60)
    print(
        "No live score element was found. "
        "There may be no live match right now, "
        "or the Cricbuzz selector may have changed."
    )

    # Assignment screenshot requirement satisfy panna,
    # current Cricbuzz page-oda screenshot save pannrom.
    save_screenshot(page)


# ============================================================
# BLOCK 8 - MAIN PROGRAM
# ============================================================
# Idhu complete automation flow:
#
# 1. Playwright start
# 2. Chromium launch
# 3. Cricbuzz open
# 4. Live score element-ku wait
# 5. Score text extract
# 6. Terminal-la print
# 7. score.png save
# 8. Browser close
#
# Browser headed/headless mode environment variable moolama control pannalaam.

def main():
    print_startup_info()

    try:
        with sync_playwright() as p:

            # Browser launch.
            # HEADLESS=false -> browser screen-la visible-a irukkum.
            # HEADLESS=true  -> browser hidden/background-la run aagum.
            browser = p.chromium.launch(
                headless=HEADLESS
            )

            # New browser page create pannrom.
            page = browser.new_page(
                viewport={
                    "width": 1440,
                    "height": 900
                }
            )

            try:
                # Cricbuzz open pannrom.
                open_cricbuzz(page)

                # Live score element varum vara wait pannrom.
                score_element = wait_for_score_element(page)

                # Score text extract pannrom.
                score_text = extract_score(score_element)

                if score_text:
                    # Assignment requirement:
                    # "Print the score text to your terminal."
                    print("=" * 60)
                    print("LIVE CRICKET SCORE")
                    print("=" * 60)
                    print(score_text)
                    print("=" * 60)

                    # Final page screenshot save pannrom.
                    save_screenshot(page)

                else:
                    # Live match / score available illaina
                    # graceful handling.
                    handle_no_live_score(page)

            finally:
                # Browser resources properly close pannrom.
                browser.close()

    except PlaywrightTimeoutError as error:
        print("=" * 60)
        print("PLAYWRIGHT TIMEOUT")
        print("=" * 60)
        print(f"Error: {error}")
        sys.exit(1)

    except Exception as error:
        print("=" * 60)
        print("PROGRAM FAILED")
        print("=" * 60)
        print(f"Error: {error}")
        print()
        print("Check the following:")
        print("1. Playwright is installed.")
        print("2. Chromium browser is installed.")
        print("3. Internet connection is available.")
        print("4. Cricbuzz is accessible.")
        print("5. SCORE_SELECTOR matches the current Cricbuzz DOM.")
        sys.exit(1)

    print()
    print("Program completed.")
    print(f"Screenshot: {SCREENSHOT_FILE}")


# ============================================================
# BLOCK 9 - PYTHON ENTRY POINT
# ============================================================
# Indha standard Python entry point use pannuvadhala
# file direct-a execute pannumbodhu main() call aagum.

if __name__ == "__main__":
    main()
