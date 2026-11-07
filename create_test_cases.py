import os
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

URL = "https://dola333.github.io/Hero-travel-repo/"

HEADERS = [
    "Test ID", "Module", "Test Scenario", "Preconditions", "Test Steps",
    "Test Data", "Expected Result", "Actual Result", "Status", "Priority",
    "Automated", "Automation Test Name",
]

TEST_CASES = [
    ["TC-001", "Home Page", "Verify home page loads with correct title",
     "Browser is open",
     "1. Open the Hero Travel URL\n2. Read the page title",
     URL, "Page title contains 'Hero Travel'",
     "Title contains 'Hero Travel'", "Pass", "High", "Yes", "test_home_page_title"],
    ["TC-002", "Home Page", "Verify main heading is displayed",
     "Home page is open",
     "1. Locate the main h1 heading",
     "-", "Main heading is visible",
     "Heading is visible", "Pass", "Medium", "Yes", "test_main_heading"],
    ["TC-003", "Navigation", "Verify Packages link opens Packages page",
     "Home page is open",
     "1. Click 'Packages' in the navbar",
     "Link: Packages", "URL contains packages.html",
     "URL contains packages.html", "Pass", "High", "Yes",
     "test_navbar_links[Packages-packages.html]"],
    ["TC-004", "Navigation", "Verify Testimonial link opens Testimonial page",
     "Home page is open",
     "1. Click 'Testimonial' in the navbar",
     "Link: Testimonial", "URL contains testimonial.html",
     "URL contains testimonial.html", "Pass", "High", "Yes",
     "test_navbar_links[Testimonial-testimonial.html]"],
    ["TC-005", "Navigation", "Verify Blog link opens Blog page",
     "Home page is open",
     "1. Click 'Blog' in the navbar",
     "Link: Blog", "URL contains blog.html",
     "URL contains blog.html", "Pass", "High", "Yes",
     "test_navbar_links[Blog-blog.html]"],
    ["TC-006", "Navigation", "Verify Contact link opens Contact page",
     "Home page is open",
     "1. Click 'Contact' in the navbar",
     "Link: Contact", "URL contains contact.html",
     "URL contains contact.html", "Pass", "High", "Yes",
     "test_navbar_links[Contact-contact.html]"],
    ["TC-007", "Search Form", "Verify Where / When / Type dropdowns can be selected",
     "Home page is open",
     "1. Select 'Bangladesh' in Where Go\n2. Select 'December' in When\n3. Select 'Beach Vacation' in Select Type",
     "Bangladesh, December, Beach Vacation",
     "All three selected values are shown in the dropdowns",
     "Selected values shown correctly", "Pass", "High", "Yes",
     "test_search_dropdowns"],
    ["TC-008", "Search Form", "Verify country dropdown contains expected countries",
     "Home page is open",
     "1. Open the Where Go dropdown\n2. Read all options",
     "Bangladesh, Japan",
     "Options include Bangladesh and Japan",
     "Both options found", "Pass", "Medium", "Yes", "test_country_options"],
    ["TC-009", "Deals", "Verify deals section shows tours and price",
     "Home page is open",
     "1. Scroll to Deals & Discounts\n2. Read tour names and price",
     "Satorini, Maldives, Dubai, $1300-$1500",
     "All three tours and the price text are displayed",
     "All tours and price displayed", "Pass", "Medium", "Yes",
     "test_deals_section"],
    ["TC-010", "Deals", "Verify Book Now buttons are present",
     "Home page is open",
     "1. Scroll to Deals & Discounts\n2. Count 'Book Now' buttons",
     "-", "At least 3 Book Now buttons exist",
     "3 or more buttons found", "Pass", "Medium", "Yes",
     "test_book_now_buttons"],
    ["TC-011", "Destinations", "Verify destination image links to Contact page",
     "Home page is open",
     "1. Scroll to Choose Your Destination\n2. Click a destination image",
     "-", "Contact page opens",
     "Contact page opened", "Pass", "Medium", "Yes",
     "test_destination_links_to_contact"],
    ["TC-012", "Newsletter", "Verify Subscribe link opens subscription page",
     "Home page is open",
     "1. Scroll to Newsletter\n2. Click 'Subscribe'",
     "-", "URL contains sub.html",
     "URL contains sub.html", "Pass", "Medium", "Yes",
     "test_subscribe_link"],
    ["TC-013", "Navigation", "Verify browser Back returns to home page",
     "Home page is open",
     "1. Open the Blog page\n2. Click browser Back",
     "-", "Home page URL is shown again",
     "Home page URL shown", "Pass", "Low", "Yes", "test_back_navigation"],
]


def output_folder():
    # When running as an .exe, save next to the .exe file.
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.getcwd()


def build_workbook():
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    thin = Side(style="thin", color="BBBBBB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    header_fill = PatternFill("solid", fgColor="1F4E78")

    ws.append(HEADERS)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border

    for row in TEST_CASES:
        ws.append(row)

    widths = [10, 14, 38, 20, 42, 28, 38, 30, 10, 10, 11, 40]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = w

    last_row = len(TEST_CASES) + 1
    for r in ws.iter_rows(min_row=2, max_row=last_row):
        for cell in r:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border

    # Dropdown lists
    status_dv = DataValidation(type="list", formula1='"Pass,Fail,Blocked,Not Run"', allow_blank=True)
    priority_dv = DataValidation(type="list", formula1='"High,Medium,Low"', allow_blank=True)
    auto_dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    for dv in (status_dv, priority_dv, auto_dv):
        ws.add_data_validation(dv)
    status_dv.add(f"I2:I{last_row}")
    priority_dv.add(f"J2:J{last_row}")
    auto_dv.add(f"K2:K{last_row}")

    # Colour the Status column
    rng = f"I2:I{last_row}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Pass"'],
                                  fill=PatternFill("solid", bgColor="C6EFCE"), font=Font(color="006100")))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Fail"'],
                                  fill=PatternFill("solid", bgColor="FFC7CE"), font=Font(color="9C0006")))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Blocked"'],
                                  fill=PatternFill("solid", bgColor="FFEB9C"), font=Font(color="9C5700")))

    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:L{last_row}"

    # Summary sheet with live formulas
    sm = wb.create_sheet("Summary")
    sm["A1"] = "Hero Travel - Test Summary"
    sm["A1"].font = Font(bold=True, size=14)
    sm["A3"], sm["B3"] = "Application URL", URL
    sm["A4"], sm["B4"] = "Date", date.today().strftime("%d-%b-%Y")
    sm["A5"], sm["B5"] = "Tested by", "Nabila Binte Delwar Dola"
    sm["A6"], sm["B6"] = "Tool", "Selenium + Python + pytest"

    sm["A8"], sm["B8"] = "Metric", "Count"
    sm["A8"].font = sm["B8"].font = Font(bold=True, color="FFFFFF")
    sm["A8"].fill = sm["B8"].fill = header_fill
    labels = [
        ("Total test cases", f"=COUNTA('Test Cases'!A2:A{last_row})"),
        ("Passed", f"=COUNTIF('Test Cases'!I2:I{last_row},\"Pass\")"),
        ("Failed", f"=COUNTIF('Test Cases'!I2:I{last_row},\"Fail\")"),
        ("Blocked", f"=COUNTIF('Test Cases'!I2:I{last_row},\"Blocked\")"),
        ("Not run", f"=COUNTIF('Test Cases'!I2:I{last_row},\"Not Run\")"),
        ("Pass rate", "=IF(B9=0,0,B10/B9)"),
    ]
    for i, (label, formula) in enumerate(labels, start=9):
        sm[f"A{i}"] = label
        sm[f"B{i}"] = formula
    sm["B14"].number_format = "0.0%"
    sm.column_dimensions["A"].width = 22
    sm.column_dimensions["B"].width = 60
    return wb


def main():
    wb = build_workbook()
    path = os.path.join(output_folder(), "Hero_Travel_Test_Cases.xlsx")
    wb.save(path)
    print("Spreadsheet created:")
    print(path)
    input("Press Enter to close...")


main()