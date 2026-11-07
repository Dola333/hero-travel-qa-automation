# Hero Travel QA Automation

Testing project for my Hero Travel website:
https://dola333.github.io/Hero-travel-repo/

## What is inside
- test_hero_travel.py: 13 Selenium + pytest UI tests (navigation, dropdowns, deals, links)
- report.html: pytest-html report (13 passed)
- create_test_cases.py: generates Hero_Travel_Test_Cases.xlsx (test case sheet)
- hero-load-test.js: k6 load test (3 users, 15 seconds)
- k6-result.txt: k6 results

## How to run
pip install selenium pytest pytest-html
pytest test_hero_travel.py -v --html=report.html --self-contained-html
k6 run hero-load-test.js

## Tools
Python, Selenium, pytest, k6, openpyxl