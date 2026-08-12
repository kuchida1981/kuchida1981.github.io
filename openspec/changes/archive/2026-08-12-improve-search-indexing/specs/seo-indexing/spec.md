## ADDED Requirements

### Requirement: Robots.txt Generation
The system SHALL generate a `robots.txt` file at build time using Hugo's built-in robots.txt template, including a `Sitemap:` directive pointing at the site's `sitemap.xml`.

#### Scenario: Production build allows crawling
- **WHEN** the site is built in production (`hugo.IsProduction` is true, as in the GitHub Pages deploy workflow)
- **THEN** the generated `robots.txt` contains `Disallow:` (empty), permitting crawling
- **AND** the generated `robots.txt` contains a `Sitemap:` line pointing to the site's `sitemap.xml`

#### Scenario: Non-production build disallows crawling
- **WHEN** the site is built outside of production (e.g. a local preview build without the production environment set)
- **THEN** the generated `robots.txt` contains `Disallow: /`, blocking crawling

### Requirement: Site Description Reflects Actual Content
The site-wide description used in `<meta name="description">` and in the homepage's JSON-LD structured data SHALL describe the site's actual content, not a placeholder value.

#### Scenario: Homepage meta description matches configured value
- **WHEN** a user or crawler requests the site homepage
- **THEN** the `<meta name="description">` tag content equals the configured site description
- **AND** the content is not the placeholder value `Sandbox`

#### Scenario: JSON-LD description matches configured value
- **WHEN** a crawler parses the homepage's `application/ld+json` structured data
- **THEN** the `description` field equals the configured site description

### Requirement: IndexNow Notification on Content Publish
The system SHALL notify IndexNow-participating search engines of published or updated post URLs after a deploy triggered by a push to the default branch that changes files under `content/posts/`.

#### Scenario: Push with new or changed post triggers notification
- **WHEN** a push to the default branch adds or modifies one or more files under `content/posts/`
- **THEN** the corresponding public post URLs are submitted to the IndexNow endpoint after the site is deployed

#### Scenario: Push without post changes does not trigger notification
- **WHEN** a push to the default branch does not add or modify any file under `content/posts/`
- **THEN** no IndexNow notification is sent

#### Scenario: Non-push triggers do not send notifications
- **WHEN** the deploy workflow runs due to the scheduled 6-hourly trigger or a manual `workflow_dispatch`
- **THEN** no IndexNow notification is sent

#### Scenario: Notification failure does not block deployment
- **WHEN** the IndexNow notification request fails or times out
- **THEN** the GitHub Pages deployment still completes successfully
