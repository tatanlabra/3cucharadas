import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "style_manual_corpus.py"
SPEC = importlib.util.spec_from_file_location("style_manual_corpus", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class StyleManualCorpusTest(unittest.TestCase):
    def test_chunks_retain_page_provenance_and_overlap(self):
        chunks = MODULE.chunk_pages(["uno " * 70, "dos " * 70], 100, 10)
        self.assertEqual(2, len(chunks))
        self.assertEqual((1, 2), (chunks[0]["page_start"], chunks[0]["page_end"]))
        self.assertTrue(str(chunks[1]["text"]).startswith("dos "))

    def test_rejects_overlap_as_large_as_chunk(self):
        with self.assertRaises(ValueError):
            MODULE.chunk_pages(["texto"], 100, 100)

    def test_normalisation_removes_nulls_and_excess_blank_lines(self):
        self.assertEqual("a\n\nb", MODULE.normalise("a\x00\n\n\n b"))

    def test_repository_boundary_is_explicit(self):
        root = Path("/tmp/example-repository")
        self.assertTrue(MODULE.path_is_within(root / "private-corpus", root))
        self.assertFalse(MODULE.path_is_within(Path("/tmp/private-corpus"), root))


if __name__ == "__main__":
    unittest.main()
