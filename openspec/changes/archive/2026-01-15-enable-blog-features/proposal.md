# Change: Enable Blog Features

## Why
Currently, the site is configured primarily as a profile page (`profileMode: true`), and there is no accessible blog section or content. The user wants to enable blog functionality to start publishing posts.

## What Changes
- Add a "Blog" (or "Archives") link to the main navigation menu in `config.yml`.
- Create the standard Hugo post directory structure (`content/posts/`).
- Add a sample "Hello World" post to verify functionality.
- Ensure the blog list page is accessible at `/posts/`.

## Impact
- **Configuration**: Updates to `config.yml` to add menu items.
- **Content**: New directory `content/posts/` and new markdown files.
- **Specs**: New `blog` capability defining accessibility and content requirements.
