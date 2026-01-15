import os
import datetime
import feedparser
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit(1)

client = genai.Client(api_key=API_KEY)

# RSS Feeds to check
RSS_FEEDS = [
    "https://news.ycombinator.com/rss",  # Hacker News
    "https://techcrunch.com/feed/",      # TechCrunch
    "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml", # ITmedia
]

def fetch_rss_items():
    items = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]: # Top 5 from each
                items.append(f"- Title: {entry.title}\n  Link: {entry.link}\n  Summary: {entry.get('summary', 'No summary')}\n")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return items

def generate_blog_post(feed_items):
    today = datetime.date.today().isoformat()
    
    prompt = f"""
    You are a helpful assistant for a tech blog "U-REI.com".
    Today is {today}.
    
    Here is a list of recent tech news headlines:
    
    {''.join(feed_items)}
    
    Please select ONE interesting topic from these headlines that would be suitable for a personal tech blog.
    Write a blog post about it in Japanese.
    
    IMPORTANT: Provide ONLY the Markdown content starting with the Front Matter. 
    Do NOT include any conversational filler.
    Do NOT repeat the title as an H1 header (`# Title`) inside the body, as the blog theme already displays the title from the Front Matter.
    
    The blog post MUST follow this structure (Hugo Markdown):
    
    ---
    title: "{{Title of the post}}"
    date: {datetime.datetime.now().astimezone().isoformat()}
    draft: false
    tags: ["News", "{{Topic Tag}}"]
    categories: ["Tech"]
    ---
    
    Write an engaging introduction about the news.
    Summarize the key points based on the headline and what you know about the topic.
    Add some personal thoughts or analysis (as a tech enthusiast).
    
    Reference the original link at the end.
    """
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text

def save_post(content):
    # Extract title for filename (simple approach, or just use date)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"content/posts/{today_str}-daily-news.md"
    
    # Clean up markdown code blocks if present
    content = content.replace("```markdown", "").replace("```", "").strip()

    # Ensure it starts with --- (strip any conversational filler Gemini might have added)
    if "---" in content:
        content = "---" + content.split("---", 1)[1]
    
    # Extract title from front matter
    title = "Daily News"
    try:
        import re
        match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
        if match:
            title = match.group(1)
    except Exception:
        pass

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved post to {filename}")
    return title

def main():
    print("Fetching RSS feeds...")
    items = fetch_rss_items()
    if not items:
        print("No news found.")
        return

    print("Generating post with Gemini...")
    try:
        post_content = generate_blog_post(items)
        title = save_post(post_content)
        
        # Write title to GITHUB_OUTPUT
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"post_title={title}\n")
                
    except Exception as e:
        print(f"Error generating post: {e}")

if __name__ == "__main__":
    main()