#  始從網路爬取最新書籍資料...慢些但執行沒問題
import sys
#  這行是把 Python 的內建模組 sys 匯入（import）：「系統(System)模組」
#  typing 模組是 Python 提供的，用來說明「這個變數是 List（列表）型態／這個是 Dict（字典）型態／裡面元素是什麼型態」等等。
#  List, Dict, Any 分別代表「列表」、「字典」和「任意型態」，https://docs.python.org/zh-tw/3.13/library/typing.html
from typing import List, Dict, Any
# 從 database.py 這個模組檔案中，匯入 save_books、query_by_title、query_by_author 這三個函式
from database import save_books, query_by_title, query_by_author
# 從 scraper.py 這個模組檔案中，匯入 scrape_llm_books 這個函式
from scraper import scrape_llm_books
#  1.顯示主選單# 回傳有用的資料，只是做一些動作（像印選單、操作狀態、處理輸入／輸出）
def main_menu():
    book = "LLM"
    print(f"----- 博客來 {book} 書籍管理系統 -----") # f-string
    #  print("----- 博客來 LLM 書籍管理系統 -----")
    print("1. 更新書籍資料庫") #  印出選單標題，讓使用者知道「這是 LLM 書籍管理系統」
    print("2. 查詢書籍")
    print("3. 離開系統")
    print("---------------------------------")
    print("請選擇操作選項 (1-3):", end=" ")

#  2.從網路爬取書籍資料 + 存入資料庫
def update_database():
    print("開始從網路爬取最新書籍資料...")
    book_list = scrape_llm_books()# 爬最新書完（呼叫 scrape_llm_books()）再存進資料庫。
    # 計算從網路爬取到多少筆資料。這是給使用者一個回報
    total_count = len(book_list) 
    # 呼叫 database.py 裡的 save_books 函式，把爬到的資料存入資
    new_count = save_books(book_list)
    print(
        f"資料庫更新完成！共爬取 {total_count} 筆資料，新增了 {new_count} 筆新書記錄。"
    )
    print(" ")
#  列印查詢結果。
def print_results(results: List[Dict[str, Any]]) :
#  如果結果列表是空的（沒有資料）
    if not results:
        print("查無資料。")
        return

    print(f"\n====================")
    for book in results: #  迴圈處理每本書
        print(f"書名：{book['title']}")
        print(f"作者：{book['author']}")
        print(f"價格：{book['price']}")
        print("---")
    print("====================\n")

#  3處理使用者查詢書籍（依書名或作者）流程。
def query_books():

    while True:
        print("\n--- 查詢書籍 ---")
        print("a. 依書名查詢")
        print("b. 依作者查詢")
        print("c. 返回主選單")
        print("---------------")
        choice = input("請選擇查詢方式 (a-c): ").strip().lower() # .lower() 轉為小寫用 .strip() 就可以把 " a" 或 "a " 變成 "a"，讓後續的判斷比較乾淨、比較不容易出錯。

        if choice == "a":
            key = input("請輸入書名關鍵字: ").strip()  
            #  https://www.geeksforgeeks.org/python/python-string-strip/
            results = query_by_title(key)
            print_results(results)
        elif choice == "b":
            key = input("請輸入作者關鍵字: ").strip()
            results = query_by_author(key)
            print_results(results)
        elif choice == "c":
            print(" ")
            return
        else:
            print("無效選項，請重新輸入。")
           

#  主程式：主選單迴圈，直到使用者選擇離開。
def main():
    
    while True:
        main_menu()
        choice = input().strip()
        if choice == "1":
            update_database()
        elif choice == "2":
            query_books()
        elif choice == "3":
            print("感謝使用，系統已退出。")
            sys.exit(0)
        else:
            print("無效選項，請重新輸入。")
            print(" ")

#  https://pypi.org/project/main-function/?utm_source #  函式會被呼叫，整個選單流程開始
if __name__ == "__main__":
    main()

