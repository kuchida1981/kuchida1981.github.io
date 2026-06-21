# blog Specification

## Purpose
TBD - created by archiving change enable-blog-features. Update Purpose after archive.
## Requirements
### Requirement: Blog Navigation
Users SHALL be able to navigate to the blog section from the main menu.

#### Scenario: Accessing Blog
- **WHEN** a user clicks the "Blog" link in the navigation menu
- **THEN** the system navigates to the blog post list page (`/posts/`)

### Requirement: Blog Content Display
The system SHALL display blog posts in a list format and allow viewing individual posts. Posts stored in subdirectories under `content/posts/` SHALL be included in the list.

#### Scenario: Viewing Post List
- **WHEN** a user visits the blog section
- **THEN** a list of all published posts is displayed, including posts in `content/posts/YYYY/MM/` subdirectories

#### Scenario: Reading a Post
- **WHEN** a user clicks on a post title from the list
- **THEN** the full content of the post is displayed

### Requirement: Highlight Manual Posts
The system SHALL distinguish between manual and automated blog posts in the article list and highlight manual posts visually using a left border accent.

#### Scenario: Visual Distinction of Manual Posts
- **WHEN** a user views the blog post list page
- **THEN** posts written by a human (where the author is the site owner or not "Ghost Writer") are rendered with a left border accent color that adjusts for light and dark modes
- **AND** automated posts written by "Ghost Writer" are rendered without any border accent

#### Scenario: Flat List Layout
- **WHEN** a user views the blog post list page
- **THEN** all post entries are rendered without card-style background color, border, or border-radius
- **AND** entries are separated by vertical spacing only (no divider lines)
- **AND** the page background color is uniform (no contrast background behind the list)

### Requirement: Automated Daily Content
The system SHALL automatically draft a blog post daily based on recent news, outputting the file to a year/month directory hierarchy. The author field SHALL be guaranteed by post-processing, not solely by LLM prompt instruction.

#### Scenario: Daily Draft Generation
- **WHEN** the scheduled time (e.g., daily) arrives
- **THEN** a new blog post file is created at `content/posts/YYYY/MM/YYYY-MM-DD-daily-news.md`
- **AND** the directory `content/posts/YYYY/MM/` is created if it does not exist
- **AND** the content is based on recent news or trends
- **AND** the author field in front matter is set to "Ghost Writer"
- **AND** a Pull Request is opened for user review

#### Scenario: Author Field Missing from LLM Output
- **WHEN** the LLM generates a blog post without an `author` field in the front matter
- **THEN** the save process SHALL insert `author: "Ghost Writer"` into the front matter before writing the file

