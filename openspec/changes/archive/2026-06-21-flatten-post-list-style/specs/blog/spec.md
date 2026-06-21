## MODIFIED Requirements

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
