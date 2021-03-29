import csv
from selenium import webdriver

def writeToFile():
    table = driver.find_element_by_css_selector("#gvwPensioners")
    with open('hyderabad.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements_by_css_selector('tr')[1:21]:
            cells = row.find_elements_by_css_selector('td')
            wr.writerow([d.text for d in cells])

driver = webdriver.Chrome()
driver.get("https://www.aasara.telangana.gov.in/SSPTG/UserInterface/Portal/GeneralSearch.aspx")
selector = driver.find_element_by_css_selector("#ddlDistrict")
driver.find_element_by_xpath("//*[@id='ddlDistrict']/option[4]").click()
#selector.select_by_value("Hyderabad")
submit = driver.find_element_by_css_selector("#btnSave")
submit.click()

writeToFile()

for x in range(1, 1000000):
    table = driver.find_element_by_css_selector("#gvwPensioners")
    linkrow = table.find_elements_by_css_selector('tr')[22]
    linkrowcells = linkrow.find_elements_by_css_selector('td')
    #print(len(linkrowcells))
    y=2
    if len(linkrowcells) == 12:
        y = 3
    for y in range(y, y+10):
        try:
            link = driver.find_element_by_css_selector("#gvwPensioners > tbody > tr:nth-child(22) > td > table > tbody > tr > td:nth-child(" + str(y) +") > a")
            print(link.get_attribute("href"))
            if link.get_attribute("href") is not None:
                link.click()
                writeToFile()
        except:
            print(1)