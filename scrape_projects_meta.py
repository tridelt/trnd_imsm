from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils import *
from requests.exceptions import *


def scrape_projects_meta(cc):
    r = requests.get(f'https://www.trnd.com/{cc}')
    r_soup = BeautifulSoup(r.content, 'html.parser')
    projects_url = r_soup.find(class_='CampaignOverview')['href']

    r = requests.get(projects_url ,headers={'user-agent': 'x'})
    r_soup = BeautifulSoup(r.content, 'html.parser')
    
    articles = r_soup.find_all('article')
    articles_parsed = []

    for i, article in enumerate(articles):
        link_elem = article.find(class_='campaign-card__link')
        category_elem = article.find(class_='campaign-card__category')
        title_elem = article.find('h1')
        description_elem = article.find(class_='campaign-card__paragraph')
        dates_elems = article.find(class_='campaign-card__progress').find_all('p')

        articles_parsed.append(
            {
                 'project_id' : i+1,
                 'href' : link_elem.attrs['href'] if link_elem else None,
                 'category' : category_elem.text.strip() if category_elem else None,
                 'title' : title_elem.text.strip() if title_elem else None,
                 'description' : description_elem.text.strip() if description_elem else None,
                 'start_date' : dates_elems[0].text.strip() if dates_elems else None,
                 'end_date' : dates_elems[1].text.strip() if dates_elems else None
            }
        )
    df = pd.DataFrame(articles_parsed)
    df.to_csv(f'./data/{cc}/projects.csv', index=None)

    
    
    project_df = pd.read_csv(f'./data/{cc}/projects.csv')
    csv_projekte_meta_lines = []
    for i, row in project_df.iterrows():   

        try:
            r = requests.get(row['href'])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(f"error while scraping PROJECT page for: {row['href']}")
            continue
            
        r_soup = BeautifulSoup(r.content, 'html.parser')


        participants_elem = r_soup.find(class_='project-hero__project-size')

        participants = int(participants_elem.text.split()[0]) if participants_elem else None

        row['participants'] = participants
        csv_projekte_meta_lines.append(row)
    #     break

    df = pd.DataFrame(csv_projekte_meta_lines)
    df.to_csv(f'./data/{cc}/projects.csv', index=None)  