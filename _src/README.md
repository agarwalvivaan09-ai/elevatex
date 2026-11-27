# Website source

The pages in the repo root are generated. Edit these files instead, then rebuild:

```bash
python3 _src/build.py
```

- `pages/*.html`: each page's content. The comment at the top sets the title, the search description and which menu item is highlighted.
- `articles/articles.json`: the founder's notes and blog posts, word for word. Add a new blog post here, then add its key to the list in `build_articles()` in `build.py`.
- `gallery/albums.json`: the Gallery's albums. Each album has a group (`drives` or `events`), a title, a one-line description and its photos as `[file, description]`. The first photo is the album's cover. Add a photo by putting the file in `images/gallery/` and adding a line here.
- `build.py`: writes the shared header, phone menu and footer into every page, builds the Gallery and one page per album, makes the small previews in `images/thumbs/`, adds image sizes and lazy loading, and regenerates `sitemap.xml`.

## Images

All images live in `images/`:

| Folder | What's in it |
|---|---|
| `brand/` | the logo |
| `team/` | the team photo and member portraits |
| `drives/` | the main photo for each kind of drive |
| `events/` | event photos and posters |
| `gallery/` | Gallery photos (`elevatex-gallery-<album>-<n>.jpg`) |
| `hub/` | Volunteer Hub screenshots |
| `thumbs/` | small previews made by the build; don't edit by hand |
| `archive/` | older images no page uses, kept in case they're needed |

Image sizes and previews need Pillow (`pip install pillow`). Keep photos under about 1600 px on the long side so pages stay fast on phones.

## Look and feel

`styles.css` explains the design at the top. In short: one typeface (Archivo), wide and heavy for headings, plain white pages, trunk brown text, and banner yellow used only for small labels and highlights. Spacing only uses the scale in `:root` (`--s1` to `--s9`). Nothing fades in on scroll.

Writing on the site: plain sentences, straight quotes, no em dashes, and one name per action ("Join ElevateX", "Member login").

GitHub Pages doesn't publish this folder.
