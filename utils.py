from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd


def get_blog_links_design2(phases):
    blog_links = []
    for phase_link in [phase['href'] for phase in phases]:
        r = requests.get(phase_link)
        r_soup = BeautifulSoup(r.content, 'html.parser')
        blog_links.extend([blog.find('a')['href'] for blog in r_soup.find_all('article')])
        
    #     if additional pages exist, scrape them also
        has_next = r_soup.find(class_='next')
        while has_next:
            r = requests.get(has_next['href'])
            r_soup = BeautifulSoup(r.content, 'html.parser')
            blog_links.extend([blog.find('a')['href'] for blog in r_soup.find_all('article')])

            has_next = r_soup.find(class_='next')

    return blog_links



# PARSE ALL COMMENTS FROM BLOG
def parse_blog(blog_url):    
    r = requests.get(blog_url)
    r_soup = BeautifulSoup(r.content, 'html.parser')
    
    n_comments = r_soup.find(class_='comment-headline')
    n_comments = n_comments.text if n_comments != None else '0 Comments'
    # print(f"es gibt {n_comments}")
    
    

#         COMMENTS
    comments_parsed = []
    comments_div = r_soup.find(id='comments')
    if comments_div == None:
        return []
    else:
        comments_parsed.extend(parse_comments(comments_div))

        has_prev = r_soup.find(class_='prev')
        while has_prev:
            # print(has_prev.attrs['href'])
            r = requests.get(has_prev.attrs['href'])
            r_soup = BeautifulSoup(r.content, 'html.parser')
            comments_div = r_soup.find(id='comments')
            comments_parsed.extend(parse_comments(comments_div))
            
            has_prev = r_soup.find(class_='prev')

        return comments_parsed

        #     break
#         df = pd.DataFrame(comments_parsed)
#         df.insert(0,'comment_id',range(1,len(comments_parsed)+1))
#         return df

def parse_comments(comments_div):
    comments_parsed = []
    scrape_time = datetime.datetime.now()
    for comment_div in comments_div.find_all(class_='comment-text'):
        
        comments_raw = []
        is_reply = False
        if 'replies' in comment_div.attrs['class']:
            comments_raw = comment_div.find(class_='comment')
            is_reply = True
        else:
            comments_raw = [comment_div]
        
        for comment in comments_raw:
            comment_author = comment.find(class_='comment-author').text
            comment_time = comment.find(class_='comment-time').text.strip()

            comment_ps = comment.find_all('p')
            
            try:
                comment_text = comment_ps[1].text if len(comment_ps) == 2 else comment.find('dl').text.strip()

    #             comment_text = comment.find('p')[1].text
                is_moderator = len(comment.find_all(class_='moderator')) > 0
                reply_to = comment_text.split(': ')[0] if is_reply else None
            
            except:
                comment_text = None
                print(comment)

            comments_parsed.append(
                {
                     'comment_author' : comment_author,
                     'is_moderator' : is_moderator,
                     'comment_time' : comment_time,
                     'comment_text' : comment_text,
                     'reply_to' : reply_to
                }
            )
    return comments_parsed


def count_comments(cc):
    df = pd.read_csv(f'./data/{cc}/blogs_meta.csv')
            
    res_df = pd.read_csv(f'./data/{cc}/results.csv')
    for i, row in res_df.iterrows():
        res_df.at[i,'n_comments'] = int(df.loc[df['project_id'] == row['project_id'], 'n_comments'].sum())

        
    res_df.to_csv(f'./data/{cc}/results.csv', index=None)
