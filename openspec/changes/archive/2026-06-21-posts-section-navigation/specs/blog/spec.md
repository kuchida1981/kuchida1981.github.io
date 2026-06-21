## MODIFIED Requirements

### Requirement: Blog Navigation
Users SHALL be able to navigate to the blog section from the main menu.

#### Scenario: Accessing Blog
- **WHEN** a user clicks the "Posts" link in the navigation menu
- **THEN** the system navigates to the blog post list page (`/posts/`)

#### Scenario: Archives menu item removed
- **WHEN** a user views the global navigation menu
- **THEN** the "Archives" menu item SHALL NOT be present
- **AND** only "Services" and "Posts" are displayed as menu items

## REMOVED Requirements

### Requirement: Archives Page
**Reason**: Archives の機能は Posts セクション内のナビゲーションブロックに統合されたため、独立したページとしては不要になった。
**Migration**: 年月別のアーカイブ閲覧は Posts ページ下部のナビゲーションブロックから `/posts/YYYY/MM/` 経由でアクセス可能。
