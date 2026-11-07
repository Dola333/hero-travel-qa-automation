from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://dola333.github.io/Hero-travel-repo/")

print("Title:", driver.title)
assert "Hero Travel" in driver.title

driver.quit()