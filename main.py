from selenium import webdriver
import sqlite3
from sqlite3 import Error
import time
import random

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def addLine(conn, tablename,cols,results):
    sql = f'INSERT INTO "{tablename}" ("title","company","job level","location","field","mode","size","job","experience",'
    for name in cols[:-1]:
        sql = sql + f'"{name}",'
    sql = sql + f'"{cols[-1]}") VALUES(?,?,?,?,?,?,?,?,?,'
    for i in cols[:-1]:
        sql = sql + f'?,'
    sql = sql + f'?)'
    cur = conn.cursor()
    cur.execute(sql, results)
    conn.commit()
    return cur.lastrowid

def getKeyword(job,key):
    for i in range(len(job.splitlines())):
        line=str(job.splitlines()[i])
        if key.lower() in line.lower():
            return line
    return ''

def k1_and_k2(job,key1,key2):
    for i in range(len(job.splitlines())):
        line = str(job.splitlines()[i])
        if key1 in line.lower() and key2 in line.lower():
            return line
    return ''

def k1_or_k2(job,key1,key2):
    for i in range(len(job.splitlines())):
        line = str(job.splitlines()[i])
        if key1 in line.lower() or key2 in line.lower():
            return line
    return ''

def parse(email,pw,kw,l,cols):
    title_list=[]
    location_list=[]
    size_list=[]
    mode_list=[]
    company_list=[]
    level_list=[]
    detail_list=[]
    field_list=[]
    experience_list=[]
    op= webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=op)
    driver.get("https://linkedin.com/uas/login")
    driver.set_window_size(1400,1000)
    time.sleep(3)
    username = driver.find_element_by_id("username")
    username.send_keys(email)
    time.sleep(random.randint(3,5))
    pword = driver.find_element_by_id("password")

    pword.send_keys(pw)
    time.sleep(random.randint(3,5))
    driver.find_element_by_xpath("//button[@type='submit']").click()

    time.sleep(13)
    url=f"https://www.linkedin.com/jobs/search/?geoId=103644278&keywords={str(kw).replace(' ','%20')}&location={str(l.title()).replace(' ','%20')}"
    driver.get(url)
    time.sleep(5)
    left=driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div')")
    driver.execute_script("arguments[0].scrollTop = arguments[1]", left, 3000)
    time.sleep(5)
    lastpage_i=driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > section>div>ul>li').length")
    t=driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > section>div>ul>li')[{lastpage_i-1}].querySelector('button')").get_attribute('textContent')
    page=int(t.replace(' ',''))+1

    print(page)
    allskills_dict={}
    for c in cols:
        allskills_dict[c]=[]
    #for p in range(page):
    for p in range(5):
        print(f'now on page {p+1}')
        n=25*p
        if n==0:
            n=1
        driver.get(url)
        time.sleep(3)
        for i in range(0,25):
            try:
                driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > ul>li')[{i}].querySelector('div>div').click()")
                time.sleep(3)
                try:
                    title = driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>a')").text
                except:
                    title='N/A'
                try:
                    company = driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>div.jobs-unified-top-card__primary-description>span')[0].querySelector('span')").text
                except:
                    company='N/A'
                try:
                    level = driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane > div.mt5.mb2 > ul > li:nth-child(1) > span')").text
                except:
                    level='N/A'
                try:
                    location = driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>div.jobs-unified-top-card__primary-description>span')[0].querySelectorAll('span')[1]").text
                except:
                    location='N/A'
                try:
                    mode = driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>div.jobs-unified-top-card__primary-description>span')[0].querySelectorAll('span')[2]").text
                except:
                    mode='N/A'
                company_info = driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane > div.mt5.mb2 > ul > li:nth-child(2) > span')").text
                try:
                    size=company_info.split(' ')[0]
                except:
                    size='N/A'
                try:
                    field=company_info.split(' · ')[1]
                except:
                    field='N/A'
                print(title,company,level,location,field,mode,size)
                detail = (driver.execute_script(f"return document.querySelector('#job-details > span')").text)
                title_list.append(title)
                location_list.append(location)
                size_list.append(size)
                company_list.append(company)
                level_list.append(level)
                mode_list.append(mode)
                detail_list.append(detail)
                field_list.append(field)
                experience_list.append(k1_and_k2(detail,'experience','year'))
                for col in cols:
                    allskills_dict[col]=allskills_dict[col]+[getKeyword(detail,col)]
                time.sleep(2)
            except:
                title_list.append('')
                location_list.append('')
                size_list.append('')
                level_list.append('')
                company_list.append('')
                mode_list.append('')
                detail_list.append('')
                field_list.append('')
                experience_list.append('')
                for col in cols:
                    allskills_dict[col]=allskills_dict[col]+['']

        time.sleep(2)
    return title_list,location_list,size_list,detail_list,company_list,level_list,mode_list,field_list,experience_list,allskills_dict



def main(email,pw,kw,l,dbtable,skillsets):
    database = "linkedIn.db"

    sql_create_table = f'CREATE TABLE IF NOT EXISTS "{dbtable}" ("title" text,"company" text,"job level" text,"location" text,"field" text,"mode" text,"size" text,"job" text,"experience" text,'
    for name in skillsets[:-1]:
        sql_create_table = sql_create_table + f'"{name}" text,'
    sql_create_table = sql_create_table + f'"{skillsets[-1]}" text)'
    print(sql_create_table)
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        title_list,location_list,size_list,detail_list,company_list,level_list,mode_list,field_list,experience_list,skills_dict=parse(email,pw,kw,l,skillsets)
        for i in range(len(title_list)):
            mytuple = (title_list[i], company_list[i], level_list[i], location_list[i], field_list[i], mode_list[i],
                       size_list[i], detail_list[i], experience_list[i])
            for s in skills_dict:
                mytuple = mytuple + (skills_dict[s][i],)
            addLine(conn, dbtable,skillsets,mytuple)


if __name__ == '__main__':
    main('your linkedin account','password','keyword youd like to search','location','table name in database',["skill1","skill2","..."])

