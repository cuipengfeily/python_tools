from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# 基金网址
fund_url = "http://fundf10.eastmoney.com/jjjz_008593.html"

# 初始化web开发驱动
print("start Edge browser driver")
# driver = webdriver.Firefox()
driver = webdriver.Edge()
print("start ok...")
driver.get(fund_url)
# 打印浏览器标题
print(driver.title)

# 保存每日基金净值数据
# 每一条都是这种格式的字符串：2023-12-29,1.0620,1.0620,0.30%,开放申购,开放赎回,
itmes=[]


# 获取当前点击时间点：2021-08-29 16:00:00.000000
start_time = time.time()

# 获取当前网页上的基金数据，然后点击下一页，再获取下一页的数据，直到最后一页
# 你可以根据实际情况调整循环次数，例如：只获取前10页的数据，则可以在while循环中加入一个计数器，当计数器达到10时，退出循环
want_page = 5 # 只抓取5页数据
toal_page = -1 # 总页数,在第一次循环中获取
current_page = 0 # 当前页
while True:
    current_page += 1
    if current_page > want_page:
        break

    # 找到包含基金净值表格的网页元素
    # <div id="jztable">
    elem = driver.find_element(By.ID, "jztable")

    # 定位到table元素
    # <table class="w782 comm lsjz">
    table = elem.find_element(By.TAG_NAME, "table")

    # 获取所有行和列的数据
    # <tbody>
    # <tr class="">
    #     <td>2023-08-25</td>
    #     <td class="tor bold">1.1357        </td>
    #     <td class="tor bold">1.1357</td>
    #     <td class="tor bold grn">-0.25%</td>
    #     <td>开放申购</td>
    #     <td>开放赎回</td>
    #     <td class="red unbold"></td>
    # </tr>
    # <tr class="">
    #     <td>2023-08-24</td>
    #     <td class="tor bold">1.1385        </td>
    #     <td class="tor bold">1.1385</td>
    #     <td class="tor bold red">0.61%</td>        
    #     <td>开放申购</td>
    #     <td>开放赎回</td>
    #     <td class="red unbold"></td>
    # </tr>
    # ...
    # </tbody>
    rows = table.find_element(By.TAG_NAME, "tbody")

    # 每个tbody中含有20行（20天）的基金数据，每条数据都在一个tr中
    tr = rows.find_elements(By.TAG_NAME, "tr") # print(type(tr), len(tr))
    for row in tr:
        # print("tagname: ", row.tag_name, row.size)
        # 20行数据：每一行包含7列数据，每一列都在一个td中，分别是日期、单位净值、累计净值、日增长率、申购状态、赎回状态、分红送配
        columns = row.find_elements(By.TAG_NAME, "td")
        # 将每行数据用逗号隔开格式化，按照这种格式保存：2023-12-29,1.0620,1.0620,0.30%,开放申购,开放赎回,
        col_content = ""
        for column in columns:
            if col_content != "": 
                col_content+=","
            col_content = col_content + column.text
        # print(col_content)
        # 2023-12-29,1.0620,1.0620,0.30%,开放申购,开放赎回,
        itmes.append(col_content)
    
    # print(elem)
    # <selenium.webdriver.remote.webelement.WebElement (session="2afb5d480128a5ea71652754984c8ebf", element="985430FD19D38B71406F6E99B4D4DC13_element_46")>
    
    # 查找下一页的按钮
    # next_button = driver.find_element(By.XPATH, '//a[@tagname="label"][text()="下一页"]')
    # <div class="pagebtns" style="left: 203px;">
    #     <label class="end" value="1">上一页</label>
    #     <label value="1" class="cur">1</label>
    #     <label value="2">2</label>
    #     <label value="3">3</label>
    #     <label value="4">4</label>
    #     <label value="5">5</label>
    #     <span>...</span>
    #     <label value="45">45</label>
    #     <label value="2">下一页</label>
    #     <span>转到</span>
    #     <input type="text" class="pnum">
    #     <span>页</span>
    #     <input type="button" class="pgo">
    # </div>
    page_tools = driver.find_element(By.CLASS_NAME, 'pagebtns')
    labels = page_tools.find_elements(By.TAG_NAME, 'label')
    # 找到下一页的按钮位置和总页数
    last_label = ""
    for label in labels:
        # print(label.text)
        if label.text == '下一页':
            next_button = label
            break
        last_label = label.text
    if toal_page <= 0:
        toal_page = int(last_label)
    # next_button = page_button.find_element(By.XPATH, "/label[@text='下一页']")
    # next_button = driver.find_element(By.XPATH, "//label[1]")
    # print(next_button.get_attribute('for'))
    # print("enable: ", next_button.is_enabled())
    next_button_class = next_button.get_attribute('class')
    if next_button_class == 'end':
        value = next_button.get_attribute('value')
        # print("last page value: ", value)
            
        break
    
    # print(next_button.text)
    # 模拟点击下一页按钮
    next_button.click()
    # 等待一秒钟，等待页面加载完成，这里需要根据实际情况调整等待时间
    time.sleep(1)
    # 获取点击完成时间点：2021-08-29 16:00:01.000000
    loaded_time = time.time()
    # 打印总消耗时间
    elapsed_time = loaded_time - start_time
    print("总页数：", toal_page, "当前页：", current_page, "想抓取的页数：", want_page, "，时间过去了：", elapsed_time, "秒")

# 将数据保存到文件中
with open('simp.csv', 'w', encoding='utf-8') as f:
    f.write('日期,单位净值,累计净值,日增长率,申购状态,赎回状态,分红送配\n')
    for item in itmes:
        f.write(item)
        f.write('\n')

# print(next_button)
# 如果下一页的按钮不可用，则退出循环
# if 'disabled' in next_button.get_attribute('class'):
#     break
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
driver.close()