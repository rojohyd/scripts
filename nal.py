import csv
from selenium import webdriver

def writeToFile(filename):
    table = driver.find_element_by_css_selector("#gvwPensioners")
    with open('nalgonda_'+str(filename)+'.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements_by_css_selector('tr')[1:21]:
            cells = row.find_elements_by_css_selector('td')
            wr.writerow([d.text for d in cells])

mandalList = [33]
for mandal in mandalList:
    driver = webdriver.Chrome()
    driver.get("https://www.aasara.telangana.gov.in/SSPTG/UserInterface/Portal/GeneralSearch.aspx")
    selector = driver.find_element_by_css_selector("#ddlDistrict")
    driver.find_element_by_xpath("//*[@id='ddlDistrict']/option[20]").click()
    driver.find_element_by_xpath("//*[@id='ddlMandal']/option["+str(mandal)+"]").click()
    submit = driver.find_element_by_css_selector("#btnSave")
    submit.click()
    writeToFile(mandal)
    for x in range(1, 1000000):
        try:
            table = driver.find_element_by_css_selector("#gvwPensioners")
            linkrow = table.find_elements_by_css_selector('tr')[22]
            linkrowcells = linkrow.find_elements_by_css_selector('td')
            #print(len(linkrowcells))
            y=2
            z=1
            if len(linkrowcells) == 12:
                y = 3
                z = 0
            for y in range(y, y+len(linkrowcells)-2+z):
                    link = driver.find_element_by_css_selector("#gvwPensioners > tbody > tr:nth-child(22) > td > table > tbody > tr > td:nth-child(" + str(y) +") > a")
                    print(link.get_attribute("href"))
                    if link.get_attribute("href") is not None:
                        link.click()
                        writeToFile(mandal)
        except:
            driver.close()
            driver.quit()
            break