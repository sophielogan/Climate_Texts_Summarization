'''
This file webscrappes the press releases and publications from:
"https://www.climatepolicyinitiative.org"
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
import requests
import os
import subprocess

def make_soup(url):
    '''
    This function makes a soup object given a url
    Input:
        url: (str) A url from a website
    Output:
        soup: (BeautifulSoup) A Beautiful Soup object we can scrape
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    return soup


def get_links(url):
    '''
    Gets the link of press realeases from Climate Policy Finance
    Input:
        url: (str) This gets the press releases from:
        "https://www.climatepolicyinitiative.org/resources/press-releases/"
    Output:
        link: (lst of str) Retrieves a list of link of each press realease
    '''
    soup = make_soup(url)

    # Find all h2 tags with class "post-header--title"
    headers_h2 = soup.find_all("h2", class_="post-header--title")

    links = []
    # Loop through the headers and extract the links in the <a> tags
    for header in headers_h2:
        link = header.find("a").get("href")
        links.append(link)
    
    return links


def press_release_extractor(links):
    '''
    Loop through the press releases links and extract their content into a dataframe
    Input:
        link: (lst of str) List of link of each press realease
    Output:
        articles_df: (pandas dataframe) Contains the information of the press releases.
        Including the tittles, content and programs.
    '''
    titles = []
    contents = []
    programs = []
    for link in links:
        soup = make_soup(link)    
        # Extract the title, content, and program of the press release
        article = soup.find('article')
        title = article.find("h1", class_="article--title").text.strip()
        titles.append(title)
        content = article.find("div", class_="col article--content").text.strip()
        contents.append(content)
        try:
            program = article.find("div", class_="post-meta post-taxonomy is-programs").find("a").text.strip()
        except AttributeError:
            program = 'NA'
        programs.append(program)

    # create a dictionary with keys as attribute names and values as lists
    articles_data = {'Title': titles, 'Content': contents, 'Program': programs}

    # create a dataframe from the dictionary
    articles_df = pd.DataFrame(articles_data)

    return articles_df


def get_press_realeases():
    '''
    Scrapes the press releases of Climate Policy Finance and save their content in a csv file
    Output:
        articles.csv
    '''
    links = get_links("https://www.climatepolicyinitiative.org/resources/press-releases/")
    articles_df = press_release_extractor(links)
    articles_df.to_csv('articles.csv', index=False)


def publications_extractor(links):
    '''
    Loop through the publications links and extract their content into a dataframe,
    Including downloading the full reports and extracting all the written content
    Input:
        link: (lst of str) List of link of each publication
    Output:
        articles_df: (pandas dataframe) Contains the information of the publication.
        Including the tittles, content, programs, and full reports.
    '''
    # Loop through the links and print the title and URL of each press release
    titles = []
    contents = []
    programs = []
    full_reports = []
    for link in links:
        soup = make_soup(link)    
        # Extract the title, content, and program of the press release
        article = soup.find('article')
        try:
            title = article.find("h1", class_="article--title").text.strip()
        except AttributeError:
            continue
        titles.append(title)
        try:
            content = article.find("div", class_="col article--content").text.strip()
        except AttributeError:
            content = 'NA'
        contents.append(content)
        try:
            program = article.find("div", class_="post-meta post-taxonomy is-programs").find("a").text.strip()
        except AttributeError:
            program = 'NA'
        programs.append(program)

        # Full report link
        try:
            report_link = article.find("div", class_="post-meta post-downloads").find("a").get('href')
        except AttributeError: 
            full_reports.append('N/A')
            continue
        
        # Delete the PDF file
        try:
            os.remove('full_report.pdf')
        except FileNotFoundError:
            pass

        # Download the full report
        #!curl -o full_report.pdf {report_link}
        command = "curl -o full_report.pdf "+ report_link
        subprocess.run(command, shell=True)

        # Open the PDF file in read-binary mode
        with open('full_report.pdf', 'rb') as f:
            # create a PyPDF2 reader object from the PDF content
            try:
                pdf_reader = PyPDF2.PdfReader(f)
            except Exception:
                full_reports.append('N/A')
                continue
                
            # read the text content from the PDF file
            full_report = ""
            for page in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page]
                full_report += page_obj.extract_text()

            # print the text content
            full_reports.append(full_report)
    
    # create a dictionary with keys as attribute names and values as lists
    publications_data = {'Title': titles, 'Content': contents, 'Program': programs, 'Full_Report': full_reports}

    # create a dataframe from the dictionary
    publications_df = pd.DataFrame(publications_data)

    return publications_df


def get_publications():
    '''
    Scrapes the publications of Climate Policy Finance and save their content in a csv file
    Output:
        publications.csv
    '''
    links = get_links("https://www.climatepolicyinitiative.org/resources/publications/")
    publications_df = publications_extractor(links)
    publications_df.to_csv('publications.csv', escapechar='\\',  index=False)
