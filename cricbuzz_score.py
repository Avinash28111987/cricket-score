"""Print the NZ vs India session, team score and batter runs; save a screenshot."""

import re
from playwright.sync_api import TimeoutError
from playwright.sync_api import sync_playwright


URL = "https://www.cricbuzz.com/live-cricket-scores/161285/nz-vs-ind-1st-test-india-tour-of-new-zealand-2026"

# Playwright sync API moolama browser open panni match page-ku pogrom.
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    try:
        # Screenshot-la irukkira Batter heading varum vara wait pannrom; fixed sleep illa.
        page.get_by_text("Batter", exact=True).first.wait_for(state="visible", timeout=30000)
        text = " ".join(page.locator("body").inner_text().split())

        # Match session/day text print pannrom.
        session = re.search(r"Day\s+\d+\s*:\s*[^.]+?Session", text)
        if session:
            print(session.group(0))

        # Cricbuzz score e.g. NZ 107 -5 (38.4)-a irundhaalum, NZ 107/5 (38.4)-nu format pannrom.
        score = re.search(r"\bNZ\s+(\d+)\s*[-/]\s*(\d+)\s*\(([\d.]+)\)", text)
        if score:
            print(f"NZ {score.group(1)}/{score.group(2)} ({score.group(3)})")
        else:
            print("Team score not found")

        # Batter table-la player name-um runs-um mattum eduthu print pannrom.
        table = re.search(r"Batter\s+R\s+B\s+4s\s+6s\s+SR(.*?)Bowler", text)
        if table:
            batter_pattern = re.compile(
                r"([A-Za-z][A-Za-z .'-]*?)(?:\s+\*)?\s+(\d+)\s+\d+\s+\d+\s+\d+\s+[\d.]+"
            )
            for batter in batter_pattern.finditer(table.group(1)):
                print(f"{batter.group(1).strip()}: {batter.group(2)}")
    except TimeoutError:
        print("Score table did not appear. The page may have changed.")
    finally:
        # Timeout aanaalum screenshot save panni browser close pannrom.
        page.screenshot(path="score.png")
        print("saved score.png")
        browser.close()
