# Author: Shaoyu Hsu (aka Joanna Hsu)
#
from tkinter import *

import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
import sqlite3
from sqlite3 import Error
import time


def start_running():
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def addLine(conn, tablename, results,keywords):
        sql = f'INSERT INTO "{tablename}" (title,company,"job level",location,"company info",detail,'
        for kw in keywords:
            sql = sql + f'"{kw}",'
        sql = sql[:-1] + ') VALUES(?,?,?,?,?,?,'
        for i in range(len(keywords)):
            sql = sql + f'?,'
        sql = sql[:-1] + ')'
        cur = conn.cursor()
        results = sep(results)
        cur.execute(sql, results)
        conn.commit()
        return cur.lastrowid

    def sep(results):
        skills = results[-1]
        results = results[:-1]
        for a in skills.keys():
            results.append(skills[a])
        return results

    def getInfo(kws, overview):
        result = {}
        for keywords in kws:
            s = ''
            for line in overview.split('.'):
                if keywords.lower() in line.lower():
                    s = s + line + '\n\n'
            result[keywords] = s
        return result

    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def parse(driver, url, keywords):
        title_list = []
        location_list = []
        companyinfo_list = []
        company_list = []
        level_list = []
        detail_list = []
        kw_list = []
        driver.get(url)
        left = driver.find_element(By.CSS_SELECTOR, '#main > div > section.scaffold-layout__list>div')
        for i in range(1, 3):
            driver.execute_script("arguments[0].scrollTop = arguments[1]", left, 3000)
            driver.find_element(By.CSS_SELECTOR,
                                f'#main > div > section.scaffold-layout__list > div > ul>li:nth-child({i})').click()
            time.sleep(2)
            try:
                title = (driver.find_element(By.CSS_SELECTOR,
                                             "#main > div > section.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.job-view-layout.jobs-details>div>div>div>div>div.relative>div>a>h2").get_attribute(
                    'textContent')).lstrip()
            except:
                title = 'N/A'
            try:
                company = (driver.find_element(By.CSS_SELECTOR,
                                               "#main > div > section.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.job-view-layout.jobs-details>div>div>div>div>div.relative>div>div>span>span>a").get_attribute(
                    'textContent')).lstrip()
            except:
                company = 'N/A'
            try:
                level = ((driver.find_element(By.CSS_SELECTOR,
                                              "#main > div > section.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.job-view-layout.jobs-details>div>div>div>div>div.relative>div>div.mt5.mb2>ul>li>span").get_attribute(
                    'textContent')).split(' · ')[1]).lstrip()
            except:
                level = 'N/A'
            try:
                location = (driver.find_element(By.CSS_SELECTOR,
                                                "#main > div > section.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.job-view-layout.jobs-details>div>div>div>div>div.relative>div>div>span>span.jobs-unified-top-card__bullet").get_attribute(
                    'textContent')).lstrip()
            except:
                location = 'N/A'
            try:
                company_info = (driver.find_element(By.CSS_SELECTOR,
                                                    "#main > div > section.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.job-view-layout.jobs-details>div>div>div>div>div.relative>div>div.mt5.mb2>ul>li.jobs-unified-top-card__job-insight:nth-child(2)>span").get_attribute(
                    'textContent')).lstrip()
            except:
                company_info = 'N/A'
            try:
                detail = (driver.find_element(By.CSS_SELECTOR, "#job-details").get_attribute('textContent')).lstrip()
            except:
                detail = 'N/A'
            kw_output = getInfo(keywords, detail)

            title_list.append(title)
            location_list.append(location)
            companyinfo_list.append(company_info)
            company_list.append(company)
            level_list.append(level)
            detail_list.append(detail)
            kw_list.append(kw_output)
        return title_list, location_list, companyinfo_list, detail_list, company_list, level_list, kw_list

    def getkw(strings):
        return strings.split(',')

    database = "linkedIn.db"
    sql_create_table=f'CREATE TABLE IF NOT EXISTS "{table.get()}" ("title" text,"company" text,"job level" text,"location" text,"company info" text,"detail" text)'
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_table)
    else:
        print("Error! cannot create the database connection.")
    title_list = []
    company_list = []
    level_list = []
    location_list = []
    companyinfo_list = []
    detail_list = []
    op = webdriver.ChromeOptions()
    #op.add_argument('headless')
    chromedriver = r'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chromedriver, options=op)
    start = 0
    driver.get("https://linkedin.com/uas/login")
    driver.maximize_window()
    time.sleep(1)
    username = driver.find_element(By.ID,"username")
    username.send_keys('joannahsusy@gmail.com')
    time.sleep(1)
    pword = driver.find_element(By.ID,"password")

    pword.send_keys('H224562418h')
    time.sleep(1)
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(13)
    with conn:
        url=f"https://www.linkedin.com/jobs/search/?currentJobId=3286478083&geoId=90000084&keywords=selenium%20python&location=San%20Francisco%20Bay%20Area&refresh=true&start={start}"
        driver.get(url)
        try:
            whole = driver.find_element(By.CSS_SELECTOR,
                                        'body > div.application-outlet > div.authentication-outlet > div.scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--list-detail.scaffold-layout--reflow.scaffold-layout--has-list-detail.jobs-search-two-pane__layout > div').get_attribute(
                'textContent')

            time.sleep(2)
            while 'No matching jobs found.' not in whole:
                time.sleep(1)
                start = start + 25
                url = f"https://www.linkedin.com/jobs/search/?currentJobId=3286478083&geoId=90000084&keywords=selenium%20python&location=San%20Francisco%20Bay%20Area&refresh=true&start={start}"
                driver.get(url)
                whole = driver.find_element(By.CSS_SELECTOR,
                                            'body > div.application-outlet > div.authentication-outlet > div.scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--list-detail.scaffold-layout--reflow.scaffold-layout--has-list-detail.jobs-search-two-pane__layout > div').get_attribute(
                    'textContent')


                title, location, companyinfo, detail, company, level, kw = parse(driver,url,getkw(keywords.get()))

                title_list = title_list+title
                company_list = company_list+company
                level_list = level_list+level
                location_list = location_list+location
                companyinfo_list = companyinfo_list+companyinfo
                detail_list = detail_list+detail
                kw_list = kw_list + kw
            for i in range(len(title_list)):
                addLine(conn,table.get(),[title_list[i], company_list[i], level_list[i], location_list[i], companyinfo_list[i], detail_list[i],kw_list[i]],getkw(keywords.get()))
        except selenium.common.exceptions.NoSuchElementException:
            print('''Need Security Check. Comment out line "op.add_argument('headless')" to do security check manually ''')
            root.destroy()
    try:
        root.destroy()
    except:
        print()

root = Tk()
root.geometry('400x300')
button = Button(root,text='Click',command=lambda :start_running())
button.place(x=140,y=250)


Label(root, text="account").place(x=4,y=10)
acc=Entry(root,width=30)
acc.place(x=140,y=10)

Label(root, text="password").place(x=4,y=40)
pw=Entry(root,width=30)
pw.place(x=140,y=40)

Label(root, text="job title").place(x=4,y=70)
job=Entry(root,width=30)
job.place(x=140,y=70)

Label(root, text="location").place(x=4,y=100)
loc=Entry(root,width=30)
loc.place(x=140,y=100)

Label(root, text="database table name").place(x=4,y=130)
table=Entry(root,width=30)
table.place(x=140,y=130)

Label(root, text="skillsets").place(x=4,y=160)
keywords=Entry(root,width=40)
keywords.place(x=140,y=160)

root.mainloop()
