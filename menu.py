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

    try:
        # Wait for dropdown menu to load and then click on an option
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(option)).click()
        # Wait until period tabs have loaded and then extract
        WebDriverWait(driver, 30).until(EC.any_of(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='nav nav-tabs']//li/a")),
                                                  EC.text_to_be_present_in_element((By.XPATH, "//div[@class='loading-content_loadingText_22OQi']"),
                                                                                   "Sorry, we weren't able to find menus for this location for the day you selected.")))
    except:
        continue
    # Extract the tabs
    period_tabs = driver.find_elements(By.XPATH, "//ul[@class='nav nav-tabs']//li/a")
    if not period_tabs:
        continue
    
    dining_hall_menu = {}

    for tab in period_tabs:        
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(tab)).click()
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-hidden='false']")))
            WebDriverWait(table, 10).until_not(EC.presence_of_element_located((By.XPATH, "//div[@class='loading-content_loadingText22OQi']")))
        except:
            continue
            
        stations_menu = []

        stations = table.find_elements(By.TAG_NAME, "table")
        if not stations:
            continue

        for station in stations:
            caption = station.find_element(By.XPATH, "caption")
            stations_menu.append(caption.text)
        
        dining_hall_menu[tab.text] = stations_menu

    menu[option.get_attribute("textContent").strip()] = dining_hall_menu
    
print(menu)
driver.quit()