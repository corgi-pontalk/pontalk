import sys
import os
import requests
import markdown
import re

# from dotenv import load_dotenv


# load_dotenv()

# 環境変数から読み込み (GitHub Secrets など)
# WP_URL = os.getenv('WP_URL')  # 例: https://asukacode.com
# WP_USER = os.getenv('WP_USER')
# WP_PASS = os.getenv('WP_PASS')
WP_URL = os.environ['WP_URL']  # 例: https://asukacode.com
WP_USER = os.environ['WP_USER']
WP_PASS = os.environ['WP_PASS']

def get_jwt_token():
    url = f"{WP_URL}/wp-json/jwt-auth/v1/token"
    response = requests.post(url, json={
        "username": WP_USER,
        "password": WP_PASS
    })
    response.raise_for_status()
    return response.json()["token"]

def fetch_terms(term_type):
    """カテゴリ or タグの一覧を取得"""
    url = f"{WP_URL}/wp-json/wp/v2/{term_type}?per_page=100"
    r = requests.get(url)
    r.raise_for_status()
    return {item["name"].lower(): item["id"] for item in r.json()}

def parse_markdown(file_path):
    """Markdown のフロントマターからタイトル、カテゴリ、タグを抜き出す"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    title_match = re.search(r'^# (.+)', text, re.MULTILINE)
    categories_match = re.search(r'Categories: (.+)', text)
    tags_match = re.search(r'Tags: (.+)', text)

    title = title_match.group(1) if title_match else "No title"
    categories = [c.strip().lower() for c in categories_match.group(1).split(",")] if categories_match else []
    tags = [t.strip().lower() for t in tags_match.group(1).split(",")] if tags_match else []

    # 本文を HTML に変換
    content_md = re.sub(r'^# .+\n', '', text, count=1).strip()
    lines = content_md.split('\n')
    content_ = ""
    excerpt = ""
    excerpt_flag = 0
    for line_ in lines:
        if line_.startswith("Categories: "):
            continue
        elif line_.startswith("Tags: "):
            continue
        elif "## Excerpt" in line_:
            excerpt_flag = 1
        elif excerpt_flag == 0:
            content_ += line_ + "\n"
        else:
            excerpt += line_ + "\n"

    configs = {
        'codehilite':{
            'noclasses': True
        }
    }
    content_html = markdown.markdown(
        content_,
        extensions=['fenced_code', 'codehilite'],
        extension_configs=configs
    )

    return title, categories, tags, excerpt, content_html

def post_to_wordpress(file_path):
    token = get_jwt_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 既存のカテゴリ・タグ一覧を取得
    category_map = fetch_terms("categories")
    tag_map = fetch_terms("tags")

    title, categories, tags, excerpt, content_html = parse_markdown(file_path)
    modified_categories = []
    for item in categories:
        modified_categories.append(item.replace('&', '&amp;'))

    modified_tags = []
    for item in tags:
        modified_tags.append(item.replace('&', '&amp;'))

    # 名前から ID に変換（なければ None を無視）
    category_ids = [category_map.get(c) for c in modified_categories if c in category_map]
    tag_ids = [tag_map.get(t) for t in modified_tags if t in tag_map]

    data = {
        "title": title,
        "status": "publish",
        "content": content_html,
        "categories": category_ids,
        "excerpt": excerpt,
        "tags": tag_ids
    }

    url = f"{WP_URL}/wp-json/wp/v2/posts"
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    print("✅ 投稿完了:", r.json()["link"])

if __name__ == "__main__":
    post_to_wordpress(sys.argv[1])

