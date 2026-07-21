# QEC Syllabus Website Design

## Goal

Publish `/Users/hyzhou/Documents/Faculty/Teaching/MIT-QEC-course-26/QEC_Syllabus_Working_Draft.md` on the existing Teaching page. Preserve the page's short introduction and the exact course-overview wording currently rendered in `teaching.html` so visitors can orient themselves before reading the detailed syllabus.

## Content and structure

The page will retain its current notice and overview, followed by the heading “QEC Course Syllabus (Working Draft).” The syllabus will reproduce the supplied draft's wording and ordering without paraphrase or omission. This fidelity requirement includes every goal, topic bullet, reference description and URL, weekly-format item, assessment weight, and generative-AI-policy paragraph. Week 11's “TBD based on recent developments in the field” and the policy's qualified “Prohibited uses may include:” wording are intentional and must remain unchanged.

The content divisions are:

- course goals, audience, prerequisites, and general references;
- the twelve-week schedule, including the references assigned to individual weeks;
- weekly format and assessment;
- the course policy on generative AI use.

External references will be rendered as descriptive clickable links. The existing site hierarchy will be used: section headings for major syllabus divisions, subheadings for individual weeks and policy subsections, and ordinary lists for goals, topics, references, and assessment weights.

## Implementation

`teaching.jemdoc` is the editable source of truth. Its overview will first be aligned with the exact wording currently rendered in `teaching.html`, then the syllabus will be added. The generated page will be produced with `./jemdoc -c mysite.conf teaching.jemdoc`. No JavaScript or new site-wide visual system is needed. CSS changes are out of scope unless rendering exposes a specific readability or mobile-layout problem.

## Verification

Verification will cover four points:

1. Regeneration succeeds twice. After normalizing only the generated footer timestamp, the two HTML outputs are byte-identical.
2. A source-to-output audit confirms that every heading, paragraph, list item, reference description, and URL from the draft appears in the rendered page without paraphrase or omission.
3. The HTML has balanced structural tags and all local asset references resolve.
4. The page remains readable at desktop and narrow mobile widths, with no unintended changes to other pages.

## Scope boundaries

This update does not create a separate course site, downloadable syllabus, interactive schedule, or new navigation entry. The syllabus remains explicitly presented as a working draft within the existing Teaching page.
