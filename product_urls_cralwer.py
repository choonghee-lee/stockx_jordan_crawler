import csv

from selenium                       import webdriver
from selenium.common.exceptions     import NoSuchElementException
from selenium.webdriver.common.keys import Keys

TARGET_URL_LIST   = "https://stockx.com/sneakers"
CSV_FILENAME      = "stockx_product_urls.csv"
IMPLICIT_WAIT     = 5

# .csv 파일 열기
csv_open   = open(CSV_FILENAME, "w+", encoding="utf-8")
csv_writer = csv.writer(csv_open)

# 타겟 url 접속
driver = webdriver.Chrome()
driver.get(TARGET_URL_LIST)
driver.implicitly_wait(IMPLICIT_WAIT)

# 처음에 나오는 모달창 취소
element_choose_your_location_cancel = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/section/div/img')
element_choose_your_location_cancel.click()
driver.implicitly_wait(IMPLICIT_WAIT)

# 카테고리 조던 선택
element_category_jordan = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/div/div[3]/div[2]")
element_category_jordan.click()

# 조던 1~5 까지 선택
for i in range(2, 7):
    checkbox_jordan_xpath   = f"/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/div/div[3]/div[2]/div[2]/div[{i}]/div/label"
    element_checkbox_jordan = driver.find_element_by_xpath(checkbox_jordan_xpath)
    jordan_number = element_checkbox_jordan.text
    element_checkbox_jordan.click()
    driver.implicitly_wait(IMPLICIT_WAIT)

    # 사이즈 타입 (men, women, child, preschool, infant, toddler) 선택
    for j in range(1, 7):
        checkbox_size_type_xpath = f"/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[1]/div/div[4]/div[2]/div[{j}]/div/div/label"
        element_checkbox_size_type = driver.find_element_by_xpath(checkbox_size_type_xpath)
        size_type = element_checkbox_size_type.text
        element_checkbox_size_type.click()
        driver.implicitly_wait(IMPLICIT_WAIT)

        # 페이지네이션 돌기
        k = 1
        base_url = driver.current_url
        while True:
                target_url = base_url + f"&page={k}"
                driver.get(target_url)
                driver.implicitly_wait(IMPLICIT_WAIT)

                # 상품이 없다는 안내 문구가 있는 페이지면 break
                try:
                        element_suggest_product = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/a")
                        break
                except NoSuchElementException:
                        pass

                # 신발 상품 url 저장
                list_element_product_links = driver.find_elements_by_xpath('//div[contains(@class, "tile") and contains(@class, "css-1bonzt1") and contains(@class, "e1yt6rrx0")]/a')
                for element_product_link in list_element_product_links:
                        element_product_link.send_keys(Keys.TAB)
                        driver.implicitly_wait(2)
                        element_product_image = element_product_link.find_element_by_xpath('.//div/img')
                        image_src             = element_product_image.get_attribute("src")
                        href                  = element_product_link.get_attribute("href")
                        row                   = (jordan_number, size_type, image_src, href,)
                        csv_writer.writerow(row)
                k+=1
        
# 리소스 해제
csv_open.close()
driver.quit()
