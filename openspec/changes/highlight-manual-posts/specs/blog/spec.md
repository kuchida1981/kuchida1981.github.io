## ADDED Requirements

### Requirement: Highlight Manual Posts
The system SHALL distinguish between manual and automated blog posts in the article list and highlight manual posts visually.

#### Scenario: Visual Distinction of Manual Posts
- **WHEN** a user views the blog post list page
- **THEN** posts written by a human (where the author is the site owner or not "Ghost Writer") are rendered with a highlighted background color that adjusts dynamically for light and dark modes
- **AND** automated posts written by "Ghost Writer" are rendered with the default background style

## MODIFIED Requirements

### Requirement: Automated Daily Content
The system SHALL automatically draft a blog post daily based on recent news, setting the author metadata.

#### Scenario: Daily Draft Generation
- **WHEN** the scheduled time (e.g., daily) arrives
- **THEN** a new blog post file is created in the `content/posts` directory
- **AND** the content is based on recent news or trends
- **AND** the author field in front matter is set to "Ghost Writer"
- **AND** a Pull Request is opened for user review
