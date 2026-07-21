"""Regression specification for the QEC syllabus on the teaching page."""

from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DRAFT = Path(
    "/Users/hyzhou/Documents/Faculty/Teaching/MIT-QEC-course-26/"
    "QEC_Syllabus_Working_Draft.md"
)

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

OVERVIEW = (
    "Develops the theory and practice of quantum error correction (QEC) and "
    "fault-tolerant quantum computation, with emphasis on recent developments. "
    "Begins with stabilizer codes and the Knill-Laflamme error-correction "
    "conditions, then outlines the full fault tolerance stack with surface codes, "
    "including lattice surgery, transversal gates, non-Clifford gates, and decoding. "
    "The second half of the course introduces high-rate quantum low-density "
    "parity-check codes and recent progress in logical gate design, concluding with "
    "examples of end-to-end fault-tolerant architecture design with resource "
    "estimation. Students simulate and benchmark QEC circuits, critique recent "
    "literature, and complete a research-style final project. Designed to introduce "
    "students to frontiers of QEC developments."
)

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


def normalized_whitespace(text: str) -> str:
    return " ".join(text.split())


def normalize_markdown_line(line: str) -> str:
    """Return the human-visible portion of one source-draft line."""
    line = line.strip()
    line = re.sub(r"^#{1,6}\s+", "", line)
    line = re.sub(r"^[-*+]\s+", "", line)
    line = re.sub(r"\s+https?://\S+\s*$", "", line)
    line = re.sub(r"(\*\*|__)(.*?)\1", r"\2", line)
    line = re.sub(r"(?<!\w)([*_])([^*_]+)\1(?!\w)", r"\2", line)
    return normalized_whitespace(line)


class PageParser(HTMLParser):
    """Collect rendered text, links, local assets, and basic tag-balance state."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.visible_fragments: list[str] = []
        self.links: list[str] = []
        self.anchor_pairs: list[tuple[str, str]] = []
        self.local_references: list[str] = []
        self.stack: list[str] = []
        self._hidden_depth = 0
        self._anchor_stack: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = dict(attrs)
        if tag not in VOID_ELEMENTS:
            self.stack.append(tag)
        if tag in {"script", "style"}:
            self._hidden_depth += 1
        if tag == "a" and attributes.get("href") is not None:
            href = attributes["href"]
            assert href is not None
            self.links.append(href)
            self._anchor_stack.append((href, []))
        self._collect_local_reference(attributes.get("href"))
        self._collect_local_reference(attributes.get("src"))

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        self._collect_local_reference(attributes.get("href"))
        self._collect_local_reference(attributes.get("src"))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style"}:
            self._hidden_depth -= 1
        if tag == "a" and self._anchor_stack:
            href, fragments = self._anchor_stack.pop()
            self.anchor_pairs.append((normalized_whitespace("".join(fragments)), href))
        if tag not in VOID_ELEMENTS:
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            else:
                self.stack.append(f"!unmatched:{tag}")

    def handle_data(self, data: str) -> None:
        if not self._hidden_depth:
            self.visible_fragments.append(data)
            for _, fragments in self._anchor_stack:
                fragments.append(data)

    def _collect_local_reference(self, value: str | None) -> None:
        if not value:
            return
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or value.startswith("/") or value.startswith("#"):
            return
        path = unquote(parsed.path)
        if path:
            self.local_references.append(path)


class TeachingSyllabusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parser = PageParser()
        parser.feed((ROOT / "teaching.html").read_text(encoding="utf-8"))
        parser.close()
        cls.visible_text = normalized_whitespace("".join(parser.visible_fragments))
        cls.links = parser.links
        cls.anchor_pairs = parser.anchor_pairs
        cls.local_references = parser.local_references
        cls.final_stack = parser.stack
        cls.draft_lines = [
            normalize_markdown_line(line)
            for line in DRAFT.read_text(encoding="utf-8").splitlines()
            if normalize_markdown_line(line)
        ]

    def test_html_structure_is_balanced(self) -> None:
        self.assertEqual([], self.final_stack)

    def test_existing_course_overview_is_preserved_exactly(self) -> None:
        self.assertIn(OVERVIEW, self.visible_text)

    def test_local_dependencies_resolve(self) -> None:
        for reference in self.local_references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

    def test_major_sections_and_all_weeks_are_present(self) -> None:
        sections = [
            "Course goals", "Intended audience", "Prerequisites (draft)",
            "Textbook and general references", "Weekly schedule (12 weeks)",
            "Weekly format", "Assessment", "Generative AI use",
            "Use in course materials", "Student use policy", "Prohibited uses",
        ] + [f"Week {week}:" for week in range(1, 13)]
        for section in sections:
            with self.subTest(section=section):
                self.assertIn(section, self.visible_text)

    def test_boundary_wording_and_assessment_weights_are_preserved(self) -> None:
        required = [
            "Week 11: Special topics and recent developments",
            "TBD based on recent developments in the field",
            "Prohibited uses may include:",
            "Problem sets: 20%", "Midterm: 35%", "Participation: 10%",
            "Final presentation: 35%",
        ]
        for wording in required:
            with self.subTest(wording=wording):
                self.assertIn(wording, self.visible_text)

    def test_each_draft_url_is_linked_exactly_once(self) -> None:
        self.assertEqual(25, len(EXPECTED_URLS))
        for url in EXPECTED_URLS:
            with self.subTest(url=url):
                self.assertEqual(1, self.links.count(url))

    def test_reference_descriptions_are_their_own_link_text(self) -> None:
        for source_line in DRAFT.read_text(encoding="utf-8").splitlines():
            url_match = re.search(r"(https?://\S+)\s*$", source_line)
            if not url_match:
                continue
            description = normalize_markdown_line(source_line)
            pair = (description, url_match.group(1))
            with self.subTest(description=description):
                self.assertIn(pair, self.anchor_pairs)

    def test_ordered_draft_content_is_rendered(self) -> None:
        expected_lines = list(self.draft_lines)
        self.assertEqual("QEC Course Syllabus", expected_lines[0])
        expected_lines[0] = "QEC Course Syllabus (Working Draft)"
        cursor = 0
        for line in expected_lines:
            found_at = self.visible_text.find(line, cursor)
            self.assertNotEqual(
                -1, found_at, msg=f"Missing or out-of-order draft line: {line!r}"
            )
            cursor = found_at + len(line)


if __name__ == "__main__":
    unittest.main()
