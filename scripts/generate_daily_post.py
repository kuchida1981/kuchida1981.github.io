import os
import datetime
import feedparser
import re
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
    author: "Ghost Writer"
    ---
    
    Write an engaging introduction about the news.
    Summarize the key points based on the headline and what you know about the topic.
    Add some personal thoughts or analysis (as a tech enthusiast).
    
    Reference the original link at the end.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def sanitize_slug(raw: str) -> str:
    cleaned = re.sub(r'\s+', '-', raw)
    cleaned = cleaned.lower()
    cleaned = re.sub(r'[^a-z0-9\-]', '', cleaned)
    cleaned = re.sub(r'-+', '-', cleaned)
    cleaned = cleaned.strip('-')
    words = cleaned.split('-')
    if len(words) > 6:
        words = words[:6]
    cleaned = '-'.join(words)
    if not cleaned:
        return "daily-news"
    return cleaned

def generate_slug(client, title: str) -> str:
    prompt = f"""
    Please generate an English slug for the following Japanese title.
    
    Title: "{title}"
    
    Requirements:
    - 2 to 6 English keywords representing the main subject of the title.
    - Use kebab-case and lowercase ASCII characters only.
    - Output ONLY the slug itself (do NOT include any markdown code blocks, conversational filler, or additional text).
    
    Example:
    "Adobe Creative CloudにAIエージェント全面導入！" -> "adobe-ai-agents-creative-cloud"
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        raw_slug = response.text
        if not raw_slug:
            return "daily-news"
        return sanitize_slug(raw_slug)
    except Exception as e:
        print(f"Error generating slug: {e}")
        return "daily-news"

def extract_title(content: str) -> str:
    try:
        cleaned = content.replace("```markdown", "").replace("```", "").strip()
        if "---" in cleaned:
            cleaned = "---" + cleaned.split("---", 1)[1]
        match = re.search(r'^title:\s*"(.*?)"', cleaned, re.MULTILINE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Daily News"

def save_post(content, slug: str = "daily-news"):
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    year = today.strftime("%Y")
    month = today.strftime("%m")
    out_dir = f"content/posts/{year}/{month}"
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{out_dir}/{today_str}-{slug}.md"
    
    # Clean up markdown code blocks if present
    content = content.replace("```markdown", "").replace("```", "").strip()

    # Ensure it starts with --- (strip any conversational filler Gemini might have added)
    if "---" in content:
        content = "---" + content.split("---", 1)[1]
    
    # Extract title from front matter
    title = "Daily News"
    try:
        title = extract_title(content)
        
        # Check if author line exists in frontmatter
        idx = content.find("---", 3)
        if idx != -1:
            frontmatter = content[:idx]
            author_match = re.search(r'^author:', frontmatter, re.MULTILINE)
            if not author_match:
                content = content[:idx] + 'author: "Ghost Writer"\n' + content[idx:]
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
        
        # Extract title from content
        title = extract_title(post_content)
        
        slug = generate_slug(client, title)
        title = save_post(post_content, slug)
        
        # Write title to GITHUB_OUTPUT
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"post_title={title}\n")
                
    except Exception as e:
        print(f"::error::Error generating post: {e}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()