import praw
from datetime import datetime
from sqlmodel import Session
from app_main import engine
from models import Source

# Configure Reddit API
reddit = praw.Reddit(
    client_id="YOUR_ID",
    client_secret="YOUR_SECRET",
    user_agent="fiction-engine"
)

def scrape_reddit(subreddit="Fantasy", limit=20):
    subreddit_obj = reddit.subreddit(subreddit)
    posts = []
    for post in subreddit_obj.new(limit=limit):
        posts.append(Source(
            platform="reddit",
            url=f"https://reddit.com{post.permalink}",
            author=str(post.author),
            posted_at=datetime.utcfromtimestamp(post.created_utc),
            raw_text=(post.title or "") + "\n" + (post.selftext or "")
        ))
    with Session(engine) as s:
        for p in posts:
            s.add(p)
        s.commit()
    print(f"✅ Scraped {len(posts)} posts from r/{subreddit}")
    return posts

if __name__ == "__main__":
    scrape_reddit("Fantasy", limit=10)
