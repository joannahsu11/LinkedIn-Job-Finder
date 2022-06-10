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

def addLine(conn, task):
    sql = ''' INSERT INTO tasks(title,name,location,field,mode,size,job,python,SQL)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def parse(email,pw,kw,l,driverfile):
    title_list=[]
    location_list=[]
    size_list=[]
    mode_list=[]
    name_list=[]
    detail_list=[]
    field_list=[]
    op= webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path=driverfile, options=op)
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

    time.sleep(random.randint(3,5))
    driver.get('https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=data%20engineer&location=United%20States')
    time.sleep(5)
    left=driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div')")
    driver.execute_script("arguments[0].scrollTop = arguments[1]", left, 3000)
    time.sleep(5)
    lastpage_i=driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > section>div>ul>li').length")
    t=driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > section>div>ul>li')[{lastpage_i-1}].querySelector('button')").get_attribute('textContent')
    page=int(t.replace(' ',''))+1


    #for p in range(page):
    for p in range(2):
        n=25*p
        if n==0:
            n=1
        driver.get(f"https://www.linkedin.com/jobs/search/?geoId=103644278&keywords={str(kw).replace(' ','%20')}&location={str(l.title()).replace(' ','%20')}&start={n}")
        time.sleep(3)
        for i in range(0,25):
            # try:
            driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__left-rail > div > div > ul>li')[{i}].querySelector('div>div').click()")
            time.sleep(3)
            try:
                title = driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>a')").text
            except:
                title='N/A'
            try:
                name = driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>div.jobs-unified-top-card__primary-description>span')[0].querySelector('span')").text
            except:
                name='N/A'
            try:
                location = driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>div.jobs-unified-top-card__primary-description>span')[0].querySelectorAll('span')[1]").text
            except:
                location='N/A'
            try:
                mode = driver.execute_script(f"return document.querySelectorAll('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane>div.jobs-unified-top-card__primary-description>span')[0].querySelectorAll('span')[2]").text
            except:
                mode='N/A'
            company = driver.execute_script(f"return document.querySelector('body > div.application-outlet > div.authentication-outlet > div.job-search-ext > div.jobs-search-two-pane__wrapper > div > section.jobs-search__right-rail > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.relative > div.jobs-unified-top-card__content--two-pane > div.mt5.mb2 > ul > li:nth-child(2) > span')").text
            try:
                size=company.split(' ')[0]
            except:
                size='N/A'
            try:
                field=company.split(' · ')[1]
            except:
                field='N/A'
            print(title,name,location,mode,size,field)
            detail = (driver.execute_script(f"return document.querySelector('#job-details > span')").text)
            title_list.append(title)
            location_list.append(location)
            size_list.append(size)
            name_list.append(name)
            mode_list.append(mode)
            detail_list.append(detail)
            field_list.append(field)
            time.sleep(2)
        time.sleep(5)
    return title_list,location_list,size_list,detail_list,name_list,mode_list,field_list



def main(email,pw,kw,l,driverfile):
    database = r"C:\Users\bb971\Desktop\linkedIn.db"

    sql_create_table = """ CREATE TABLE IF NOT EXISTS tasks (title text,name text,location text,field text,mode text,size text,job text,python text,SQL text); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        title_list,location_list,size_list,detail_list,name_list,mode_list,field_list=parse(email,pw,kw,l,driverfile)
        for i in range(len(title_list)):
            if 'python' in str(detail_list[i]).lower():
                p='v'
            else:
                p=''
            if 'sql' in str(detail_list[i]).lower():
                s = 'v'
            else:
                s=''
            addLine(conn, (title_list[i],name_list[i],location_list[i],field_list[i],mode_list[i],size_list[i],detail_list[i],p,s))


if __name__ == '__main__':
    main('your email','your password','your keywords','location','your chromerdriver directory')

