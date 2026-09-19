# Design Direction

## Design Inspiration URL

Fallback: **Calm productivity app** (designmd.ai not accessed)

## What We Borrow

- **Layout:** Clean dashboard with organized card grid, clear visual hierarchy, generous whitespace
- **Spacing:** Consistent 8px/16px/24px rhythm, breathing room between sections, no cramped elements
- **Cards:** Subtle shadow/border, rounded corners (8–12px), hover elevation for interactive cards, clear content separation
- **Navigation:** Persistent sidebar or top nav with clear active states, logical grouping
- **Tables:** Readable row height (48px+), alternating row stripes, sortable headers, status badges
- **Forms:** Single-column layout, clear labels above inputs, helpful validation messages, generous tap targets

## What We Do Not Copy

- Any specific brand colors, logos, or illustrations from existing productivity apps
- Proprietary icon sets (use Bootstrap Icons instead)
- Exact layout measurements (adapt to our content needs)
- Dark mode as default (light mode primary, dark optional later)
- Complex animation systems (subtle transitions only)

## Visual Mood

**Student-friendly and calm** — professional campus feel, modern but approachable. Think university portal meets modern SaaS dashboard. Trustworthy, organized, not sterile.

**Keywords:** Clean, organized, readable, calm, trustworthy, student-accessible

## Layout Rules

### Global
- **Container max-width:** 1200px for dashboards, 720px for forms/detail pages
- **Grid:** 12-column Bootstrap grid, 24px gutter
- **Section spacing:** 32px between major sections, 16px between cards
- **Border radius:** 8px (cards), 6px (buttons/inputs), 4px (badges)
- **Shadows:** `0 2px 8px rgba(0,0,0,0.08)` for cards, `0 4px 16px rgba(0,0,0,0.12)` for modals/dropdowns

### Student Portal
- **Header:** Fixed top bar (56px) with logo, user menu, logout
- **Sidebar:** Collapsible left nav (240px expanded, 72px collapsed) on desktop; drawer on mobile
- **Content area:** 24px padding, card-based layout
- **Dashboard:** 4 stat cards (row), recent complaints table (card), quick action card

### Admin Portal
- **Header:** Fixed top bar with logo, admin badge, user menu
- **Sidebar:** Persistent left nav (260px) — Dashboard, Complaints, Statistics
- **Content:** 24px padding
- **Dashboard:** 5 stat cards (row), 2 charts side-by-side (cards), recent complaints table
- **Complaints list:** Toolbar (search + filters) + paginated table card
- **Detail view:** Two-column (info + actions) on desktop, stacked on mobile

## Color / Contrast Rules

### Palette
| Role | Hex | Usage |
|------|-----|-------|
| Primary | `#2563EB` (Blue 600) | Primary buttons, active nav, links, focus rings |
| Primary Hover | `#1D4ED8` (Blue 700) | Button hover |
| Primary Light | `#DBEAFE` (Blue 50) | Badge backgrounds, subtle accents |
| Success | `#059669` (Emerald 600) | Resolved status, success messages |
| Success Light | `#D1FAE5` | Resolved badge bg |
| Warning | `#D97706` (Amber 600) | In Progress status, warnings |
| Warning Light | `#FEF3C7` | In Progress badge bg |
| Danger | `#DC2626` (Red 600) | Rejected status, delete actions, errors |
| Danger Light | `#FEE2E2` | Rejected badge bg |
| Info | `#0891B2` (Cyan 600) | Under Review status, info messages |
| Info Light | `#CFFAFE` | Under Review badge bg |
| Gray 50 | `#F9FAFB` | Page background |
| Gray 100 | `#F3F4F6` | Card backgrounds, input backgrounds |
| Gray 200 | `#E5E7EB` | Borders, dividers |
| Gray 400 | `#9CA3AF` | Placeholder text, disabled states |
| Gray 600 | `#4B5563` | Secondary text, labels |
| Gray 900 | `#111827` | Primary text, headings |

### Contrast
- All text meets WCAG AA (4.5:1 for normal, 3:1 for large)
- Status badges use Light bg + 600 fg for 4.5:1+
- Focus rings: `0 0 0 3px rgba(37, 99, 235, 0.4)`

### Status Badge Colors
- **Submitted:** Gray 600 on Gray 100
- **Under Review:** Cyan 600 on Cyan 50
- **In Progress:** Amber 600 on Amber 50
- **Resolved:** Emerald 600 on Emerald 50
- **Rejected:** Red 600 on Red 50

### Priority Badge Colors
- **Low:** Gray 600 on Gray 100
- **Medium:** Blue 600 on Blue 50
- **High:** Orange 600 on Orange 50
- **Critical:** Red 600 on Red 50

## Typography Feel

- **Font Family:** System UI stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`) — no external font load
- **Scale:**
  - Display: 2.5rem (40px) — page titles only
  - H1: 1.875rem (30px) — dashboard titles
  - H2: 1.5rem (24px) — section headers
  - H3: 1.25rem (20px) — card titles
  - Body: 1rem (16px) — base
  - Small: 0.875rem (14px) — meta, labels
  - XS: 0.75rem (12px) — badges, timestamps
- **Line Height:** 1.5 (body), 1.25 (headings)
- **Font Weight:** 400 (normal), 500 (medium), 600 (semibold), 700 (bold)
- **Letter Spacing:** Normal, -0.02em for headings

## Component Style

### Buttons
| Variant | Style |
|---------|-------|
| Primary | Blue 600 bg, white text, 6px radius, 12px 24px padding, 500 weight |
| Primary Hover | Blue 700 bg, subtle shadow |
| Secondary | Gray 100 bg, Gray 900 text, Gray 300 border |
| Secondary Hover | Gray 200 bg |
| Danger | Red 600 bg, white text |
| Danger Hover | Red 700 bg |
| Ghost | Transparent bg, Blue 600 text, no border |
| Ghost Hover | Blue 50 bg |

### Inputs
- 40px height, 12px horizontal padding, Gray 200 border, Gray 300 hover, Primary focus ring
- Label: 14px, 500 weight, Gray 700, 6px margin-bottom
- Error: Red 500 border, Red 500 text (12px) below
- File upload: Drag-drop zone with dashed border, preview thumbnail

### Cards
- White bg, Gray 100 border (1px), 8px radius, 24px padding
- Header: H3 + optional action (right-aligned)
- Body: 16px spacing between elements
- Footer (optional): Gray 50 bg, 16px padding, -24px margin, rounded bottom

### Tables
- Striped rows (Gray 50), hover highlight (Blue 50)
- Header: 14px, 600 weight, Gray 600, 12px padding
- Cells: 14px, 16px padding, vertical-align middle
- Actions: Icon buttons (20px) with tooltip, grouped in dropdown on mobile

### Badges
- 6px radius, 10px 12px padding, 12px font, 500 weight
- Icon + text for status (optional)

### Forms
- Single column, 20px gap between fields
- Required marker: `*` in Red 500
- Submit: Primary button, full width on mobile, auto width on desktop
- Cancel: Secondary button

## Mobile Rules

### Breakpoints
- **Mobile:** < 576px (Bootstrap `sm`)
- **Tablet:** 576px – 991px (`md`)
- **Desktop:** ≥ 992px (`lg`)

### Student Mobile
- Sidebar → hamburger drawer (slide-in from left)
- Stat cards: 2 per row on ≥ 576px, 1 per row on < 576px
- Tables: Horizontal scroll with sticky first column (complaint ID)
- Forms: Full-width inputs, stacked buttons
- Complaint detail: Stacked sections, image full-width

### Admin Mobile
- Sidebar → bottom nav bar (Dashboard, Complaints, Profile) or drawer
- Dashboard stats: 2 per row
- Charts: Stacked, full-width
- Complaints table: Card-based list view (each row = card) on < 768px
- Detail view: Stacked, actions at bottom
- Filter toolbar: Collapsible accordion

### Touch Targets
- Minimum 44×44px for all interactive elements
- 8px gap between adjacent targets

## Accessibility Basics

- **Semantic HTML:** `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- **Heading hierarchy:** One H1 per page, logical H2/H3 nesting
- **Labels:** All inputs have `<label for="id">` or `aria-label`
- **Focus visible:** Custom focus ring on all interactive elements
- **Color not sole indicator:** Status badges have text + color; required fields have `*` + color
- **Alt text:** All images (complaint photos) have descriptive alt
- **ARIA:** `aria-expanded` on dropdowns, `aria-live` on toast/flash messages, `role="alert"` for errors
- **Keyboard:** Full navigation, skip link, modal trap focus
- **Language:** `lang="en"` on `<html>`

## Anti-Slop Rules

- No fake logos, brand marks, or university names — use generic "Campus Complaint System"
- No fake testimonials or user avatars — use initials or placeholder icons
- No fake statistics — all dashboard numbers come from real DB queries
- No "Lorem ipsum" — all placeholder text is meaningful (e.g., "Describe the issue...")
- One clear primary action per screen (Submit, Update, Save)
- Readable on 375px width (iPhone SE) — no horizontal scroll on content
- No auto-playing media, carousels, or parallax
- No cookie banners, newsletter popups, or chat widgets
- Loading states: skeleton screens for lists, spinner for actions
- Empty states: Illustrative icon + helpful text + primary action (e.g., "No complaints yet — Submit your first")

## Design Verification Checklist

- [ ] Light mode primary, all colors meet WCAG AA
- [ ] Student dashboard: 4 stat cards + recent table + quick action
- [ ] Admin dashboard: 5 stat cards + 2 charts + recent table
- [ ] Complaint submit form: category dropdown, location, description, image upload with preview
- [ ] Complaints list: search, filter (category/status/priority), pagination
- [ ] Complaint detail: read-only (student) / editable (admin) with status/priority/remarks
- [ ] Mobile: sidebar → drawer, tables → cards/list, forms stacked
- [ ] Focus rings visible on all interactive elements
- [ ] Status/priority badges use semantic colors + text
- [ ] Flash messages (success/error) dismissible, accessible
- [ ] Empty states for: no complaints, no search results, no image uploaded
- [ ] Loading states for: form submit, page transitions, image upload
- [ ] Consistent 8px spacing rhythm throughout
- [ ] No external font dependencies (system UI stack)
- [ ] Bootstrap Icons only (CDN)