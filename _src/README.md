# Website source

The pages in the repo root are generated. Edit these files instead, then rebuild:

```bash
python3 _src/build.py
```

- `pages/*.html`: each page's content. The comment at the top sets the title, the search description and which menu item is highlighted.
- `articles/articles.json`: the founder's notes and blog posts, word for word. Add a new blog post here, then add its key to the list in `build_articles()` in `build.py`.
- `build.py`: writes the shared header, phone menu and footer into every page, adds image sizes and lazy loading, and regenerates `sitemap.xml`.

Image sizes need Pillow (`pip install pillow`). Keep photos under about 1600 px on the long side so pages stay fast on phones.

GitHub Pages doesn't publish this folder.
