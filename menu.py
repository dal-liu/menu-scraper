from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _create_station(station):
    period_items = []
    items = station.find_elements(By.XPATH, "tbody[@role='rowgroup']/tr")
    for item in items:
        period_items.append(_create_item(item))
    
    return {
        "name": station.find_element(By.TAG_NAME, "caption").text,
        "items": period_items
    }


def _create_item(item):
    properties = item.find_elements(By.TAG_NAME, "td")
    return {
        "name": properties[0].find_element(By.TAG_NAME, "strong").text.strip(),
        # "description": properties[0].find_element(By.XPATH, "div/span").text,
        "portion": properties[1].text,
        "calories": int(properties[2].text)
    }


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
    # Dict with keys of time periods and values of the stations and food
    dining_periods = []

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
    if period_tabs:
        for tab in period_tabs:
            dining_period = { "name" : tab.text }
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable(tab)).click()
                table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='tabpanel' and @aria-hidden='false']")))
                WebDriverWait(table, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='row menu-period-dropdowns']"))) #TODO: need to add retry in case fetching fails
            except:
                continue
            stations = table.find_elements(By.TAG_NAME, "table")
            if not stations:
                continue
            # List of stations
            period_stations = []

            for station in stations:
                caption = station.find_element(By.TAG_NAME, "caption").text
                period_station = { "name" : caption }
                period_items = []

                items = station.find_elements(By.XPATH, "tbody[@role='rowgroup']/tr")
                for item in items:
                    period_items.append(_create_item(item))

                period_station["items"] = period_items
                period_stations.append(period_station)
            
            dining_period["stations"] = period_stations

        dining_periods.append(dining_period)

    menu[option.get_attribute("textContent").strip()] = dining_periods
    
print(menu)
driver.quit()