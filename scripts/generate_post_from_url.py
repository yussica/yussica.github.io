import os
import sys
import datetime
import re
import argparse
import requests
from bs4 import BeautifulSoup
from google import genai

def get_page_title_and_content(url):
    try:
        # Need to provide a user agent, otherwise some sites block the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.title.string if soup.title else "generated-post"
        
        # Sanitize title for filename
        safe_title = re.sub(r'[\\/\s:*?\"<>|]+', '-', title.strip()).strip('-')
        return safe_title[:100], content
    except Exception as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate blog post from URL")
    parser.add_argument("url", help="The URL to fetch content from")
    parser.add_argument("--lang", choices=["zh", "ja", "both"], default="zh", help="Output language")
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable is missing.")
        sys.exit(1)
        
    url = args.url
    lang_input = args.lang
    
    output_lang_map = {
        "zh": "Chinese",
        "ja": "Japanese",
        "both": "both Chinese and Japanese (bilingual, providing both language versions in the same post)"
    }
    output_lang = output_lang_map[lang_input]
    
    current_date = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S.000 %z")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    print(f"Fetching content from {url}...")
    page_title, html_content = get_page_title_and_content(url)
    
    if not page_title:
        page_title = "generated-post"
        
    prompt = f"""I have fetched the HTML content from the following URL: {url}.
Here is the raw content enclosed in XML tags: 
<content>
{html_content}
</content>

As a specialized Content Creator for a Japan-based money-saving ('撸羊毛') personal blog, please analyze the content above and generate a highly engaging blog post in {output_lang}.
The post must strictly follow these requirements:
1. Include Proper Jekyll front matter at the top:
---
layout: post
title: 【Catchy Title Here】
date: {current_date}
last_modified_at: {current_date}
category: 
author: 
tags: [Relevant Tags, e.g., 撸羊毛, 支付, 优惠]
summary: 
---

2. Structure the content logically:
- A clear summary of the deal, promotion, or core points.
- Step-by-step instructions on how to participate or get the reward.
- Key dates, deadlines, and any important conditions or caveats.
- The estimated exact value of the deal (in JPY or points).
- Embed links (with {{:target="_blank"}}) and images if appropriate.

3. Tone: Friendly, enthusiastic, and tailored to bargain hunters living in Tokyo/Japan. (If generating Japanese, use natural polite Japanese 'Desu/Masu' form).

Do NOT output any conversational text or markdown code blocks like ```markdown. Output ONLY the raw markdown content so it can be saved directly to a file."""

    print("Drafting the post with Gemini...")
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    generated_text = response.text
    
    # Clean up formatting to ensure it starts with front matter
    if '```markdown' in generated_text:
        generated_text = generated_text.replace('```markdown\n', '').replace('```', '')
    
    if '---' in generated_text:
        parts = generated_text.split('---', 2)
        if len(parts) >= 3:
            generated_text = '---' + parts[1] + '---' + parts[2]
            
    # Append the reference link
    generated_text = generated_text.strip()
    generated_text += f'\n\n---\n**参考链接:** [活动官方页面]({url}){{:target="_blank"}}\n'
    
    os.makedirs("_posts", exist_ok=True)
    filename = f"_posts/{today}-{page_title}.markdown"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generated_text)
        
    print(f"Success! The post has been saved to {filename}")

if __name__ == "__main__":
    main()
