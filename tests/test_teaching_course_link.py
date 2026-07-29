from pathlib import Path
import unittest


class TeachingCourseLinkTest(unittest.TestCase):
    def test_course_number_links_to_official_mit_subject_entry(self):
        generated = Path("teaching.html").read_text()
        self.assertIn(
            '<a href="https://www.eecs.mit.edu/academics/subject-updates/subject-updates-fall-2026/#6_S980">6.S980</a>',
            generated,
        )


if __name__ == "__main__":
    unittest.main()
