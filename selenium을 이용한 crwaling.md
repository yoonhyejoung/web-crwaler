# selenium을 이용한 crwaling 

##### 사용자가 원하는 키워드를 Naver 지식인에 검색하여 질문과 채택된 답변만을 txt 파일로 저장



 1. selenium 드라이버 설치(Chrome 드라이버)   

    ```python
    from selenium import webdriver #웹 자동화 프로그램 import
    
    #크롬 드라이버 사용
    driver = webdriver.Chrome('D:\\chromedriver') #설치한 크롬드라이버 위치
    #원할한 접속을 위해 3초 대기
    driver.implicitly_wait(3)
    
    ```

2. selenium으로 네이버 지식인 자동 접속

   ```python
   driver.get ("https://kin.naver.com/index.nhn")
   ```

   

3. beatifulSoup을 통해 페이지 가져오기

```python
#Beautifulsoup를 이용해 크롤링
from bs4 import BeautifulSoup #크롤링 import
#네이버 지식인 검색창에 검색 키워드 전송
elem = driver.find_element_by_name("query")
elem.send_keys(keyword)
elem.submit()

#requests요청으로 url 정보를 가져오고 인코딩, text문서로 변환
res = requests.get(url)
res.encoding = res.apparent_encoding
html = res.text
soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')

```

4. selenium으로 페이징 처리

   ```python
   #현재 페이지를 driver hadlese 배열 0으로 설정
   window_before = driver.window_handles[0]
   
   #driver.window_handles: 현재 페이지를 window_handles배열에 저장, selenium에서 제공
   elems = driver.find_elements_by_xpath('.//li[*]/dl/dt/a')
   
   #xpath : W3C의 표준으로 확장 생성 언어 문서의 구조를 통해 경로 위에 지정한 구문을 사용하여 항목을 배치하고 처리하는 방법을 기술하는 언어이다.
   #driver.find_elements_by_xpath함수를 통해 해당 페이지에 검색 결과 링크수 찾음
   elems = driver.find_elements_by_xpath('.//li[*]/dl/dt/a')
   
   
   ### 현재 페이지의 검색결과 링크의 개수가 몇개인지 파악
   for elem in elems:
       #print (elem.get_attribute("href"))
       n = n + 1
   print ("한페이지 검색 결과 :  ", n) 
   
   #driver.find_elements_by_xpath함수를 통해 몇페이지가 있는지 찾음(ex.1page~10page, 다음페이지 )
   elems2 = driver.find_elements_by_xpath('.//div[3]/div[2]/a')
   for elem2 in elems2:
       #print (elem2.get_attribute("href"))
       m = m + 1
   print ("검색결과 페이지 수 : ", m)  
   
   ```

   

5. 네이버 지식인 크롤링

   ```python
     while True:
   		#i는 selenium이 검색 결과 링크들을 하나씩 클릭하기 위한 변수 점차 증가 
           i = i + 1   
       
   		#변수 n은 실제 검색 결과 한 페이지의 링크 개수(ex. 10)
           #일반적으로 검색결과 한페이지에 10개의 링크가 표시되고 10개의 페이지의 링크를 클릭하면 2페이지로 이동
           if i <= n:
               
               driver.find_element_by_xpath('//*[@id="s_content"]/div[3]/ul/li[' +str(i)+ ']/dl/dt/a').click()  
               #웹크롤러를 클릭한 페이지로 변수 driver이동
               driver.switch_to.window(driver.window_handles[-1])
               #새로 열린 페이지의 url주소를 driver.current_url함수로 이용해 url변수에 저장
               url = driver.current_url
               print (url)
               res = requests.get(url)
               #한글을 위한 인코딩
               res.encoding = res.apparent_encoding
               #html을 text로 변환
               html = res.text
               #html.parser로 파싱
               soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')
               #soup.find함수, i태그의 클래스 이름이 icon_check_adopt(네이버 채택 표시)을 find하면 it문 실행
               if soup.find('i', {'class':'icon icon_check_adopt'}):
   				#div태그의 클래스 명이 title이 있으면 다음 if문 실행
                   if soup.find('div', {'class':'title'}) is not None: 
                       title = soup.find('div', {'class':'title'})
                       title.insert(0, "title : ")
                       #data_list_naver 리스트에 title에 대한 text를 예쁘게 입력(text파일로 출력하기 위해)
                       data_list_naver.append(title.get_text().strip().replace('  ','').replace('\n',''))
                       #콘솔에 출력
                       print ("title ", ":", title.text.strip().replace('  ','').replace('\n',''))
          			#div태그의 클래스 명이 c-heading__content 있으면 다음 if문 실행
                   if soup.find('div', {'class':'c-heading__content'}) is not None:
                       contents = soup.find('div', {'class':'c-heading__content'})
                       contents.insert(0, "content : ")
                       data_list_naver.append(contents.get_text().strip().replace('  ','').replace('\n',''))
                       print ("contnet : ", contents.text.strip().replace('  ','').replace('\n',''))
                       print ('\n')            
                      
   				#div태그의 클래스 명이 heading__content 있으면 다음 if문 실행
                   if soup.find('div', {'class':'c-heading__content'}) is not None:
   
                       print ("=================================채택된 답변==================================")
                       solution = soup.find('div', {'class':'_endContentsText c-heading-answer__content-user'})
                       solution.insert(0, "solution : ")
                       data_list_naver.append(solution.get_text().strip().replace('  ','').replace('\n',''))
                       print ("solution : ", solution.text.strip().replace('  ','').replace('\n',''))
                    
                       print ('\n')    
                  
                   #sleep(5)
               
                   driver.close()
                   driver.switch_to.window(driver.window_handles[0])
                   file = open('naver.txt','w', encoding='utf-8')
                   for naver in data_list_naver:
                       file.write(naver + '\n')  
                   file.close()   
   
               else :
                   #sleep(5)
                   driver.close()
                   driver.switch_to.window(driver.window_handles[0]) 
   #만약 10개의 링크를 클릭했다면 다음 if문 실행
           elif i > n:
           #n은 0으로 초기화 하고
               n = 0
               #1페이지에서 2페이지의 이동을 위한 변수
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
               #만약 10페이지까지 이동을 하고 다음페이지 버튼을 클릭하기 위한 if 문
               if j == m:
                   m = 0 
                   elems2 = driver.find_elements_by_xpath('.//div[3]/div[2]/a')
                   for elem2 in elems2:
                       #print (elem2.get_attribute("href"))
                       m = m + 1
                   print ("검색결과 페이지 수 : ", m)     
                   j = 1 
   ```

   