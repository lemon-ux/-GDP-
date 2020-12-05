import requests
import re
from bs4 import BeautifulSoup
import bs4
import traceback      #输出详细的异常信息
import xlwt


#获取爬取网页源代码
def getHTMLText(url,code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        #print(r.text)
        return r.text
    except:
        return "爬取失败"


#将获取的显示的各个年份存入列表
def getGDPList(GDPurl):
    lst1=[]
    html = getHTMLText(GDPurl)
    soup = BeautifulSoup(html , 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst1.append(re.findall(r'(19[6-9]\d|200\d|201[0-8])',href)[0])
        except:
            continue
    lst1.reverse()
    print(lst1)
    return lst1
    


#将获取的各个国家url存入列表
def getCountryList(GDPurl):
    count1=[]
    count2=[]
    html = getHTMLText(GDPurl)
    try:
        if html == "":
            print("")
        soup = BeautifulSoup(html,'html.parser')
        countryInfo = soup.find_all('ul',attrs={'class':'list-inline ul-country'})
        for ul in countryInfo:
            a = ul.find_all('a')
            for i in a:
                count1.append(i.attrs['href'])
                count2.append(i.string)
        print(count1)
        print(count2)
        return count1,count2    
    except:
        return "",""


#获取每个国家每年GDP数据并存入excel文件
def getGDPInfo(lst1,count1,count2,filename):
    values = []
    for country in count1:
        value = []
        url = "https://www.kylc.com" + country
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html,'html.parser')
            gdpInfo = soup.find('tbody')
            for tr in gdpInfo.children:
                if isinstance(tr,bs4.element.Tag):
                    tds = tr.contents
                    if len(tds) < 4:
                        continue
                    else:
                        digit = re.findall(r'[(](.*?)[)]',tds[3].string)[0]
                        value.append(digit.replace(',',''))
            values.append(value)
        except:
            traceback.print_exc()     
            continue
    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('python_work')
    heads = ['Country Name']
    heads.extend(lst1)
    for i in range(0,len(lst1)+1):
        sheet.write(0,i,heads[i])
    n = 1
    for value in values:
        for m in range(1,len(value)+1):
            sheet.write(n,m,value[m-1])
        print("\r当前进度：{:.2f}%".format(n*100/len(values)),end="")
        n += 1
    for j in range(1,len(count2)+1):
        sheet.write(j,0,count2[j-1])    
    work_book.save(filename)
    
        
def main():
    gdp_url = 'https://www.kylc.com/stats/global/yearly_overview/g_gdp.html'
    output_file = 'gdp_analysis.xls'
    list1 = []
    gcount1 = []
    gcount2 = []
    list1 = getGDPList(gdp_url)
    gcount1,gcount2 = getCountryList(gdp_url)
    getGDPInfo(list1,gcount1,gcount2,output_file)

main()
