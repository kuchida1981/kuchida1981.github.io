## ADDED Requirements

### Requirement: Label AI-Generated Pull Requests
The system SHALL automatically label pull requests originating from the automated daily post workflow.

#### Scenario: PR is created for a daily post
- **GIVEN** the "Daily Automated Post" workflow is triggered
- **WHEN** the workflow successfully generates a new blog post and creates a pull request
- **THEN** the resulting pull request MUST have the `AI-generated` label applied.
- **AND** the resulting pull request MUST have the `automerge-24h` label applied.

### Requirement: Automatically Merge Labeled Pull Requests After a Delay
The system SHALL automatically merge pull requests that have a specific label after a 24-hour review period.

#### Scenario: An eligible PR is ready for merging
- **GIVEN** an open pull request exists with the `automerge-24h` label
- **AND** more than 24 hours have passed since the pull request was created
- **AND** all required branch protection checks (e.g., status checks) have passed
- **WHEN** the scheduled auto-merge workflow runs
- **THEN** the workflow SHALL merge the pull request.

#### Scenario: An eligible PR has failing checks
- **GIVEN** an open pull request exists with the `automerge-24h` label
- **AND** more than 24 hours have passed since the pull request was created
- **AND** at least one required branch protection check has not passed
- **WHEN** the scheduled auto-merge workflow runs
- **THEN** the workflow SHALL NOT merge the pull request.

#### Scenario: A PR is not yet 24 hours old
- **GIVEN** an open pull request exists with the `automerge-24h` label
- **AND** less than 24 hours have passed since the pull request was created
- **WHEN** the scheduled auto-merge workflow runs
- **THEN** the workflow SHALL NOT merge the pull request.
