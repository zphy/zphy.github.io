# Graduate Student Profiles

## Scope

Add Nathan Constantinides and Shaun Pexton to the existing “Current Team” section of the People page. Preserve the page’s current jemdoc card structure and styling.

## Content

Each profile will contain the student’s full name, the title “PhD Student,” and the biography supplied by the user. Nathan’s biography will be one paragraph. Shaun’s biography will remain two paragraphs. Markdown emphasis and escaped blank-line markers from the request are input formatting, not page content.

The profiles will appear after Kaavya Sahay and before Kuro. Nathan will appear before Shaun, following the order in which the profiles were supplied.

## Images

Copy Nathan’s supplied square portrait into `data/` under a descriptive lowercase filename. Create a square crop of Shaun’s supplied landscape photograph, centered on Shaun, and save it under a descriptive lowercase filename in `data/`. Do not modify the source files in Downloads. Both page entries will use the existing 210-pixel image width.

## Generation and Verification

Edit the canonical `people.jemdoc` source and regenerate `people.html` with the repository’s jemdoc command. Verify that both generated cards contain the correct names, titles, biographies, image paths, ordering, and balanced HTML structure. Check both image files and inspect the rendered page visually. Run `git diff --check` and preserve unrelated working-tree files.
