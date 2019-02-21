import requests
from bs4 import BeautifulSoup #크롤링
from selenium import webdriver #웹 자동화 프로그램
from time import sleep
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
####크롬드라이버 사용
driver = webdriver.Chrome('D:\\chromedriver') 
driver.implicitly_wait(3) 
data_list_p = []
data_list_naver = []
data_list_naver2 = []
data_list_naver3 = []

a = 1
print ("1. google 검색")
print ("2. naver 검색")
print ("3. URL 입력")

num = int(input("숫자를 입력하시오 : "))


if num == 1:
    print("google")
    driver.get ("http://google.com")
    keyword = str(input("크롤링할 문구를 입력하시오 : "))
    #구글 검색창 입력
    elem = driver.find_element_by_name("q")
    elem.send_keys(keyword)
    elem.submit()

    #검색 결과 1부터 5까지 이동
    for i in range(1):
        driver.find_element_by_xpath('//*[@id="rso"]/div/div/div['+ str(i+1) +']/div/div/div[1]/a[1]/h3').click() 
        url = driver.current_url
        res = requests.get(url)
        res.encoding = res.apparent_encoding #인코딩
        html = res.text
        soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')
        tag = str(input("tag : "))
        data_p = soup.find_all(tag)
        for data in data_p:
            data_list_p.append(data.get_text().strip().replace('  ','').replace('\n',''))
            print (data.text.strip().replace('  ','').replace('\n','')+'\n'+ '=========================')
        driver.back()  
        
    driver.close

    file = open('test.txt','w', encoding='utf-8')
    for data_p2 in data_list_p:
        file.write(data_p2 + '\n')
    file.close()    



###################네이버 검색

if num == 2:

    a = 0   #검색 시간을 위한 변수 설정
    i = 8   #페이지당 링크를 접속하기 위한 변수
    n = 0   #페이지당 링크 수의 확인을 위한 변수
    m = 0   #검색결과 페이지 수의 확인을 위한 변수
    j = 0
    start = time.time()  #시간 측정 시작
    print("네이버 지식인")  
    #구글 드라이버를 통해 네이버 지식인 접속
    driver.get ("https://kin.naver.com/index.nhn")
    #구글드라이버 name = query로 keyword 값 전송
    keyword = str(input("크롤링할 문구를 입력하시오 : "))
    elem = driver.find_element_by_name("query")
    elem.send_keys(keyword)
    elem.submit()
    #현재 위치의 URL 주소 가져오기
    print (driver.current_url) 
    url = driver.current_url
    #requests요청으로 url 정보를 가져오고 인코딩, text문서로 변환
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    html = res.text
    soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')
    #현재 페이지를 driver hadlese 배열 0으로 설정
    window_before = driver.window_handles[0]
    #sleep(5)
  
    #//*[@id="s_content"]/div[3]/div[2]/a[1]
    ### 현재 페이지의 검색결과 링크의 개수가 몇개인지 파악
    elems = driver.find_elements_by_xpath('.//li[*]/dl/dt/a')

    for elem in elems:
        #print (elem.get_attribute("href"))
        n = n + 1
    print ("한페이지 검색 결과 :  ", n) 
    #//*[@id="s_content"]/div[3]/div[2]/a[2]
    elems2 = driver.find_elements_by_xpath('.//div[3]/div[2]/a')

    for elem2 in elems2:
        #print (elem2.get_attribute("href"))
        m = m + 1
    print ("검색결과 페이지 수 : ", m)  

    while True:

        i = i + 1   
    

        if i <= n:
            driver.find_element_by_xpath('//*[@id="s_content"]/div[3]/ul/li[' +str(i)+ ']/dl/dt/a').click()  
            driver.switch_to.window(driver.window_handles[-1])
            url = driver.current_url
            print (url)
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            html = res.text
            soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')
            if soup.find('i', {'class':'icon icon_check_adopt'}):

                if soup.find('div', {'class':'title'}) is not None:          
                    title = soup.find('div', {'class':'title'})
                   # title.insert(0, "title : ")
                    data_list_naver.append(title.get_text().strip().replace('  ','').replace('\n',''))
                    print ("title ", ":", title.text.strip().replace('  ','').replace('\n',''))
       
                if soup.find('div', {'class':'c-heading__content'}) is not None:
                    contents = soup.find('div', {'class':'c-heading__content'})
                   # contents.insert(0, "content : ")
                    data_list_naver.append(contents.get_text().strip().replace('  ','').replace('\n',''))
                    print ("contnet : ", contents.text.strip().replace('  ','').replace('\n',''))
                    print ('\n')            
                   
                if soup.find('div', {'class':'_endContentsText c-heading-answer__content-user'}) is not None:            
                    print ("=================================채택된 답변==================================")
                    solution = soup.find('div', {'class':'_endContentsText c-heading-answer__content-user'})
                   # solution.insert(0, "solution : ")
                    data_list_naver.append(solution.get_text().strip().replace('  ','').replace('\n',''))
                    print ("solution : ", solution.text.strip().replace('  ','').replace('\n',''))
                    print ('\n')    
               
                #sleep(5)
            
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                # file = open('naver.txt','w', encoding='utf-8')
                # for naver in data_list_naver:
                #     file.write(naver + '\n')  
                # file.close()   

            else :
                #sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0]) 

        elif i > n:
            n = 0
            j = j+1
            driver.find_element_by_xpath('//*[@id="s_content"]/div[3]/div[2]/a[' + str(j)+ ']').click()
            elems = driver.find_elements_by_xpath('.//li[*]/dl/dt/a')
            for elem in elems:
            #print (elem.get_attribute("href"))
                n = n + 1
            print ("한페이지 검색 결과 :  ", n) 
            window_before = driver.window_handles[0]
            #sleep(3)
            i = 0


            if j == m:
                m = 0 
                elems2 = driver.find_elements_by_xpath('.//div[3]/div[2]/a')
                for elem2 in elems2:
                    #print (elem2.get_attribute("href"))
                    m = m + 1
                print ("검색결과 페이지 수 : ", m)     
                j = 1 
      
    print ("검색 결과 수 : ", a)
    end = time.time()
    elapsed = end - start
    print ("검색 결과 시간 : ", elapsed)

if num == 3:
    print("URL")
    url = str(input("url 주소 :"))
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    html = res.text
    soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')

    #사용자가 원하는 tag 입력
    tag = str(input("tag : "))
    data_p = soup.find_all(tag)
    for data in data_p:
        data_list_p.append(data.get_text().strip().replace('  ','').replace('\n',''))
        print (data.text.strip().replace('  ','').replace('\n','')+'\n'+ '=========================')



    # #p태그 수집
    # if soup.find('p') is not None:
    #     dataes = soup.find_all('p')
    #     for data in dataes:
    #        # data_list_p.append(data.get_text().strip().replace('\n','').replace('\t','').replace('\r',''))
    #        print("p 태그 : ", data.text.strip())
    #        print("p 태그 : ", data_list_p)

    # if soup.find('b') is not None:
    #     dataes = soup.find_all('b')
    #     for data in dataes:
    #         data_list_b.append(data.get_text().strip().replace('\n','').replace('\t','').replace('\r',''))
    #         print("b 태그 : ", data.text.strip())