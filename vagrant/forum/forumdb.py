#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
#DB = []
DB = "dbname=forum"

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    conn = psycopg2.connect(DB)
    query = "select * from posts order by time desc"
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    posts = [{'content': bleach.clean(row[0]).encode('ascii', 'ignore'), 'time': row[1].strftime('%y-%m-%d')} for row in rows]
    conn.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    conn = psycopg2.connect(DB)
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))
    c = conn.cursor()
    c.execute("insert into posts (content) values (%s)", (content, ))
    conn.commit()
    conn.close()
