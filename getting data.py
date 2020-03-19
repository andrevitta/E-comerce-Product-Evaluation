# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 19:47:39 2020

@author: user
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
###############################################################################
## main variables

header = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
          }
#'cookie':'session-id=257-2197159-1971113; i18n-prefs=EUR; ubid-acbfr=257-3404900-4609202; x-wl-uid=1Xfm4ngY5/K4eT9HQVQgNI/G/C5By2L49L3Y0G7RvIPRIulHy33xmE9wFWDNeOkvYrPzX6KbWHFE=; session-id-time=2082787201l; session-token="V5cCXoe5RlfH4YLELJGD+RdRuEzX5/8lggVzuAXUbM/dEfVmUG/Tq8V3+S/RgRR/Y38EV/MYJ2Qipzvql1CuUA580VpOVHGf6cHCCxboXOaH/PQeSUUWLYoHjm4+kfKgdtm/VqW0D7hxuIrCjNNJwF/mF42F1MZJgHsZ/ulI4J6ISDgt7PjwV+xmCgP9cUCD/U+Zxai5iifue/q+XaIrTnC1hCcJIMohepRE5p/d2JiAZWztAQL5UtbwUTDPIuGm1y+4OYuRV9g="; csm-hit=tb:s-6CSP0ZNQ65G1QM8XMW14|1579901664326&t:1579901664465&adb:adblk_no'
###############################################################################
## Defining functions

def get_name(path,header=header):
      soup = BeautifulSoup(requests.get(path,headers=header).content,'lxml')
      return soup.select('h1>span')[0].text.strip()


def get_next_page(soup):
      # get next page
      next_page = [i['href'] for i in soup.select('li.a-last [href]')]
      if len(next_page)!=0:
            url = main_url+next_page[0]
      else:
            url = []
      
      return url

def avg_rating(df):
      return sum( [df[i]*(i+1) for i in  range(5)])


def get_comments(url,header=header):

      # define variables
      check2_name = []
      N_evaluations =[]
      stars = []
      comments_date =[]
      comments_content=[]
      page_count =0
            
      while len(url)!=0 :
            
            # get comment link
            r=requests.get(url,headers=header)
            page_count +=1
      
      
            if r.ok:
                  print (r, str(page_count)+' Comentary Pages loaded')
                  
                  # make comments soup :) 
                  soup = BeautifulSoup(r.content,'lxml')
                  
                  if page_count == 1:
                        
                        # get name , Number of evauations, Number of comentaires and ratings for each star
                        check2_name = soup.select('h1>.a-link-normal')[0].text
                        N_evaluations = int( soup.select('span.a-size-base')[0].text.strip().split()[0] ) 
                        raw_ratings = soup.select('td span.a-size-base .a-link-normal')
                        star = [raw_ratings[i].text.strip().split()[0] for i in range( 0,len(raw_ratings),2)]
                        per_cents = [raw_ratings[i].text.strip() for i in range( 1,len(raw_ratings),2)]
                        ratings = [star,per_cents]
                        Ncomentaries = soup.select('[data-hook="cr-filter-info-review-count"]')[0].text.split()[-2]
                        
                        print (' Number of evaluations:',str(N_evaluations))
                        
                        # wait for it ....
                        time.sleep(2)
                  else:
                        # get Stars, Date and content of each comment
                        stars.append( [i.text.strip().split(',')[0] for i in soup.select('div>a.a-link-normal>i')] )
                        comments_date.append( [i.text for i in soup.select('div#cm_cr-review_list span.a-size-base[data-hook="review-date"]')])
                        comments_content.append( [i.text.strip() for i in soup.select('div#cm_cr-review_list span.a-size-base[data-hook="review-body"]')] )
                   
                        # wait for it ....
                        time.sleep(2)
            else:
                  raise ConnectionError
                  print (r)
            # get next page
            
            url = get_next_page(soup)
                  
      
      # organize output
      names = check2_name
      Neval = N_evaluations
      st    = [j for star in stars for j in star]
      cdate = [j for date in comments_date for j in date]
      ccont = [j for coment in comments_content for j in coment]
      
      #df =pd.DataFrame({'Name':names, 'No_Evaluations':Neval, 'Rating':st, 'Date':cdate,'Comment':ccont})
      
      return [names,Neval,ratings,Ncomentaries,st,cdate,ccont]

##############################################################################
def get_articles(url,header=header):

      articles_name = list()
      articles_link = list()
      page_count = 0
      next_page = [1]
      
      while len(next_page)!=0 :
      
            # get the main page of query
            r = requests.get(url,headers=header)
            page_count +=1
            
            # check if pages were loaded and scrapes it
            if r.ok:
                  print (r, str(page_count)+' Pages loaded')
                  
                  # make soup :) 
                  main_soup = BeautifulSoup(r.content,'lxml')
      
                  # get article names
                  articles_name.append([i.text.strip('\n') for i in main_soup.select('h2>a')])
      
                  # get articles links
                  articles_link.append([ a['href'] for a in main_soup.select('h2>a',href=True) ])
                  
                  # wait for it ....
                  time.sleep(2)
            else:
                  raise ConnectionError
                  print (r)
                  
            # get next page
            next_page = [i['href'] for i in main_soup.select('li.a-last [href]')]
            if len(next_page)!=0:
                  url = main_url+next_page[0]
            else:
                  break
            
            # organize output and remove duplicates
      df = pd.DataFrame({'Name':[j for article in articles_name for j in article], 'Link': [j for link in articles_link for j in link] })
      df = df.iloc[df.Name.drop_duplicates().index,:]
      df.reset_index(drop=True,inplace=True)      
      return df

##############################################################################
def get_articles_data(df):
      product_count = 0
      Nproducts = len(df)
      check_name=[]
      evaluations =[]
      similarite_name=[]
      similarite =[]
      
      for i in range( len(df) ):
            
            # Get URL from df 
            url = main_url+df.Link[i]
            
            # get product page 
            r = requests.get(url,headers=header)
            product_count+=1
            
            # check if pages were loaded and scrapes it
            if r.ok:
                  # prit check
                  print (r, str(product_count)+' Products loaded of ',str(Nproducts))
            
                  # make leftover soup :) 
                  sub_soup = BeautifulSoup(r.content,'lxml')   
                  
                  # select product name for verification
                  check_name.append(sub_soup.select('h1>span')[0].text.strip())
                  
                  # select all evaluations page link
                  
                  evaluation_link = sub_soup.select('.a-link-emphasis')  
                  
                  if len (evaluation_link) != 0:
                        evaluations.append( get_comments(main_url+evaluation_link[0]['href']) )
                  else :
                        evaluations.append([])
                  
                  # PRODUCTS ALSO BOUGTH FREQUENTELLY
                  links_similarite = [i['href'] for i in sub_soup.select('LI.a-spacing-mini .a-size-base[href]')]
                  for j in range(len(links_similarite)):
                        similarite.append( get_name(main_url+links_similarite[j]) )
                  similarite_name.append(similarite)
                  similarite = []
            else:
                  raise ConnectionError
                  print (r)
      df = pd.DataFrame({'Name':check_name, 'Eval_name': evaluations, 'Similarities':similarite_name })
     
      return df
###############################################################################
######wrangling
def wrangle_info(df):
      
      name_id=[]
      name=[]
      N_eval=[]
      N_comments=[]
      ratings=pd.DataFrame()
      
      for i in range(len(df)):
      
            if len(df.Eval_name[i])!=0:
                  name_id.append( i )
                  name.append( df.Eval_name[i][0] )
                  N_eval.append( df.Eval_name[i][1] )
                  N_comments.append( int( df.Eval_name[i][3] ) )
                  
                  rating=pd.DataFrame(df.Eval_name[i][2][1]).T
                  rating.columns=df.Eval_name[i][2][0]
                  rating.iloc[0,:]=rating.iloc[0,:].str.strip('%').astype(int) /100
                  ratings=pd.concat([ratings,rating],sort=True)
            else:
                  continue
      
      # making a Data Frame and ajusting it       
      df_info = pd.DataFrame( {'Name_Id':name_id, 'Name': name, 'N_evaluation':N_eval,'N_comments':N_comments})
      df_info = pd.concat([df_info,ratings.reset_index()],sort=True,axis=1)
      df_info.drop('index',axis=1,inplace=True)
      
      # replaceing missing values of stars for 0
      df_info.loc[:,'1':'5'] = df_info.loc[:,'1':'5'].fillna(0)
      
      # calculating avg ratings
      df_info['Avg_rating'] = df_info.loc[:,'1':'5'].apply(avg_rating,axis=1)
      
      return df_info
###############################################################################
def wrangle_comments(df) :
      name_id=[]
      ratings=[]
      dates=[]
      comments=[]
      for i in range( len(df.Eval_name)):
            
            lst = df.Eval_name[i]
                    
            if len(lst)!=0:
                  # fixing a empty spaces issue must solve it better!!!!
                  lst[4] = list(filter(None, lst[4])) 
                  
                  if len(lst[4])!=len(lst[5]) :
                        print( i )
                  name_id+=([i]*len(lst[4]))
                  ratings+=( lst[4] )
                  dates+=( lst[5] )
                  comments+=( lst[6] )
            else:
                  continue
            
      df_comments= pd.DataFrame({'Name_Id':name_id, 'Comments_Ratings':ratings, 'Comment_date':dates, 'Comments':comments})
      df_comments.Comments_Ratings = df_comments.Comments_Ratings.astype(int)
      
      return df_comments
##############################################################################
def get_top(df_info):
      top20 = df_info.sort_values(by=['N_evaluation'],ascending=False).head(20)

      top6 = top20.sort_values(by=['Avg_rating'],ascending=False).head(6)
      return top6 

##############################################################################
def get_analisys(df_info,df_comments):
      
      top6 = get_top(df_info)
      
      Ids = list (top6.Name_Id[1:])

      ######################
      positive =[]
      negative = []
      T=[]
      name_id =[]
      
      for i in Ids:

            ind = df_comments.Name_Id == i
            name_id.append(i)
            vcount = df_comments.Comments_Ratings[ind].value_counts()
       
            positive.append( vcount.iloc[vcount.index>3].sum() )
            negative.append( vcount.iloc[vcount.index<=3].sum() )
      
            text = [ i.split() for i in df_comments.Comments[ind].replace('\W',' ',regex=True)]
            
            T_text = []
            for i in range(len(text)):
                  T_text+=text[i]
            
            T.append([ [t for t in T_text if len(t)>4] ])

      analisys = pd.DataFrame( {'Name_Id':name_id,'Positive':positive, 'Negative': negative, 'Comments':T } )
      return top6 , analisys
###############################################################################

                ### Aquisition ######
## query for loreal+gariner and filter for garnier

# define global variable
      
main_url = 'https://www.amazon.fr'

url = 'https://www.amazon.fr/s?k=loreal+garnier&rh=p_89%3AGarnier&ref=sr_pg_1'


print ( time.localtime())
# get df of products on pages
#df = get_articles(url)
df.to_json('df_main.json')

# Gets data from each page DF of main query 

#df_articles = get_articles_data(df)
df_articles.to_json('df_articles.json')
print ( time.localtime())      

                 ##### wrangling ######
# make two clean dfs on with the product infos and the second with comentaries
# create also product id to conect the two df

# organizes products infos
df_info = wrangle_info(df_articles)
df_info.to_json('df_info.json')

### Organize comments 
df_comments = wrangle_comments(df_articles)
df_comments.to_json('df_comments.json')


# select top 5 evaluated products wit more than 30 evaluations

top6, df_analysis = get_analisys(df_info,df_comments)
df_analysis.to_json('df_analisys.json')

################################################################################
#main_url = 'https://www.amazon.com'
#
#url = 'https://www.amazon.com/s?k=loreal+garnier&rh=p_89%3AGarnier&ref=sr_nr_p_89_1'
#
#print ( time.localtime())
#
## get df of products on pages
#df = get_articles(url)
#df.to_json('df_main_US.json')
#
## Gets data from each page DF of main query 
#df_articles = get_articles_data(df)
#df_articles.to_json('df_articles_US.json')
#
#print ( time.localtime())      
#
#
#                 ##### wrangling ######
## make two clean dfs on with the product infos and the second with comentaries
## create also product id to conect the two df
#
## organizes products infos
#df_info = wrangle_info(df_articles)
#df_info.to_json('df_info_US.json')
#
#### Organize comments 
#df_comments = wrangle_comments(df_articles)
#df_comments.to_json('df_comments_US.json')
#
#
## select top 5 evaluated products wit more than 30 evaluations
#
#df_analisys = get_analisys(df_info,df_comments)
#df_analisys.to_json('df_analisys_US.json')



