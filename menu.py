from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://dineoncampus.com/northwestern/whats-on-the-menu")

dropdown_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu-location-selector__BV_toggle_")))

dropdown_options = driver.find_elements(By.XPATH, "//ul[@id='building_6113ef5ae82971150a5bf8ba']//li/button")
for option in dropdown_options:
    dropdown_menu.click()
    option.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='tabs menu-periods']")))
    period_tabs = driver.find_elements(By.XPATH, "//ul[@class='nav nav-tabs']//li/a")
    for tab in period_tabs:
        print(tab.text)

driver.quit()