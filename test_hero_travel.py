import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://dola333.github.io/Hero-travel-repo/"

def click_and_follow(driver, element):
    """Click a link. If it opens a new tab, switch to that tab."""
    old_tabs = driver.window_handles
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element.click()
    WebDriverWait(driver, 10).until(lambda d: True)
    new_tabs = driver.window_handles
    if len(new_tabs) > len(old_tabs):
        driver.switch_to.window(new_tabs[-1])


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    d.implicitly_wait(5)
    d.get(BASE)
    yield d          # the test runs here
    d.quit()         # cleanup after each test


# 1. Page loads correctly
def test_home_page_title(driver):
    assert "Hero Travel" in driver.title


# 2. Main heading is visible
def test_main_heading(driver):
    heading = driver.find_element(By.TAG_NAME, "h1")
    assert heading.is_displayed()


# 3. Navbar links go to the right pages
@pytest.mark.parametrize("link_text, expected_url_part", [
    ("Packages", "packages.html"),
    ("Testimonial", "testimonial.html"),
    ("Blog", "blog.html"),
    ("Contact", "contact.html"),
])
def test_navbar_links(driver, link_text, expected_url_part):
    link = driver.find_element(By.LINK_TEXT, link_text)
    click_and_follow(driver, link)
    WebDriverWait(driver, 10).until(EC.url_contains(expected_url_part))
    assert expected_url_part in driver.current_url




# 4. Dropdowns: Where / When / Type
def test_search_dropdowns(driver):
    selects = driver.find_elements(By.TAG_NAME, "select")
    assert len(selects) >= 3

    Select(selects[0]).select_by_visible_text("Bangladesh")
    Select(selects[1]).select_by_visible_text("December")
    Select(selects[2]).select_by_visible_text("Beach Vacation")

    assert Select(selects[0]).first_selected_option.text == "Bangladesh"
    assert Select(selects[1]).first_selected_option.text == "December"
    assert Select(selects[2]).first_selected_option.text == "Beach Vacation"


# 5. Country dropdown has the expected options
def test_country_options(driver):
    country = Select(driver.find_elements(By.TAG_NAME, "select")[0])
    names = [o.text for o in country.options]
    assert "Bangladesh" in names
    assert "Japan" in names


# 6. Deals section shows tours and prices
def test_deals_section(driver):
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Tour To Satorini" in body_text
    assert "Tour To Maldives" in body_text
    assert "Tour To Dubai" in body_text
    assert "Price: $1300-$1500" in body_text


# 7. Book Now buttons exist
def test_book_now_buttons(driver):
    buttons = driver.find_elements(By.XPATH, "//*[normalize-space()='Book Now']")
    assert len(buttons) >= 3


# 8. Destination images link to the contact page
def test_destination_links_to_contact(driver):
    link = driver.find_element(By.CSS_SELECTOR, "a[href*='contact.html']")
    driver.execute_script("arguments[0].click();", link)   # JS click ignores overlays
    WebDriverWait(driver, 10).until(lambda d: "contact.html" in d.current_url
                                    or len(d.window_handles) > 1)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(EC.url_contains("contact.html"))
    assert "contact.html" in driver.current_url


# 9. Subscribe link opens the subscription page
def test_subscribe_link(driver):
    sub = driver.find_element(By.LINK_TEXT, "Subscribe")
    click_and_follow(driver, sub)
    WebDriverWait(driver, 10).until(EC.url_contains("sub.html"))
    assert "sub.html" in driver.current_url


# 10. Back navigation works
def test_back_navigation(driver):
    driver.get(BASE + "blog.html")
    driver.back()
    assert driver.current_url.rstrip("/") == BASE.rstrip("/")