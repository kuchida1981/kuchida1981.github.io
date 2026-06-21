# filename-slug-generation Specification

## Purpose
Generate content-aware English filename slugs from Japanese blog post titles for automated daily posts.

## Requirements

### Requirement: Slug Generation from Title
The system SHALL generate an English URL slug from the Japanese blog post title using a separate Gemini API call after the blog post content is generated.

#### Scenario: Successful slug generation
- **WHEN** a blog post has been generated with a Japanese title
- **THEN** the system calls the Gemini API with the title to generate an English slug
- **AND** the slug consists of 2 to 6 English words in kebab-case
- **AND** the slug contains only lowercase ASCII alphanumeric characters and hyphens

#### Scenario: Slug generation API failure
- **WHEN** the Gemini API call for slug generation raises an exception
- **THEN** the system SHALL use `daily-news` as the fallback slug
- **AND** the blog post SHALL still be saved successfully

### Requirement: Slug Sanitization
The system SHALL sanitize the generated slug to ensure it is a valid filename component.

#### Scenario: Slug contains non-ASCII characters
- **WHEN** the generated slug contains non-ASCII characters (e.g., Japanese text)
- **THEN** the system SHALL remove all non-ASCII characters
- **AND** if the result is empty after removal, use `daily-news` as the fallback slug

#### Scenario: Slug exceeds word limit
- **WHEN** the generated slug contains more than 6 hyphen-separated words
- **THEN** the system SHALL truncate to the first 6 words

#### Scenario: Slug contains invalid characters
- **WHEN** the generated slug contains characters other than lowercase ASCII alphanumeric and hyphens
- **THEN** the system SHALL remove those characters
- **AND** collapse consecutive hyphens into a single hyphen
- **AND** strip leading and trailing hyphens
