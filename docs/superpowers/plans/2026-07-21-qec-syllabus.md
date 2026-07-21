# QEC Syllabus Website Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the complete QEC syllabus working draft beneath the existing overview on the Teaching page and produce a verified, reviewable HTML page.

**Architecture:** Keep `teaching.jemdoc` as the repository's editable source and use the bundled jemdoc generator to produce `teaching.html`. Add a focused standard-library regression test for the syllabus structure, representative exact content, link destinations, and local page dependencies; supplement it with a source-to-output completeness audit and browser checks.

**Tech Stack:** jemdoc, XHTML, Python standard-library `unittest` and `html.parser`, local browser

---

## File structure

- `teaching.jemdoc`: canonical Teaching page content, including the existing overview and new syllabus.
- `teaching.html`: generated browser-facing output; never hand-edit independently.
- `tests/test_teaching_syllabus.py`: focused regression checks for syllabus content and generated-page integrity.
- `docs/superpowers/specs/2026-07-21-qec-syllabus-design.md`: approved requirements and acceptance criteria.

## Chunk 1: Tested syllabus integration

### Task 1: Add failing syllabus regression coverage

**Files:**
- Create: `tests/test_teaching_syllabus.py`
- Read: `/Users/hyzhou/Documents/Faculty/Teaching/MIT-QEC-course-26/QEC_Syllabus_Working_Draft.md`
- Test: `tests/test_teaching_syllabus.py`

- [ ] **Step 1: Create the parser and normalization helpers**

Create a standard-library `unittest` module with:

- `ROOT = Path(__file__).resolve().parents[1]` and `DRAFT = Path("/Users/hyzhou/Documents/Faculty/Teaching/MIT-QEC-course-26/QEC_Syllabus_Working_Draft.md")`;
- a `PageParser(HTMLParser)` that appends data outside `script` and `style` elements to `text_parts`, records every anchor `href` in `links`, records relative `href` and `src` values in `local_references`, and maintains a stack for non-void start/end tags;
- `normalize_markdown_line()`, which removes heading/list prefixes, bold and italic markers, and a trailing bare URL while preserving the human-visible wording;
- `assert_ordered_draft_content()`, which searches the normalized visible page text from left to right for each nonempty normalized source line. Map the source title to `QEC Course Syllabus (Working Draft)` and require each subsequent match to begin after the prior one.

Use this complete URL inventory:

```python
EXPECTED_URLS = {
    "https://www.cs.umd.edu/~dgottesm/QECCbook-2026.pdf",
    "https://www.preskill.caltech.edu/ph229/",
    "https://arxiv.org/abs/quant-ph/0110143",
    "https://arxiv.org/abs/1208.0928",
    "https://arxiv.org/abs/2103.02202",
    "https://arxiv.org/abs/1808.02892",
    "https://arxiv.org/abs/2403.03272",
    "https://arxiv.org/abs/2204.13834",
    "https://arxiv.org/abs/quant-ph/0403025",
    "https://arxiv.org/abs/0811.4262",
    "https://arxiv.org/abs/2409.17595",
    "https://arxiv.org/abs/2303.15933",
    "https://arxiv.org/abs/1709.06218",
    "https://arxiv.org/abs/2506.01779",
    "https://arxiv.org/abs/2103.06309",
    "https://doi.org/10.1109/TIT.2013.2292061",
    "https://www.nature.com/articles/s41586-024-07107-7",
    "https://arxiv.org/abs/1311.0885",
    "https://arxiv.org/abs/2407.18393",
    "https://arxiv.org/abs/2503.10390",
    "https://arxiv.org/abs/2110.10794",
    "https://arxiv.org/abs/1905.09749",
    "https://dl.acm.org/doi/10.1145/3695053.3731039",
    "https://arxiv.org/abs/2602.11457",
    "https://arxiv.org/abs/2603.28627",
}
```

Implement the parser and normalization helpers as follows (the test class may call them directly or wrap them in assertion methods):

```python
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(
    "/Users/hyzhou/Documents/Faculty/Teaching/MIT-QEC-course-26/"
    "QEC_Syllabus_Working_Draft.md"
)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.text_parts = []
        self.links = []
        self.anchor_pairs = []
        self.current_anchor_href = None
        self.current_anchor_text = []
        self.local_references = []
        self.hidden_depth = 0

    def _record_attributes(self, attrs):
        for name, value in attrs:
            if not value or name not in {"href", "src"}:
                continue
            if name == "href":
                self.links.append(value)
            parsed = urlparse(value)
            if not parsed.scheme and not parsed.netloc and not value.startswith("#"):
                self.local_references.append(value)

    def handle_starttag(self, tag, attrs):
        self._record_attributes(attrs)
        if tag == "a":
            self.current_anchor_href = dict(attrs).get("href")
            self.current_anchor_text = []
        if tag not in VOID_TAGS:
            self.stack.append(tag)
        if tag in {"script", "style"}:
            self.hidden_depth += 1

    def handle_startendtag(self, tag, attrs):
        self._record_attributes(attrs)

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden_depth -= 1
        if tag == "a":
            anchor_text = re.sub(r"\s+", " ", "".join(self.current_anchor_text)).strip()
            self.anchor_pairs.append((anchor_text, self.current_anchor_href))
            self.current_anchor_href = None
            self.current_anchor_text = []
        if tag not in VOID_TAGS:
            if not self.stack or self.stack[-1] != tag:
                raise AssertionError(f"mismatched closing tag: {tag}; stack={self.stack}")
            self.stack.pop()

    def handle_data(self, data):
        if not self.hidden_depth and data:
            self.text_parts.append(data)
            if self.current_anchor_href is not None:
                self.current_anchor_text.append(data)


def normalize_markdown_line(line):
    normalized = re.sub(r"^(?:#+|-)[ ]+", "", line.strip())
    normalized = normalized.replace("**", "").replace("*", "")
    normalized = re.sub(r"[ ]+https?://\S+$", "", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def assert_ordered_draft_content(test_case, visible_text, draft_text):
    cursor = 0
    for index, source_line in enumerate(draft_text.splitlines()):
        expected = normalize_markdown_line(source_line)
        if not expected:
            continue
        if index == 0:
            expected = "QEC Course Syllabus (Working Draft)"
        position = visible_text.find(expected, cursor)
        test_case.assertNotEqual(position, -1, f"missing or out of order: {expected}")
        cursor = position + len(expected)
```

- [ ] **Step 2: Add the test fixture setup and baseline integrity tests**

Append this constant and class scaffold after the helpers:

```python
EXPECTED_OVERVIEW = (
    "Develops the theory and practice of quantum error correction (QEC) and "
    "fault-tolerant quantum computation, with emphasis on recent developments. "
    "Begins with stabilizer codes and the Knill-Laflamme error-correction "
    "conditions, then outlines the full fault tolerance stack with surface "
    "codes, including lattice surgery, transversal gates, non-Clifford gates, "
    "and decoding. The second half of the course introduces high-rate quantum "
    "low-density parity-check codes and recent progress in logical gate design, "
    "concluding with examples of end-to-end fault-tolerant architecture design "
    "with resource estimation. Students simulate and benchmark QEC circuits, "
    "critique recent literature, and complete a research-style final project. "
    "Designed to introduce students to frontiers of QEC developments."
)


class TeachingSyllabusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = PageParser()
        parser.feed((ROOT / "teaching.html").read_text(encoding="utf-8"))
        cls.visible_text = re.sub(r"\s+", " ", "".join(parser.text_parts)).strip()
        cls.links = parser.links
        cls.anchor_pairs = parser.anchor_pairs
        cls.local_references = parser.local_references
        cls.final_stack = parser.stack

    def test_html_structure_is_balanced(self):
        self.assertEqual(self.final_stack, [])

    def test_existing_overview_is_preserved(self):
        self.assertIn(EXPECTED_OVERVIEW, self.visible_text)

    def test_local_dependencies_resolve(self):
        for reference in self.local_references:
            self.assertTrue((ROOT / reference).is_file(), reference)
```

- [ ] **Step 3: Add syllabus structure and boundary tests**

Append these methods to `TeachingSyllabusTest`:

```python
    def test_all_syllabus_sections_and_weeks_are_rendered(self):
        expected = [
            "QEC Course Syllabus (Working Draft)",
            "Course goals",
            "Intended audience",
            "Prerequisites (draft)",
            "Textbook and general references",
            "Weekly schedule (12 weeks)",
            *[f"Week {week}:" for week in range(1, 13)],
            "Weekly format",
            "Assessment",
            "Generative AI use",
            "Use in course materials",
            "Student use policy",
            "Prohibited uses",
        ]
        for text in expected:
            self.assertIn(text, self.visible_text)

    def test_boundary_wording_is_preserved(self):
        for text in [
            "TBD based on recent developments in the field",
            "Prohibited uses may include:",
            "Problem sets: 20%",
            "Midterm: 35%",
            "Participation: 10%",
            "Final presentation: 35%",
        ]:
            self.assertIn(text, self.visible_text)
```

- [ ] **Step 4: Add link-pairing and full-draft fidelity tests**

Append these methods to `TeachingSyllabusTest`:

```python
    def test_reference_urls_are_clickable_once(self):
        counts = Counter(self.links)
        for url in EXPECTED_URLS:
            self.assertEqual(counts[url], 1, url)

    def test_reference_descriptions_link_to_their_urls(self):
        self.assertTrue(DRAFT.is_file(), DRAFT)
        for source_line in DRAFT.read_text(encoding="utf-8").splitlines():
            match = re.search(r"(https?://\S+)$", source_line)
            if match:
                expected = (normalize_markdown_line(source_line), match.group(1))
                self.assertIn(expected, self.anchor_pairs)

    def test_full_draft_wording_and_order(self):
        self.assertTrue(DRAFT.is_file(), DRAFT)
        assert_ordered_draft_content(
            self, self.visible_text, DRAFT.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 5: Run the test to verify RED**

Run: `python -m unittest tests/test_teaching_syllabus.py -v`

Expected: the new syllabus assertions fail because the generated page currently contains only the short overview. The pre-existing overview and local-dependency checks should pass.

- [ ] **Step 6: Commit the RED phase**

```bash
git add tests/test_teaching_syllabus.py
git commit -m "test: specify QEC syllabus page content"
```

### Task 2: Add the complete syllabus and regenerate the page

**Files:**
- Modify: `teaching.jemdoc`
- Modify: `teaching.html`
- Test: `tests/test_teaching_syllabus.py`

- [ ] **Step 1: Align the canonical overview**

Replace the overview in `teaching.jemdoc` with the exact `EXPECTED_OVERVIEW` paragraph from Task 1. This changes “This course develops” to “Develops” and “The course begins” to “Begins,” preserving the current rendered page word for word.

- [ ] **Step 2: Add the syllabus title and course information**

After the overview, add `== QEC Course Syllabus (Working Draft)`, then reproduce the course goals, intended audience, prerequisites, and general references in their original order. Use jemdoc headings and lists. Render each general-reference URL as a link whose text is the complete reference description; do not show a bare URL or alter the supplied prose.

- [ ] **Step 3: Add Weeks 1 through 6**

Reproduce the weekly-schedule heading and Weeks 1 through 6 in their original order. Use a subheading for each week, lists for topic bullets, and a bold `Key references:` label followed by linked reference descriptions.

- [ ] **Step 4: Add Weeks 7 through 12**

Reproduce Weeks 7 through 12 in their original order using the same structure. Preserve Week 11's `TBD based on recent developments in the field` wording exactly.

- [ ] **Step 5: Add format, assessment, and AI-use policy**

Reproduce the weekly format, assessment weights, and all generative-AI-policy subsections in their original order. Preserve `Prohibited uses may include:` and every prohibited-use bullet exactly.

- [ ] **Step 6: Regenerate the HTML**

Run: `./jemdoc -c mysite.conf teaching.jemdoc`

Expected: exit status 0 and an updated `teaching.html` containing the complete syllabus.

- [ ] **Step 7: Run the regression test to verify GREEN**

Run: `python -m unittest tests/test_teaching_syllabus.py -v`

Expected: all tests pass.

- [ ] **Step 8: Audit complete draft reproduction**

Run the committed full-draft test directly:

`python -m unittest tests.test_teaching_syllabus.TeachingSyllabusTest.test_full_draft_wording_and_order -v`

The helper examines every nonempty source line in order, stripping only Markdown presentation markers and trailing URLs. The URL test separately checks every source URL exactly once through HTML `href` values. Expected: PASS, with only the explicitly mapped “(Working Draft)” title suffix differing from the source.

- [ ] **Step 9: Verify deterministic generation**

Run:

```bash
cp teaching.html /tmp/teaching-first.html
sleep 2
./jemdoc -c mysite.conf teaching.jemdoc
python -c 'from pathlib import Path; import re; norm=lambda value: re.sub(r"Page generated .*?, by", "Page generated TIMESTAMP, by", value); first=norm(Path("/tmp/teaching-first.html").read_text()); second=norm(Path("teaching.html").read_text()); assert first == second'
```

Expected: no differences after footer timestamp normalization.

- [ ] **Step 10: Commit the GREEN phase**

```bash
git add teaching.jemdoc teaching.html
git commit -m "feat: publish QEC syllabus working draft"
```

### Task 3: Verify the rendered page and repository state

**Files:**
- Verify: `teaching.html`
- Verify: `jemdoc.css`

- [ ] **Step 1: Run structural checks**

Run `python -m unittest tests/test_teaching_syllabus.py -v` and `git diff --check HEAD~2..HEAD`. The committed parser test maintains a stack for all non-void structural tags, fails immediately on a mismatched closing tag, and asserts the final stack is empty.

Expected: all tests pass, no whitespace errors, and no unbalanced structural tags.

- [ ] **Step 2: Inspect desktop and mobile rendering**

Open `teaching.html` locally. Inspect the whole page at a desktop viewport and near 390 px width. Confirm heading hierarchy, list indentation, link wrapping, navigation, and absence of horizontal overflow. Do not change CSS unless a concrete defect is visible.

- [ ] **Step 3: Open the final page for user review**

Navigate the local browser to the absolute `teaching.html` path and leave it open for the user.

- [ ] **Step 4: Confirm repository scope**

Run: `git diff --name-only HEAD~2..HEAD`

Expected: only `tests/test_teaching_syllabus.py`, `teaching.jemdoc`, and `teaching.html`. Confirm separately that unrelated pre-existing untracked files remain untouched.

- [ ] **Step 5: Report the result**

Summarize the files changed, the exact verification performed, the commits created, and any known limitations. Preserve unrelated untracked files and do not push unless requested.
