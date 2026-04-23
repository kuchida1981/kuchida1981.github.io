# Design: Freelance Content Expansion

## Content Structure

### 1. About Page (`content/about.md`)
A static single page containing:
- Professional Bio
- Skillset (Technical stack)
- Experience/History
- Certifications

### 2. Services Page (`content/services.md`)
A static single page listing offerings:
- Web Application Development
- System Architecture Design
- Technical Consulting
- Pricing/Rates (optional/rough)

### 3. Works Section (`content/works/`)
A new content section (similar to `posts`) for portfolio items.
- `content/works/_index.md`: Section front matter (title "Works", etc.).
- `content/works/project-x.md`: Individual project case studies.
- Layout: List view (standard PaperMod list) showing project summaries/thumbnails.

## Configuration Changes (`config.yml`)

### Menu
Update the `main` menu to include:
- **About** (`/about/`) - Weight 1
- **Services** (`/services/`) - Weight 2
- **Works** (`/works/`) - Weight 3
- **Blog** (`/posts/`) - Weight 4 (Moved from 10)
- **Archives** (`/archives/`) - Weight 5 (Moved from 20)

### Profile Mode (Home)
Update `params.profileMode` to reflect the freelance engineer persona.
- **subtitle**: "Freelance Software Engineer / Full Stack Developer" (or similar Japanese text).
- **buttons**: Add shortcuts to "Works" or "Contact".

## Theme Considerations
- **PaperMod**: Standard layouts will be used. No custom HTML layouts required unless standard markdown proves insufficient.
- **Icons**: Ensure social icons (GitHub, X, Email) are configured in `params.socialIcons` (to be verified/added if missing).
