# Graduate Student Profiles Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish four new student profiles on the existing People page with supplied portraits and biographies.

**Architecture:** Keep `people.jemdoc` as the canonical content source and regenerate the tracked `people.html` artifact with the repository’s existing jemdoc command. Add standalone portrait assets under `data/`; no CSS, templates, or navigation changes are needed.

**Tech Stack:** jemdoc, static HTML, JPEG images, macOS `sips`, Git

---

## Chunk 1: Profile Assets and Page Update

### Task 1: Add portraits and profile cards

**Files:**
- Create: `data/nathan_constantinides.jpg`
- Create: `data/shaun_pexton.jpg`
- Create: `data/xicheng_tristan_wang.jpg`
- Create: `data/m_subhi_abo_rdan.jpeg`
- Modify: `people.jemdoc`
- Modify: `people.html`

- [ ] **Step 1: Prepare the four portrait assets**

Copy `/Users/hyzhou/Downloads/Nathan Constantinides - NSF- F-1-cropped.jpg` to `data/nathan_constantinides.jpg`, `/Users/hyzhou/Downloads/王希呈社媒图片.jpg` to `data/xicheng_tristan_wang.jpg`, and `/Users/hyzhou/Downloads/IMG_1475.jpeg` to `data/m_subhi_abo_rdan.jpeg` byte-for-byte. Create Shaun’s portrait from `/Users/hyzhou/Downloads/2U1A6819-CHOSEN.JPG` as a 2400-by-2400-pixel square crop beginning near x=1830 and y=500, adjusting only if visual inspection shows that his full head and upper torso are not centered. Do not modify any file in Downloads.

- [ ] **Step 2: Inspect the portrait assets**

Run `sips -g pixelWidth -g pixelHeight` on all four destination images. Expected: Nathan is square, Shaun remains square after any crop adjustment, and all four images have positive dimensions. Inspect Shaun’s crop visually and confirm that his full head and upper torso are visible and centered.

- [ ] **Step 3: Add the profile cards to the canonical source**

Insert four jemdoc image-table blocks in `people.jemdoc` after Kaavya Sahay and before Kuro. Use the names, titles, paragraph divisions, biography text, image filenames, 210-pixel widths, and ordering specified in `docs/superpowers/specs/2026-09-14-graduate-students-design.md`. Do not change existing profiles.

- [ ] **Step 4: Regenerate the static page**

Run `./jemdoc -c mysite.conf people.jemdoc`. Expected: exit status 0 and an updated `people.html` containing the four new cards.

- [ ] **Step 5: Verify generated content and structure**

Use focused text searches or a short read-only script to confirm each expected name, title, biography paragraph, and image path appears in `people.html`; confirm the new profiles appear in the order Nathan, Shaun, Tristan, Subhi between Kaavya and Kuro. Run a stack-based `HTMLParser` check that pushes non-void start tags, requires every end tag to match the current stack top, and asserts the stack is empty at EOF. Run `git diff --check`. Expected: all assertions and commands exit 0.

- [ ] **Step 6: Inspect the rendered page**

Open the local `people.html` page in a browser and inspect the Current Team section at desktop width. Expected: all four portraits load, each profile is readable, the cards remain aligned with the existing design, and Shaun’s crop shows his full head and upper torso at a useful scale.

- [ ] **Step 7: Review scope and commit the implementation**

Run `git status --short` and `git diff -- people.html`. Confirm only the four intended images and generated People page are included in the implementation commit; `people.jemdoc` is an intentionally ignored local source file in this repository. Preserve `data/harry_zhou_profile_202605.jpeg`, `tests/__pycache__/`, and any other unrelated files. Stage the five tracked implementation files and commit with message `Add graduate student profiles`.

- [ ] **Step 8: Publish and verify the live page**

Push `main` to `origin`, then compare `git rev-parse HEAD` with `git rev-parse origin/main`. Expected: the two commit hashes match. Open `https://zphy.github.io/people.html` after GitHub Pages updates and confirm all four names, titles, biographies, and portraits are present in the intended order. If the deployment is delayed, report the verified push separately from the still-pending live-page refresh rather than claiming publication is complete.
