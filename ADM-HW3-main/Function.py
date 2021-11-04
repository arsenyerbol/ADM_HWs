import re
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import numpy as np
import matplotlib.pyplot as plt
import string
from time import time
from bs4 import BeautifulSoup
import lxml
import requests
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from seleniumwire import webdriver
from tqdm import tqdm
import os

'''
Parsing Function

'''

def get_authors(soup):
    Authors = ""
    for el in soup.find_all('span', itemprop='name'):
        #check empty list
        if el.contents[0]:
            Authors = Authors + el.contents[0].replace('\n', '').strip() +", "
        
    
    return Authors[:-2]

def get_plot(soup):
    des = soup.find_all('div', id="description")
    #check empty list
    if des:
        #check empty list
        if des[0].find_all('span', style="display:none"):
            return des[0].find_all('span', style="display:none")[0].get_text().replace('\n', '').strip()
        elif des[0].find_all('span'):
            return des[0].find_all('span')[0].get_text().replace('\n', '').strip()
        else:
            return ''
    else:
        return ''
    
    return None
    
def get_characters(soup):
    
    find = re.compile(r"^([^(]*).*")
    characters = ''
    for el in soup.find_all('a', href=re.compile("/characters/+")):
        #check empty list
        if el.contents[0]:
            
            #Deleting attribuite of the characters eg  Cato (Hunger Games)
            m = re.match(find, el.contents[0].strip()).group(1).strip()
            characters = characters + ', ' + m

    characters = characters[2:]
    
    return characters

def get_places(soup):
    places = ''
    for el in soup.find_all('a', href=re.compile("/places/+")):
        if el.contents[0]:
            places = places + ', ' + el.contents[0].strip()

    places = places[2:]
    
    return places

def get_series(soup):
    List = soup.find_all('a', class_="greyText", href=re.compile("/series/+"))
    if List:
        if List[0].contents:
            return List[0].contents[0].strip()
        else:
            return ''
    else:
        return ''
    
    return None
    
def get_rating_value(soup):
    List = soup.find_all('span', itemprop="ratingValue")
    #check if list is empty
    if List:
        #check if list is empty
        if List[0].contents:
            return List[0].contents[0].strip()
        else:
            return ''
    else:
        return ''
    
    return None


def get_rating_count(soup):
    List = soup.find_all('meta', itemprop="ratingCount")
    #check if list is empty
    if List:
        return List[0].get("content")
    else:
        return ''
    
    return None
    
def get_review_count(soup):
    List = soup.find_all('meta', itemprop="reviewCount")
    #check if list is empty
    if List:
        return List[0].get("content")
    else:
        return ''
    
    return None
    
def get_title(soup):
    List = soup.find_all('h1')
    if List:
        if List[0].contents:
            return List[0].contents[0].replace('\n', '').strip()
        else:
            return ''
    else:
        return ''
    
    return None

def get_number_pages(soup):
    List = soup.find_all('span', itemprop="numberOfPages")
    
    if List:
        if List[0].contents:
            return List[0].contents[0].strip()[:-6]
        else:
            return ''
    else:
        return ''
    
    return None

def get_publishing_date(soup):
    List =soup.find_all('div', id="details")
    
    if List:
        List = List[0].find_all('div', class_="row")
        # we need second element of the list
        if List[1:]:
            if List[1].contents:
                return List[1].contents[0].split("\n")[2].strip()
            else:
                return ''
        else:
            return ''
    else:
        return ''
    
    return None

def scrap_book(soup):
        
    bookTitle = get_title(soup) 
    bookSeries = get_series(soup)
    bookAuthors = get_authors(soup)
    ratingValue = get_rating_value(soup) 
    ratingCount = get_rating_count(soup) 
    reviewCount = get_review_count(soup) 
    Plot = get_plot(soup)
    NumberofPages = get_number_pages(soup) 
    PublishingDate = get_publishing_date(soup)
    Characters = get_characters(soup)
    Settings = get_places(soup)
    
       
    return [bookTitle, bookSeries, bookAuthors, ratingValue, ratingCount, reviewCount, 
            Plot, NumberofPages, PublishingDate, Characters, Settings]
 

'''
Function question 4

'''

def replace_all(x, array):
    for i in array:
        x = x.replace(i, '')
    return x

def check_single_book(x):
    find_1 = re.compile(r'[0-9]-[0-9]') #minus symbol
    find_2 = re.compile(r'[0-9]–[0-9]') #dash symbol
    if len(x.split('#')) == 2:
        if re.match(find_1, x.split('#')[1]) or re.match(find_2, x.split('#')[1]):
            return 0
        else:
            return 1
    else:
        return 1
    
def clean_series(x):
    return x.split('#')[0].strip()

def detect_stable(s):
    if type(s) == str:
        try:
            l = detect(s)
            return l
        except LangDetectException as e:
            return None
    else:
        return None
    
def nrBooksPerSeries(books, x):
    return len(books[books.bookSeries == str(x)])

def Plot_Cumulative_page(Series, book_analysis):
    Year = list(range(book_analysis.PublishingDate.max()+1))

    All_Series_page = {}

    for name in Series:
        page = np.zeros(book_analysis.PublishingDate.max()+1)

        page[book_analysis[book_analysis.bookSeries == name].PublishingDate.values] =\
        book_analysis[book_analysis.bookSeries == name].NumberofPages.values

        All_Series_page[name] = page
        
    plt.figure(figsize=(12, 7))
    for key in All_Series_page.keys():
        plt.plot(Year, np.cumsum(All_Series_page[key]), label = key, linewidth = 4)

    plt.legend()
    plt.show()
    
    return None

'''
Function question 5

'''

'''
The lcs (recursive) function will take in input two strings X and Y and the rispective lenght m = len(X), n = len(Y).
The function will retrieve the length of the longest subsequence of characters from S that are in alfabetical order.
'''

def lcs(X, Y, m, n):
    
    a = m-1
    b = n-1
  
    if m == 0 or n == 0: 
        return 0;
    
    elif X[a] == Y[b]:
        return 1 + lcs(X, Y, a, b); 
    else: 
        return max(lcs(X, Y, m, b), lcs(X, Y, a, n))
    
    
'''
We decided to define the mx_lcs function in order to "automate" the process of comparing the strings.
What we mean is that, thanks to this function, we will just need to give in input the string we want to compare
and then the lcs function (that will do the heavy work) will be called automatically.
'''
def max_lcs(X):
    alphabet_string = string.ascii_uppercase
    a = len(alphabet_string)
    
    b = len(X)
    
    if X.isupper():
        return lcs(X,alphabet_string,b,a)
    
    else:
        X.upper()
        return lcs(X,alphabet_string,b,a)
        

'''
The function exp_plot will give us a graphical output on a log scale in order to verify that
the time complexity is exponential. We are going to show this plot on the first 10 characters
of the input string.
'''

def exp_plot(string):
    
    string_lenght = []
    Time = []

    for i in range(6):
        S = string[: (5 + i)]
        string_lenght.append(len(S))

        t1 = time()

        lenght = max_lcs(S)

        t2 = time()

        Time.append(t2-t1) 
    
    # plotting on a logarithmic scale we will state that the time is exponential if the plot is a straight line
    plt.plot(string_lenght,Time)
    plt.yscale("log")
    plt.show()
    
    return None


'''
The following function will retrieve the longest subsequence of characters from S that are in alfabetical order
using dynamic programming which will fasten a lot the time of execution.
'''

def lcs_DP_(X , Y): 
    
    m = len(X) 
    n = len(Y) 
  
    # declaring the array for storing the dp values 
    L = [[None]*(n+1) for i in range(m+1)] 
  
    # following steps build an array L[m+1][n+1]
    for i in range(m+1): 
        for j in range(n+1): 
            
            # the first row and column of the array will be composed of zero's
            if i == 0 or j == 0 : 
                L[i][j] = 0
                
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
                
            else: 
                L[i][j] = max(L[i-1][j] , L[i][j-1]) 
  
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
    return L[m][n] 


# "automating" the function in order to have just one input

def lcs_DP(X):
    alphabet_string = string.ascii_uppercase
    return lcs_DP_(X,alphabet_string)


def matrix(X , Y): 
    
    m = len(X) 
    n = len(Y) 
  
    # declaring the array for storing the dp values 
    L = [[None]*(n+1) for i in range(m+1)] 
  
    # following steps build an array L[m+1][n+1]
    for i in range(m+1): 
        for j in range(n+1): 
            
            # (?) the first row and column of the array will be composed of zero's
            if i == 0 or j == 0 : 
                L[i][j] = 0
                
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
                
            else: 
                L[i][j] = max(L[i-1][j] , L[i][j-1]) 
  
    
    return L 
