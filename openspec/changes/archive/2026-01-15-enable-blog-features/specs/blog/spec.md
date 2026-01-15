## ADDED Requirements

### Requirement: Blog Navigation
Users SHALL be able to navigate to the blog section from the main menu.

#### Scenario: Accessing Blog
- **WHEN** a user clicks the "Blog" link in the navigation menu
- **THEN** the system navigates to the blog post list page (`/posts/`)

### Requirement: Blog Content Display
The system SHALL display blog posts in a list format and allow viewing individual posts.

#### Scenario: Viewing Post List
- **WHEN** a user visits the blog section
- **THEN** a list of published posts is displayed

#### Scenario: Reading a Post
- **WHEN** a user clicks on a post title from the list
- **THEN** the full content of the post is displayed
