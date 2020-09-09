import time
import csv
import pprint

from selenium                       import webdriver
from selenium.common.exceptions     import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

URLS_FILENAME    = "stockx_product_urls.csv"
DETAILS_FILENAME = "stockx_products.csv"
IMPLICIT_WAIT    = 5

# urls 모아져있는 csv 파일 열기
csv_urls_open    = open(URLS_FILENAME, 'r', encoding='utf-8')
csv_details_open = open(DETAILS_FILENAME, 'a', encoding="utf-8")
csv_reader       = csv.reader(csv_urls_open)
csv_writer       = csv.writer(csv_details_open)

driver = webdriver.Chrome()
action_chains = ActionChains(driver)

COUNT = 2036

for i, row in enumerate(csv_reader):
    if i < COUNT:
        continue

    jordan_number  = row[0]
    size_type      = row[1]
    list_image_url = row[2]
    product_url    = row[3]

    driver.get(product_url)
    time.sleep(3)
    # driver.implicitly_wait(10)

    # 처음에 나오는 모달창 취소
    if i == COUNT:
        element_choose_your_location_cancel = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/section/div/img')
        element_choose_your_location_cancel.click()
        driver.implicitly_wait(IMPLICIT_WAIT)

        # 로그인
        element_menu_login = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/nav/div/div[2]/ul/li[6]/a')
        driver.execute_script("arguments[0].click();", element_menu_login)
        # element_menu_login.click()
        time.sleep(3)

        element_input_email    = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[4]/div/form/div/div/div[1]/div[1]/input')
        element_input_password = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[4]/div/form/div/div/div[1]/div[2]/div/input')
        element_input_email.send_keys('choonghee.lee@hotmail.com')
        element_input_password.send_keys('Dudtkwjd1!')

        element_button_sign_in = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[4]/div/form/div/div/div[3]/button/div[1]')
        driver.execute_script("arguments[0].click();", element_button_sign_in)
        time.sleep(5)
        
    try:
        element_press_and_hold = driver.find_element_by_xpath('/html/body/section/div[3]/div/div[1]/iframe')
        action_chains.context_click(element_press_and_hold)
        time.sleep(4)
    except NoSuchElementException:
        pass

    # 상품명
    try:
        element_title = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[1]/div/h1')
        title         = element_title.text
    except NoSuchElementException:
        title = None
    # driver.implicitly_wait(2)
    # time.sleep(1)
    
    # ticker
    try:
        element_ticker = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[1]/div/small/div[2]/span')
        ticker         = element_ticker.text
    except NoSuchElementException:
        ticker = None
    # driver.implicitly_wait(2)
    # time.sleep(1)
    
    # style
    try:
        element_style = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[4]/div[1]/div[1]/span')
        style         = element_style.text
    except NoSuchElementException:
        style = None
    # driver.implicitly_wait(2)
    # time.sleep(1)

    # colorway
    try:
        element_colorway = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[4]/div[1]/div[2]/span')
        colorway         = element_colorway.text
    except NoSuchElementException:
        colorway = None
    # driver.implicitly_wait(2)
    # time.sleep(1)

    # retail price
    try:
        element_retail_price = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[4]/div[1]/div[3]/span')
        retail_price         = element_retail_price.text[1:]
    except NoSuchElementException:
        retail_price = None
    # driver.implicitly_wait(2)
    # time.sleep(1)

    # release date
    try:
        element_release_date = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[4]/div[1]/div[4]/span')
        release_date         = element_release_date.text
    except NoSuchElementException:
        release_date = None
    # driver.implicitly_wait(2)
    # time.sleep(1)

    # description
    try:
        element_description = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[4]/div[2]/p')
        description         = element_description.text
    except NoSuchElementException:
        description = None
    # driver.implicitly_wait(2)
    # time.sleep(1)

    # size
    sizes = []
    try:
        element_button_size = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div[1]/button")
        driver.execute_script("arguments[0].click();", element_button_size)
        # element_button_size.send_keys(Keys.ENTER)
        time.sleep(2)
        element_ul_sizes      = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/ul")
        list_element_li_sizes = element_ul_sizes.find_elements_by_tag_name('li')
        for i, element_li_size in enumerate(list_element_li_sizes):
            if i == 0:
                continue
            
            element_size = element_li_size.find_element_by_xpath(".//div/div[1]")
            size         = element_size.text
            # size         = size_text.split(" ")[1]
            sizes.append(size)
    except NoSuchElementException:
        pass
    
    # sales
    sales = []
    try:
        element_sales = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[3]/a")
        driver.execute_script("arguments[0].click();", element_sales)
        time.sleep(3)

        element_modal_body = driver.find_element_by_class_name("modal-body")
        modal_body_text = element_modal_body.text
        if modal_body_text != "No Sales Available":
            for i in range(1):
                try:
                    element_button_load_more = driver.find_element_by_class_name("button-block")
                    driver.implicitly_wait(2)
                    element_button_load_more.send_keys(Keys.ENTER)
                    time.sleep(1)
                except NoSuchElementException:
                    break

            try:
                element_table = driver.find_element_by_id("480")
                element_tbody = element_table.find_element_by_tag_name("tbody")
                list_element_trs = element_tbody.find_elements_by_tag_name('tr')
                for element_tr in list_element_trs:
                    sale = []
                    list_element_tds = element_tr.find_elements_by_tag_name('td')
                    for i, element_td in enumerate(list_element_tds):
                        if i == 3:
                            text = element_td.text[1:]
                        else:
                            text = element_td.text
                        sale.append(text)
                    sales.append(sale)
            except NoSuchElementException:
                pass

        element_button_close = driver.find_element_by_class_name("close")
        driver.execute_script("arguments[0].click();", element_button_close)
    except NoSuchElementException:
                pass
    # element_button_close.click()
    time.sleep(1)
    
    # asks 
    asks = []
    try:
        element_asks = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[3]/a[@data-testid='product-viewallasks']")
        driver.execute_script("arguments[0].click();", element_asks)
        # try: 
        #     element_asks.click()
        # except ElementClickInterceptedException:

        time.sleep(3)

        element_modal_body = driver.find_element_by_class_name("modal-body")
        modal_body_text = element_modal_body.text
        if modal_body_text != "No Asks Available":
            for i in range(1):
                try:
                    element_button_load_more = driver.find_element_by_class_name("button-block")
                    driver.implicitly_wait(2)
                    driver.execute_script("arguments[0].click();", element_button_load_more)
                    # element_button_load_more.send_keys(Keys.ENTER)
                    time.sleep(1)
                except NoSuchElementException:
                    break

            try:
                element_table = driver.find_element_by_id("400")
                element_tbody = element_table.find_element_by_tag_name("tbody")
                list_element_trs = element_tbody.find_elements_by_tag_name('tr')
                for element_tr in list_element_trs:
                    ask = []
                    list_element_tds = element_tr.find_elements_by_tag_name('td')
                    for i, element_td in enumerate(list_element_tds):
                        if i == 1:
                            text = element_td.text[1:]
                        else:
                            text = element_td.text
                        ask.append(text)
                    asks.append(ask)
            except NoSuchElementException:
                pass
                
            # element_tbody = element_table.find_element_by_tag_name("tbody")
            # list_element_trs = element_tbody.find_elements_by_tag_name('tr')
            # for element_tr in list_element_trs:
            #     ask = []
            #     list_element_tds = element_tr.find_elements_by_tag_name('td')
            #     for i, element_td in enumerate(list_element_tds):
            #         if i == 1:
            #             text = element_td.text[1:]
            #         else:
            #             text = element_td.text
            #         ask.append(text)
            #     asks.append(ask)

        element_button_close = driver.find_element_by_class_name("close")
        driver.execute_script("arguments[0].click();", element_button_close)
        # element_button_close.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # bids 
    bids = []
    # /html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[3]/a
    # /html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[3]
    try:
        element_bids = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[3]/a")
        driver.execute_script("arguments[0].click();", element_bids)
        time.sleep(3)

        element_modal_body = driver.find_element_by_class_name("modal-body")
        modal_body_text = element_modal_body.text
        if modal_body_text != "No Bids Available":
            for i in range(1):
                try:
                    element_button_load_more = driver.find_element_by_class_name("button-block")
                    driver.implicitly_wait(2)
                    driver.execute_script("arguments[0].click();", element_button_load_more)
                    # element_button_load_more.send_keys(Keys.ENTER)
                    time.sleep(1)
                except NoSuchElementException:
                    break

            try:
                element_table = driver.find_element_by_id("300")
                element_tbody = element_table.find_element_by_tag_name("tbody")
                list_element_trs = element_tbody.find_elements_by_tag_name('tr')
                for element_tr in list_element_trs:
                    bid = []
                    list_element_tds = element_tr.find_elements_by_tag_name('td')
                    for i, element_td in enumerate(list_element_tds):
                        if i == 1:
                            text = element_td.text[1:]
                        else:
                            text = element_td.text
                        bid.append(text)
                    bids.append(bid)
            except NoSuchElementException:
                continue
                # pass

        element_button_close = driver.find_element_by_class_name("close")
        driver.execute_script("arguments[0].click();", element_button_close)
        time.sleep(2)
    except NoSuchElementException:
        pass
    # driver.implicitly_wait(2)
    # element_button_close.click()

    # 이미지
    image_urls = []
    try:
        # /html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[4]
        element_image_slider = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[4]")
        time.sleep(3)
        while True:
            element_product_image = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/img")
            image_url             = element_product_image.get_attribute('src')
            image_urls.append(image_url)
            
            style_slider = element_image_slider.get_attribute('style')
            left  = style_slider.split(';')[0].split(':')[1].strip()
            if left == '100%':
                break
            # driver.execute_script("arguments[0].click();", element_image_slider)
            element_image_slider.send_keys(Keys.ARROW_RIGHT)
            driver.implicitly_wait(2)
    except NoSuchElementException:
            element_product_image = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[2]/div[1]/img")
            image_url             = element_product_image.get_attribute('src')
            image_urls.append(image_url)
    except ElementNotInteractableException:
        pass
    
    row = (jordan_number, size_type, list_image_url, title, ticker, style, colorway, retail_price, release_date, description, image_urls, sizes, sales, asks, bids)
    csv_writer.writerow(row)

csv_urls_open.close()
csv_details_open.close()
driver.quit()