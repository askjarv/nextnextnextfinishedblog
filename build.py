#!/usr/bin/env python3
from __future__ import annotations

import html
import math
import re
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

import markdown
import yaml

POSTS_PER_PAGE = 5
SITE_TITLE = "Next...Next...Next...Finished"
SITE_DESCRIPTION = "A technical blog by some one in IT Security"
SITE_URL = "https://askjarv.github.io/nextnextnextfinishedblog"
STYLE_FILE = "style.css"
ASSETS_TO_COPY = ["images", "assets"]
DATE_FORMAT_DISPLAY = "%Y-%m-%d"

BASE_DIR = Path(__file__).parent.resolve()
CONTENT_DIR = BASE_DIR / "content"
OUTPUT_DIR = BASE_DIR / "docs"
POST_TEMPLATE_FILE = BASE_DIR / "template.html"
INDEX_TEMPLATE_FILE = BASE_DIR / "index_template.html"
README_FILE = BASE_DIR / "README.md"


@dataclass
class Post:
    source_path: Path
    title: str
    date: datetime
    tags: list[str] = field(default_factory=list)
    body_markdown: str = ""
    body_html: str = ""
    excerpt: str = ""
    slug: str = ""
    url: str = ""
    output_path: Path | None = None
    previous_post: "Post | None" = None
    next_post: "Post | None" = None


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "-", value)
    return value.strip("-") or "post"


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError("Missing or invalid YAML front matter.")
    yaml_text, body = match.groups()
    metadata = yaml.safe_load(yaml_text) or {}
    return metadata, body.strip()


def parse_date(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if value is None:
        raise ValueError("Missing 'date' field.")
    raw = str(value).strip()
    for fmt in (
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
    ):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {raw}")


def strip_html(html_text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


FIRST_PARAGRAPH_RE = re.compile(r"<p>(.*?)</p>", re.DOTALL | re.IGNORECASE)


def excerpt_from_first_paragraph(body_html: str, max_len: int = 280) -> str:
    match = FIRST_PARAGRAPH_RE.search(body_html)
    if match:
        text = strip_html(match.group(1))
    else:
        text = strip_html(body_html)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_template(template: str, values: dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace(f"{{{{ {key} }}}}", value)
    return result


def ensure_clean_output() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def copy_assets() -> None:
    for name in ASSETS_TO_COPY:
        src = BASE_DIR / name
        dst = OUTPUT_DIR / name
        if src.exists() and src.is_dir():
            shutil.copytree(src, dst)


def load_posts() -> list[Post]:
    if not CONTENT_DIR.exists():
        raise SystemExit(f"Missing content directory: {CONTENT_DIR}")

    md = markdown.Markdown(extensions=["extra", "tables", "fenced_code", "toc"])
    posts: list[Post] = []

    for path in sorted(CONTENT_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        metadata, body = parse_front_matter(raw)

        title = str(metadata.get("title", path.stem))
        date = parse_date(metadata.get("date"))
        tags = metadata.get("tags", []) or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        tags = [str(t) for t in tags]

        body_html = md.convert(body)
        md.reset()

        slug = slugify(path.stem)
        output_path = OUTPUT_DIR / "posts" / f"{slug}.html"
        posts.append(
            Post(
                source_path=path,
                title=title,
                date=date,
                tags=tags,
                body_markdown=body,
                body_html=body_html,
                excerpt=excerpt_from_first_paragraph(body_html),
                slug=slug,
                url=f"posts/{slug}.html",
                output_path=output_path,
            )
        )

    posts.sort(key=lambda p: p.date, reverse=True)
    for idx, post in enumerate(posts):
        if idx > 0:
            post.next_post = posts[idx - 1]
        if idx < len(posts) - 1:
            post.previous_post = posts[idx + 1]
    return posts


def render_tags(tags: list[str], prefix: str = "") -> str:
    if not tags:
        return ""
    return "".join(
        f'<a class="tag" href="{prefix}tags/{slugify(tag)}.html">{html.escape(tag)}</a>'
        for tag in tags
    )


def render_post_nav(post: Post) -> str:
    prev_html = (
        f'<a class="post-nav-link" href="../{post.previous_post.url}">&larr; Older: {html.escape(post.previous_post.title)}</a>'
        if post.previous_post
        else '<span class="post-nav-empty"></span>'
    )
    next_html = (
        f'<a class="post-nav-link align-right" href="../{post.next_post.url}">Newer: {html.escape(post.next_post.title)} &rarr;</a>'
        if post.next_post
        else '<span class="post-nav-empty"></span>'
    )
    return f'<nav class="post-nav">{prev_html}{next_html}</nav>'


def build_post_pages(posts: list[Post], post_template: str) -> None:
    posts_dir = OUTPUT_DIR / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)

    for post in posts:
        html_text = render_template(
            post_template,
            {
                "page_title": html.escape(post.title),
                "site_title": html.escape(SITE_TITLE),
                "title": html.escape(post.title),
                "date": post.date.strftime(DATE_FORMAT_DISPLAY),
                "tags": render_tags(post.tags, prefix="../"),
                "content": post.body_html,
                "home_link": "../index.html",
                "stylesheet_path": f"../{STYLE_FILE}",
                "post_nav": render_post_nav(post),
            },
        )
        assert post.output_path is not None
        post.output_path.write_text(html_text, encoding="utf-8")


def render_post_list(posts: list[Post], prefix: str = "") -> str:
    chunks = []
    for post in posts:
        chunks.append(
            f"""
<article class=\"post-card\">
  <h2><a href=\"{prefix}{post.url}\">{html.escape(post.title)}</a></h2>
  <div class=\"meta\"><time datetime=\"{post.date.strftime('%Y-%m-%d')}\">{post.date.strftime(DATE_FORMAT_DISPLAY)}</time></div>
  <div class=\"tags\">{render_tags(post.tags, prefix=prefix)}</div>
  <p>{html.escape(post.excerpt)}</p>
  <p><a class=\"read-more\" href=\"{prefix}{post.url}\">Read more</a></p>
</article>
""".strip()
        )
    return "\n".join(chunks)


def render_pagination(current_page: int, total_pages: int, prefix: str = "") -> str:
    if total_pages <= 1:
        return ""

    prev_link = ""
    next_link = ""

    if current_page > 1:
        prev_href = "index.html" if current_page - 1 == 1 else f"page/{current_page - 1}.html"
        prev_link = f'<a href="{prefix}{prev_href}">&larr; Newer</a>'
    else:
        prev_link = '<span class="disabled">&larr; Newer</span>'

    if current_page < total_pages:
        next_href = f"page/{current_page + 1}.html"
        next_link = f'<a href="{prefix}{next_href}">Older &rarr;</a>'
    else:
        next_link = '<span class="disabled">Older &rarr;</span>'

    return f'<nav class="pagination">{prev_link}<span>Page {current_page} of {total_pages}</span>{next_link}</nav>'


def build_index_pages(posts: list[Post], index_template: str) -> None:
    total_pages = max(1, math.ceil(len(posts) / POSTS_PER_PAGE))
    page_dir = OUTPUT_DIR / "page"
    page_dir.mkdir(parents=True, exist_ok=True)

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * POSTS_PER_PAGE
        page_posts = posts[start : start + POSTS_PER_PAGE]

        html_text = render_template(
            index_template,
            {
                "page_title": "Home",
                "site_title": html.escape(SITE_TITLE),
                "site_description": html.escape(SITE_DESCRIPTION),
                "header_link": "index.html" if page_num == 1 else "../index.html",
                "post_list": render_post_list(page_posts, prefix="" if page_num == 1 else "../"),
                "pagination": render_pagination(page_num, total_pages, prefix="" if page_num == 1 else "../"),
                "stylesheet_path": STYLE_FILE if page_num == 1 else f"../{STYLE_FILE}",
            },
        )

        output_file = OUTPUT_DIR / "index.html" if page_num == 1 else page_dir / f"{page_num}.html"
        output_file.write_text(html_text, encoding="utf-8")


def build_tag_pages(posts: list[Post], index_template: str) -> None:
    tags_dir = OUTPUT_DIR / "tags"
    tags_dir.mkdir(parents=True, exist_ok=True)

    tag_map: dict[str, list[Post]] = {}
    for post in posts:
        for tag in post.tags:
            tag_map.setdefault(tag, []).append(post)

    for tag, tagged_posts in sorted(tag_map.items(), key=lambda x: x[0].lower()):
        html_text = render_template(
            index_template,
            {
                "page_title": f"Tag: {html.escape(tag)}",
                "site_title": f"Posts tagged '{html.escape(tag)}'",
                "site_description": html.escape(SITE_DESCRIPTION),
                "header_link": "../index.html",
                "post_list": render_post_list(tagged_posts, prefix="../"),
                "pagination": "",
                "stylesheet_path": f"../{STYLE_FILE}",
            },
        )
        (tags_dir / f"{slugify(tag)}.html").write_text(html_text, encoding="utf-8")


def absolute_url(path: str) -> str:
    return SITE_URL.rstrip("/") + "/" + path.lstrip("/")


def build_rss(posts: list[Post]) -> None:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = SITE_TITLE
    ET.SubElement(channel, "link").text = SITE_URL
    ET.SubElement(channel, "description").text = SITE_DESCRIPTION
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.now(timezone.utc))
    ET.SubElement(channel, "generator").text = "build.py"

    for post in posts[:50]:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post.title
        ET.SubElement(item, "link").text = absolute_url(post.url)
        ET.SubElement(item, "guid").text = absolute_url(post.url)
        ET.SubElement(item, "pubDate").text = format_datetime(post.date.replace(tzinfo=timezone.utc))
        description = ET.SubElement(item, "description")
        description.text = post.excerpt
        for tag in post.tags:
            ET.SubElement(item, "category").text = tag

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    tree.write(OUTPUT_DIR / "rss.xml", encoding="utf-8", xml_declaration=True)


def write_supporting_files() -> None:
    shutil.copy2(BASE_DIR / STYLE_FILE, OUTPUT_DIR / STYLE_FILE)


def main() -> None:
    ensure_clean_output()
    copy_assets()
    write_supporting_files()

    post_template = load_template(POST_TEMPLATE_FILE)
    index_template = load_template(INDEX_TEMPLATE_FILE)

    posts = load_posts()
    build_post_pages(posts, post_template)
    build_index_pages(posts, index_template)
    build_tag_pages(posts, index_template)
    build_rss(posts)

    print(f"Built {len(posts)} posts into {OUTPUT_DIR}")
    print(f"Update SITE_URL in build.py before publishing RSS on GitHub Pages.")


if __name__ == "__main__":
    main()
