import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def writeToFile(filename):
    time.sleep(1)
    table = driver.find_element_by_css_selector("#ContentPlaceHolder1_GridView1")
    with open('nalgonda_pmkisan_'+str(filename)+'.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements_by_css_selector('tr')[1:51]:
            cells = row.find_elements_by_css_selector('td')
            wr.writerow([d.text for d in cells])
            
def returnNextLink():
    span = driver.execute_script("""td = $('#ContentPlaceHolder1_GridView1 > tbody > tr:last-child > td > table > tbody > tr > td');
    l = td.length,ind = null;
    for (var i = 0; i < l; i++) {
        if (td[i].innerHTML.indexOf('span') > -1) {
           ind = i;
           break;
        }
    }
    return ind;""")
    if span is not None:
        print('span:'+str(span))
        return span+2
    return None
        

def loadMandal(mandal):
    #driver.close()
    #driver = webdriver.Chrome()
    driver.get("https://pmkisan.gov.in/Rpt_BeneficiaryStatus_pub.aspx")
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownState']/option[32]").click()
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownDistrict']/option[20]").click()
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownSubDistrict']/option["+str(mandal)+"]").click()
    driver.implicitly_wait(15)
    print(len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_DropDownBlock']/option")))

def loadBlock(x,mandal):
    loadMandal(mandal)
    blocksSize =len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_DropDownBlock']/option"))
    time.sleep(1)
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownBlock")))
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_DropDownBlock']/option[2]")))
    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ContentPlaceHolder1_DropDownBlock']/option[2]")))
    block = driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownBlock']/option["+str(x)+"]").text
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownBlock']/option["+str(x)+"]").click()

def loadVillage(y,x,mandal):
    loadBlock(x,mandal)
    #print(y)
    time.sleep(1)
    #element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownVillage")))
    #element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_DropDownVillage']/option[2]")))
    #element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ContentPlaceHolder1_DropDownVillage']/option[2]")))
    village = driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownVillage']/option["+str(y)+"]").text
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownVillage']/option["+str(y)+"]").click()

mandalList = [3]
for mandal in mandalList:
    driver = webdriver.Chrome()
    loadMandal(mandal)
    
    driver.execute_script("""
    var script = document.createElement( 'script' );
    script.type = 'text/javascript';
    script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
    document.head.appendChild(script);
    """)
    
    blocksSize =len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_DropDownBlock']/option"))
    
    for x in range(2,int(blocksSize)+1):
        try:
            #print(x)
            loadBlock(x,mandal)
            block = driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownBlock']/option["+str(x)+"]").text
            villageSize = len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_DropDownVillage']/option"))
            for y in range(2,int(villageSize)+1):
                try:
                    loadVillage(y,x,mandal)
                    submit = driver.find_element_by_css_selector("#ContentPlaceHolder1_btnsubmit")
                    submit.click()
                    time.sleep(1)
                    village = driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_DropDownVillage']/option["+str(y)+"]").text
                    
                    writeToFile(str(mandal)+"_"+str(block)+"_"+str(village))
                    while True:
                        try:
                            next = returnNextLink()
                            if next is None:
                                break
                            link = driver.find_element_by_css_selector("#ContentPlaceHolder1_GridView1 > tbody > tr:last-child > td > table > tbody > tr > td:nth-child(" + str(next) +") > a")
                            print(link.get_attribute("href"))
                            if link.get_attribute("href") is not None:
                                link.click()
                                table = driver.find_element_by_css_selector("#ContentPlaceHolder1_GridView1")
                                #element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,"#ContentPlaceHolder1_GridView1")))
                                #time.sleep(1)
                                writeToFile(str(mandal)+"_"+str(block)+"_"+str(village))
                        except:
                            driver.refresh()
                            #driver.quit()
                            print('here')
                            break
                except:
                    driver.refresh()
                    print('here y')
                    continue
        except:
            driver.refresh()
            print('here x')
            continue
                    
        #break
