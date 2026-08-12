## ADDED Requirements

### Requirement: Related Posts Section
Individual post pages SHALL display a "関連記事" (related posts) section listing up to 5 other posts computed via Hugo's built-in Related Content feature, based on the current post's front matter.

#### Scenario: Post with related content shows links
- **WHEN** a user views an individual post page and Hugo's related-content calculation finds one or more related posts
- **THEN** a "関連記事" section is displayed listing up to 5 related posts, each linking to its permalink

#### Scenario: Post with no related content hides the section
- **WHEN** a user views an individual post page and Hugo's related-content calculation finds no related posts
- **THEN** the "関連記事" section is not rendered

#### Scenario: Related posts are not filtered by author
- **WHEN** the related-content calculation includes posts by different authors (including automated posts authored by "Ghost Writer")
- **THEN** those posts are still eligible to appear in the "関連記事" section, without any author-based filtering

### Requirement: Related Content Weighting Favors Tags Over Categories
The site's related-content configuration SHALL weight shared `tags` more heavily than shared `categories` when computing related posts, so that broad category overlap alone does not dominate the ranking.

#### Scenario: Shared tags rank a post higher than shared category alone
- **WHEN** two posts share one or more tags in addition to their category
- **THEN** they are ranked more related to each other than two posts that share only the same category with no overlapping tags
