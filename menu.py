from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

menu = {}

driver = webdriver.Chrome()

driver.get("https://dineoncampus.com/northwestern/whats-on-the-menu")

# Wait for dropdown to load and extract it
dropdown_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu-location-selector__BV_toggle_")))
# Extract list of all dining halls from the dropdown
dropdown_options = driver.find_elements(By.XPATH, "//ul[@id='building_6113ef5ae82971150a5bf8ba']//li/button")
# Iterate through dining halls
for option in dropdown_options:
    dropdown_menu.click()
    # Wait for dropdown menu to load and then click on an option
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(option)).click()

    dining_hall_menu = []
    try:
        # Wait until period tabs have loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='tabs menu-periods']")))
    except:
        continue
    # Extract the tabs
    period_tabs = driver.find_elements(By.XPATH, "//ul[@class='nav nav-tabs']//li/a")
    for tab in period_tabs:
        tab.click()
        
        try:
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-hidden='false']")))
        except:
            continue
            
        period = tab.text
        print(period)

        stations = table.find_elements(By.TAG_NAME, "table")
        for station in stations:
            caption = station.find_element(By.XPATH, "caption")
            print(caption.text)

    dining_hall = option.get_attribute("textContent").strip()
    menu[dining_hall] = dining_hall_menu
    
print(menu)
driver.quit()