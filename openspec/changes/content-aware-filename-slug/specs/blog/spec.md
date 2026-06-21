## MODIFIED Requirements

### Requirement: Automated Daily Content
The system SHALL automatically draft a blog post daily based on recent news, outputting the file to a year/month directory hierarchy with a content-aware filename slug. The author field SHALL be guaranteed by post-processing, not solely by LLM prompt instruction.

#### Scenario: Daily Draft Generation
- **WHEN** the scheduled time (e.g., daily) arrives
- **THEN** a new blog post file is created at `content/posts/YYYY/MM/YYYY-MM-DD-<slug>.md` where `<slug>` is a content-aware English slug generated from the post title
- **AND** the directory `content/posts/YYYY/MM/` is created if it does not exist
- **AND** the content is based on recent news or trends
- **AND** the author field in front matter is set to "Ghost Writer"
- **AND** a Pull Request is opened for user review

#### Scenario: Author Field Missing from LLM Output
- **WHEN** the LLM generates a blog post without an `author` field in the front matter
- **THEN** the save process SHALL insert `author: "Ghost Writer"` into the front matter before writing the file
