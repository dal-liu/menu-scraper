import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_menu():
    menu = {}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://dineoncampus.com/northwestern/whats-on-the-menu")
    # Wait for dropdown to load and extract it
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "menu-location-selector__BV_toggle_"))
    )
    # Extract list of all dining halls from the dropdown
    dropdown_options = driver.find_elements(
        By.XPATH, "//ul[@id='building_6113ef5ae82971150a5bf8ba']//li/button"
    )
    time.sleep(10)
    # Iterate through dining halls
    for option in dropdown_options:
        dropdown_menu.click()
        try:
            # Wait for dropdown menu to load and then click on an option
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(option)).click()
            # Wait until period tabs have loaded and then extract
            WebDriverWait(driver, 30).until(
                EC.any_of(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//ul[@class='nav nav-tabs']//li/a")
                    ),
                    EC.text_to_be_present_in_element(
                        (By.XPATH, "//div[@class='loading-content_loadingText_22OQi']"),
                        "Sorry, we weren't able to find menus for this location for the day you selected.",
                    ),
                )
            )
        except:
            continue
        # Extract the tabs
        menu[option.get_attribute("textContent").strip()] = _create_periods_list(driver)

    driver.quit()
    return menu


def _create_periods_list(driver):
    tabs = driver.find_elements(By.XPATH, "//ul[@class='nav nav-tabs']//li/a")
    periods_list = []
    if tabs:
        for tab in tabs:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(tab)).click()
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@role='tabpanel' and @aria-hidden='false']")
                    )
                )
                WebDriverWait(table, 30).until(
                    EC.any_of(
                        EC.presence_of_element_located(
                            (By.XPATH, "div/div[@class='row menu-period-dropdowns']")
                        ),
                        EC.text_to_be_present_in_element(
                            (
                                By.XPATH,
                                "div/div[@class='loading-content_loadingText_22OQi']",
                            ),
                            "Sorry, we weren't able to find menus for this location for the day you selected.",
                        ),
                    )
                )  # TODO fix this and add retry
            except:
                continue
            stations = table.find_elements(By.TAG_NAME, "table")
            if not stations:
                continue
            periods_list.append(_create_period(tab.text, stations))
    return periods_list


def _create_period(tab_name, stations):
    return {"name": tab_name, "stations": _create_stations_list(stations)}


def _create_stations_list(stations):
    stations_list = []
    for station in stations:
        items = station.find_elements(By.XPATH, "tbody[@role='rowgroup']/tr")
        stations_list.append(
            _create_station(station.find_element(By.TAG_NAME, "caption").text, items)
        )
    return stations_list


def _create_station(station_name, items):
    return {"name": station_name, "items": _create_items_list(items)}


def _create_items_list(items):
    return [_create_item(item) for item in items]


def _create_item(item):
    properties = item.find_elements(By.TAG_NAME, "td")
    return {
        "name": properties[0].find_element(By.TAG_NAME, "strong").text.strip(),
        # "description": properties[0].find_element(By.XPATH, "div/span").text,
        "portion": properties[1].text,
        "calories": int(properties[2].text),
    }


with open("menu.json", "w") as json_file:
    json.dump(create_menu(), json_file, indent=4)
