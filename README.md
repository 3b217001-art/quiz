# 博客來 LLM 書籍管理系統:

本考試在評估你整合 Selenium 網頁爬蟲 與 SQLite 資料庫管理 的能力。這兩項技術是資料科學與自動化應用的關鍵技能。

# 1.app.py (主程式)
(1).主程式：提供命令列介面，讓使用者可更新書籍資料庫或查詢書籍。

(2).在更新書籍資料庫的開始從網路爬取最新書籍資料…->要等待下才跑出來有一點慢。

# 2.scraper.py (爬蟲功能)


# 3.database.py (資料庫功能)
(1).資料庫模組：負責與 SQLite 資料庫互動。
建立資料庫檔案 books.db（如不存在），建立資料表 llm_books，
並提供「批量新增書籍資料」與「依書名／作者查詢」功能。

# 4.結果
----- 博客來 LLM 書籍管理系統 -----
1. 更新書籍資料庫
2. 查詢書籍
3. 離開系統
---------------------------------
請選擇操作選項 (1-3): 1
開始從網路爬取最新書籍資料...
偵測到總共有 3 頁。
正在爬取第 1 / 3 頁...
正在爬取第 2 / 3 頁...
正在爬取第 3 / 3 頁...
爬取完成。
資料庫更新完成！共爬取 165 筆資料，新增了 152 筆新書記錄。

----- 博客來 LLM 書籍管理系統 -----
1. 更新書籍資料庫
2. 查詢書籍
3. 離開系統
---------------------------------
請選擇操作選項 (1-3): 2

--- 查詢書籍 ---
a. 依書名查詢
b. 依作者查詢
c. 返回主選單
---------------
請選擇查詢方式 (a-c): a
請輸入關鍵字: RAG

====================
書名：LLM最強重武裝：RAG開發應用優化現場直擊
作者：嚴燦平
價格：774
---
書名：比RAG更強：知識增強LLM型應用程式實戰
作者：王文廣
價格：774
---
書名：開源閉源LLM應用：從微調到RAG、Agent完整開發實作
作者：萬俊
價格：695
---
書名：基於大模型的RAG應用開發與優化：構建企業級LLM應用
作者：嚴燦平
價格：834
---
書名：Building AI Agents with LLMs, RAG, and Knowledge Graphs: A practical guide to autonomous and modern AI agents
作者：Gabriele, Iuculano, Raieli, Salvatore
價格：3299
---
書名：Modern Generative AI with ChatGPT and OpenAI Models: Leverage the capabilities of OpenAI’s LLM for productivity and
作者：Alto, Valentina
價格：2749
---
書名：Applied AI for Enterprise Java Development: Leveraging Generative Ai, Llms, and Machine Learning in the Java Enterprise
作者：Alex Soto, Bueno, Eisele, Markus
價格：2508
====================

--- 查詢書籍 ---
a. 依書名查詢
b. 依作者查詢
c. 返回主選單
---------------
請選擇查詢方式 (a-c): a
請輸入關鍵字: www
查無資料。

--- 查詢書籍 ---
a. 依書名查詢
b. 依作者查詢
c. 返回主選單
---------------
請選擇查詢方式 (a-c): b
請輸入關鍵字: Peter

====================
書名：Long-Term Forensic Psychiatric Care: Clinical, Ethical and Legal Challenges
作者：Birgit, Braun, Peter, Völlm
價格：5399
====================

--- 查詢書籍 ---
a. 依書名查詢
b. 依作者查詢
c. 返回主選單
---------------
請選擇查詢方式 (a-c): d
無效選項，請重新輸入。

--- 查詢書籍 ---
a. 依書名查詢
b. 依作者查詢
c. 返回主選單
---------------
請選擇查詢方式 (a-c): c

----- 博客來 LLM 書籍管理系統 -----
1. 更新書籍資料庫
2. 查詢書籍
3. 離開系統
---------------------------------
請選擇操作選項 (1-3): 4
無效選項，請重新輸入。

----- 博客來 LLM 書籍管理系統 -----
1. 更新書籍資料庫
2. 查詢書籍
3. 離開系統
---------------------------------
請選擇操作選項 (1-3): 3
感謝使用，系統已退出。

# 參考資料
1. 目標網址：博客來
定位搜尋框：輸入【LLM】，然後送出
勾選圖書：點選 圖書(165)，讓它打勾，可以看到網址會有變化
取得目前的查詢結果網址：https://search.books.com.tw/search/query/key/LLM/cat/BKA
爬取欄位：
書名 (title)：TEXT
作者 (author)：TEXT
價格 (price)：INTEGER
書籍連結 (link)：TEXT
技術細節：
2. 資料擷取：程式需能正確抓取每一本書的上述四個欄位。
提示 1：所有書籍資訊都包含在 div.table-searchbox 區域中，每一本書是一個 div.table-td 元素。
提示 2：書名和連結在 <h4> 標籤內的 <a> 標籤中。作者資訊在 <p class="author"> 下的 <a> 標籤中，可能有多位作者，請將所有作者名稱合併成一個字串（例如用逗號分隔）。
資料清理：價格欄位可能包含非數字字元，例如 優惠價: <b>79</b> 折, <b>513</b> 元。您必須從中僅擷取出數字 513 並轉換為整數。
分頁處理 (Pagination)：
程式必須能自動化地處理分頁，抓取所有頁面的書籍資料。
請在一個迴圈中，重複尋找並點擊「下一頁」按鈕。
為了確保網頁元素已載入完成，必須使用 WebDriverWait 等待「下一頁」按鈕變為 可點擊狀態 後再進行點擊。
當「下一頁」按鈕的 <a> 標籤不存在時，表示已達最後一頁，迴圈應當終止。（提示：可使用 try-except 結構來判斷元素是否存在）
強固處理：若書籍缺少作者或價格資訊，爬蟲應能優雅地處理這種情況（例如，存入 N/A 或預設值 0），而不是直接崩潰。
效率提升：使用 --headless 模式執行瀏覽器，以加速爬取過程。
3. 資料庫功能 (database.py)
此模組負責所有資料庫的互動。

資料庫檔案：books.db。若檔案不存在，程式應能自動建立。
資料表名稱：llm_books
資料表結構：
標題	欄位名稱	資料型別	條件約束
書籍編號	id	INTEGER	主鍵，自動累加
書名	title	TEXT	不可為空, 唯一值 (UNIQUE)
作者	author	TEXT	
價格	price	INTEGER	
書籍連結	link	TEXT	
提示：
為了避免重複執行爬蟲時寫入重複的書籍資料，請在 llm_books 資料表的 title 欄位上設定 UNIQUE 約束。
資料庫連接需啟用 Row factory，例如：conn.row_factory = sqlite3.Row，可使結果使用欄位名稱（如 row["title"]）的方式存取資料。
新增資料時，請使用 INSERT OR IGNORE INTO ... 語法。這樣當書名已存在時，資料庫會自動忽略該筆新增操作，而不會引發錯誤。
請實作一個函式，接收爬蟲擷取的書籍列表，並將其批量存入資料庫。

