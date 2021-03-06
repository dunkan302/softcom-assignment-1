import bs4,requests,os
from pathlib import Path
baseUrl='https://timesofindia.indiatimes.com/'
pages={'':'Index','india':'India','world':'World','business':'Business'}
def addToNote(url,title):
    #This takes links and stores stuff in the notpad file
    try:
        write_title=title+'\n\n'
        ntext=''
        write_date=''
        url=url.strip()
        content=requests.get(url)
        soup=bs4.BeautifulSoup(content.text,'html.parser')
        date=soup.find('div',{'class':'_3Mkg- byline'})
        if date.text!=None:
            write_date='Source and Date: '+date.text+'\n\n'
        roughText=soup.find('div',{'class':'ga-headlines'})
        ntext=roughText.text
        f=open('%s.txt' %title,'w',encoding='utf-8')
        f.writelines(write_title+write_date+ntext)
        f.close()
        return 1
    except:
#         print('check: ',title)
        return 0

def getLinkList(res):
    #This takes the section and collects all relevant links
    #Populates a dictionary with link and title
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    subText=soup.find('div',{'class':'main-content'})
    if subText==None:
        subText=soup.find('div',{'id':'content'})
    mainTags=subText.findAll('a',{'class':None})
    linkDict={}
    for page in mainTags:
        href=page.get('href')
        if (href==None):
            continue
        if ('https://' not in href):
            href=baseUrl+href
        if (("photogallery" not in href) and ('videos' not in href)):
            linkDict[page.get("title")]=href
    return linkDict
# res=requests.get('https://timesofindia.indiatimes.com/india')
# dic=getLinkList(res)

def netRunner():
    count=0
    actcount=0
    if ('news' not in os.listdir()):
        os.mkdir('news')
    os.chdir(Path(os.getcwd(),'news'))
    cwd=os.getcwd()
    for key in pages:
        if (pages[key] not in os.listdir()):
            os.mkdir(pages[key])
    for i in pages:
        os.chdir(Path(cwd,pages[i]))
        res=requests.get(baseUrl+i)
        dic=getLinkList(res)
        print(len(dic),'procured from',pages[i])
        actcount+=len(dic)
        for key in dic:
            if (key!=None):
                count+=addToNote(dic[key],key)
    print ('total:',actcount)
    print(count,' in readable format.')
    
netRunner()