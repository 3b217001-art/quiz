# 在在爬取3頁慢些
import re
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 測試用的
# URL = "https://www.books.com.tw/"
# 使用 Chrome 的 WebDriver
# browser = webdriver.Chrome()
# 進入網站並搜尋關鍵字
# browser.get(URL)
# search = browser.find_element(By.XPATH, '//*[@id="key"]') 用 XPATH 找到搜尋框
# search.send_keys("LLM")
# search.send_keys(Keys.RETURN)
# time.sleep(1)
# 篩選書籍分類
# browser.find_element(By.XPATH, '//*[@id="filter_cat_1"]/label[2]/span').click()
# time.sleep(2)
# 會回傳一個書籍資料的清單，每筆資料是一個字典（dict）
# 主函式：scrape_llm_books()

def scrape_llm_books() :

    base_url = "https://www.books.com.tw/"

    # 1.啟用 Headless 模式（無視窗）
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    # 使用新版 headless 模式
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    #  設定視窗大小（即使無視窗也模擬這個大小）
    chrome_options.add_argument("--window-size=1920,1080")

    # 啟動 Chrome 瀏覽器的 WebDriver。browser 是操作這個瀏覽器的物件
    service = Service()
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # print("開啟博客來首頁中...")
        browser.get(base_url)
        # 找到搜尋框並輸入 LLM
        # 用 XPATH 找到搜尋框
        search_input = browser.find_element(By.XPATH, '//*[@id="key"]') 
        search_input.send_keys("LLM")
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # 選擇「書籍分類」切換到【中文書】分類 (cat=1)
        try:
            category_button = WebDriverWait(browser, 5).until( 
                # 顯式等待，等待某個特定條件（按鈕可點）滿足後再點擊
                EC.element_to_be_clickable((By.XPATH, '//*[@id="filter_cat_1"]/label[2]/span'))
            )
            # 點擊元素
            category_button.click()  
            time.sleep(2)
        except Exception:
            print("未能切換到書籍分類，但繼續執行...")
        #  爬取每一頁的書籍資料
        books_data = []
        page_index = 1 
        # 從第 1 頁開始
        max_pages = 3  # 博客來實際有 3 頁
        last_url = browser.current_url
        # page_index 與 max_pages：控制「只抓前 3 頁」避免無限迴圈或太多資料
        print(f"偵測到總共有 {max_pages} 頁。")
        #  主迴圈，每次處理一頁。
        while page_index <= max_pages:
            print(f"正在爬取第 {page_index} / {max_pages} 頁...")

            # 等待書籍清單載入
            WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.table-searchbox div.table-td")
                )
            )
            # 找出頁面上所有符合 CSS 選擇器的元素」，然後把它們放進一個列表 (book_elements)

            book_elements = browser.find_elements(
                By.CSS_SELECTOR, "div.table-searchbox div.table-td"
            )

            #  資料擷取

            for element in book_elements:
                try:
                    # 取得書名與連結
                    title_tag = element.find_element(By.CSS_SELECTOR, "h4 a")
                    title = title_tag.text.strip()
                    link = title_tag.get_attribute("href")
                    if title == "":
                        continue
                except Exception:
                    continue  # 跳過空白或異常的項目

                try:
                    # 取得作者
                    author_tags = element.find_elements(By.CSS_SELECTOR, "p.author a")
                    authors = [a.text.strip() for a in author_tags if a.text.strip()]
                    author = ", ".join(authors) if authors else "N/A"
                except Exception:
                    author = "N/A"

                try:
                    # 取得價格區塊
                    price_li = element.find_element(By.CSS_SELECTOR, "ul.price li")
                    price_text = price_li.text  # 例："優惠價: 79 折, 513 元"
                    # 擷取所有數字，取最後一個（即金額），"優惠價: 79 折, 513 元" → 抓到 ["79", "513"] → 最後取 "513" → 轉成整數 513
                    numbers = re.findall(r"\d+", price_text)
                    price = int(numbers[-1]) if numbers else 0
                except Exception:
                    price = 0

                books_data.append({
                    "title": title,
                    "author": author,
                    "price": price,
                    "link": link,
                })

            # 下一頁判斷
            if page_index >= max_pages:
                # print("已達設定的最大頁數，停止爬取。")
                break

            try:
                next_button = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next"))
                )
                next_button.click()
                time.sleep(2)

                # 確保頁面確實換頁
                current_url = browser.current_url
                if current_url == last_url:
                    print("點擊下一頁後 URL 未改變，跳出迴圈。")
                    break
                last_url = current_url
                #  頁碼往下

                page_index += 1
            except Exception:
                print("未發現可點擊的「下一頁」按鈕，跳出迴圈。")
                break

        print("爬取完成。")
    #    print(f"爬取完成，共擷取 {len(books_data)} 筆資料。")
        return books_data

    finally:
        browser.quit()


# 直接執行時，測試用
if __name__ == "__main__":
    results = scrape_llm_books()
    print(f"總共抓取 {len(results)} 筆書籍資料")
    for idx, book in enumerate(results[:10], start=1):  # 只顯示前10筆
        print(f"{idx}. 書名：{book['title']}／作者：{book['author']}／價格：{book['price']}／連結：{book['link']}")
