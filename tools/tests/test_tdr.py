"""Tests for tools/tdr.py. Run: python tools/tests/test_tdr.py"""
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
REPO = TOOLS.parent
EXAMPLE = REPO / "examples" / "wall-shelf"
sys.path.insert(0, str(TOOLS))
import tdr  # noqa: E402


def cli(*args):
    """Run main() in process; return (exit code, stdout)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = tdr.main(list(args))
    return code, buf.getvalue()


def codes(out):
    return {line.split()[0] for line in out.splitlines() if line[:1] == "E"}


class YamlTests(unittest.TestCase):
    def test_accepts_subset(self):
        text = (
            "# comment\n"
            "kind: demo\n"
            "  # indented full-line comment\n"
            "n: 3\n"
            "f: -1.5e3\n"
            "b: true\n"
            "z: null\n"
            "date: 2026-10-20\n"
            "s1: 'it''s'\n"
            's2: "a \\"q\\" \\\\ \\n end"\n'
            "hash: 'a # b'\n"
            "lit: |\n"
            "  line one\n"
            "  # not a comment\n"
            "\n"
            "  line two\n"
            "strip: |-\n"
            "  x\n"
            "  y\n"
            "empty:\n"
            "items:\n"
            "- plain\n"
            "-   key: v\n"
            "    other: 2\n"
            "    nested:\n"
            "      deep:\n"
            "        - a\n"
            "        - b\n"
            "  # comment between\n"
            "- k2: x\n"
        )
        d = tdr.load_yaml(text)
        self.assertEqual(d["n"], 3)
        self.assertEqual(d["f"], -1500.0)
        self.assertIs(d["b"], True)
        self.assertIsNone(d["z"])
        self.assertEqual(d["date"], "2026-10-20")
        self.assertEqual(d["s1"], "it's")
        self.assertEqual(d["s2"], 'a "q" \\ \n end')
        self.assertEqual(d["hash"], "a # b")
        self.assertEqual(d["lit"], "line one\n# not a comment\n\nline two\n")
        self.assertEqual(d["strip"], "x\ny")
        self.assertIsNone(d["empty"])
        self.assertEqual(d["items"][0], "plain")
        self.assertEqual(d["items"][1]["nested"]["deep"], ["a", "b"])
        self.assertEqual(d["items"][2], {"k2": "x"})
        self.assertEqual(d["items"][1].at("other"), 24)

    def test_refusals_carry_line_numbers(self):
        cases = [
            ("a: 1\n\tb: 2\n", 2),
            ("a: {x: 1}\n", 1),
            ("ok: 1\nb: [1, 2]\n", 2),
            ("a: &x 1\n", 1),
            ("a: *x\n", 1),
            ("a: !tag 1\n", 1),
            ("---\na: 1\n", 1),
            ("a: 1\n...\n", 2),
            ("a: 1\nb: 2\na: 3\n", 3),
            ("a: x: y\n", 1),
            ("a: 1\n  b: 2\n", 2),
            ("m:\n  a: 1\n   b: 2\n", 3),
            ("a: 'open\n", 1),
            ("a: >\n  folded\n", 1),
            ("ok: 1\ntext: 30 # tentative\n", 2),
            ("a: 'x' # c\n", 1),
            ('a: "x" # c\n', 1),
            ("a: # c\n  b: 1\n", 1),
            ("a: | # c\n  b\n", 1),
            ("l:\n  - x # c\n", 2),
        ]
        for text, line in cases:
            with self.subTest(text=text):
                with self.assertRaises(tdr.YErr) as cm:
                    tdr.load_yaml(text)
                self.assertEqual(cm.exception.line, line)

    def test_e01_in_record(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "record").mkdir()
            (Path(t) / "record" / "values.yaml").write_text(
                "kind: value\nschema: 1\nitems:\n  - key: a.b\n    v: [1]\n")
            rec = tdr.Record(t)
            self.assertEqual(rec.problems[0][:3], ("E01", "record/values.yaml", 5))


class Fixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "r"
        shutil.copytree(EXAMPLE, self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def mutate(self, rel, old, new, count=1):
        p = self.root / rel
        s = p.read_text(encoding="utf-8")
        self.assertIn(old, s)
        p.write_text(s.replace(old, new, count), encoding="utf-8", newline="\n")

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")

    def check(self, *extra):
        return cli("check", "--root", str(self.root), *extra)


class ExampleTests(Fixture):
    def test_example_passes(self):
        code, out = self.check()
        self.assertEqual((code, out.strip()), (0, "ok"))

    def test_status_is_byte_exact(self):
        want = (self.root / "STATUS.md").read_bytes()
        (self.root / "STATUS.md").unlink()
        cli("status", "--root", str(self.root))
        self.assertEqual((self.root / "STATUS.md").read_bytes(), want)

    def test_e02(self):
        self.mutate("record/decisions.yaml", "id: D-002", "id: D-001")
        self.assertIn("E02", codes(self.check()[1]))

    def test_e03(self):
        self.mutate("record/requirements.yaml", "- D-002", "- D-099")
        self.assertIn("E03", codes(self.check()[1]))

    def test_e05(self):
        self.mutate("record/values.yaml", "status: decided", "status: measured")
        self.assertIn("E05", codes(self.check()[1]))

    def test_e06(self):
        with (self.root / "record" / "sources.yaml").open("a", newline="\n") as f:
            f.write("  - id: F1\n    class: F\n    title: A forum thread\n"
                    "    license: unknown\n    read: not_read\n")
        self.mutate("record/requirements.yaml",
                    "      - D-001\n    status: confirmed\n    parts:\n      - board\n      - bracket",
                    "      - F1\n    status: confirmed\n    parts:\n      - board\n      - bracket")
        self.assertIn("E06", codes(self.check()[1]))

    def test_e07(self):
        self.mutate("record/requirements.yaml",
                    "    design_point: Carry shelf.load_n at mid-span.\n", "")
        self.assertIn("E07", codes(self.check()[1]))

    def test_e08(self):
        self.mutate("record/requirements.yaml", "verify: analysis", "verify: guess")
        self.assertIn("E08", codes(self.check()[1]))

    def test_e13_never_prints_the_name(self):
        secret = "zebra-secret-name"
        with (self.root / "README.md").open("a", newline="\n") as f:
            f.write(f"\nThe {secret.upper()} appears here.\n")
        names = Path(self._tmp.name) / "names.txt"
        names.write_text("# private\n\nother\n" + secret + "\n", encoding="utf-8")
        code, out = self.check("--private-names", str(names))
        self.assertEqual(code, 1)
        self.assertIn("E13 README.md:", out)
        self.assertIn("private name #4", out)
        self.assertNotIn(secret, out.lower())

    def test_e15(self):
        self.write("record/shared.yaml", "kind: citation\nschema: 1\nitems:\n"
                   "  - ref: owner/repo#ID\n    used_for:\n      - R-01\n")
        self.assertIn("E15", codes(self.check()[1]))

    def test_e19(self):
        self.write("record/config/B-01.yaml", "kind: baseline\nschema: 1\nitems:\n"
                   "  - id: B-01\n    kind: as_built\n    date: 2026-10-23\n    decision: D-001\n"
                   "    deviations:\n      - key: board.width_mm\n        design: 200\n"
                   "        built: 195\n        decision: D-099\n")
        self.assertIn("E19", codes(self.check()[1]))

    def test_e22(self):
        cases = [
            ("origin: owner", "origin: nobody"),
            ("id: R-01", "id: X-1"),
        ]
        for old, new in cases:
            with self.subTest(old=old):
                self.mutate("record/requirements.yaml", old, new)
                self.assertIn("E22", codes(self.check()[1]))
                self.mutate("record/requirements.yaml", new, old)
        self.mutate("record/decisions.yaml", "date: 2026-10-20", "date: 20/10/2026")
        self.assertIn("E22", codes(self.check()[1]))
        self.mutate("record/decisions.yaml", "date: 20/10/2026", "date: 2026-10-20")
        self.mutate("record/sources.yaml", "class: P", "class: S")
        self.assertIn("E22", codes(self.check()[1]))
        self.mutate("record/sources.yaml", "class: S", "class: P")
        self.mutate("record/requirements.yaml", "    text: The shelf carries its design load without failure.\n", "")
        self.assertIn("E22", codes(self.check()[1]))

    def test_e21(self):
        self.mutate("record/requirements.yaml", "    origin: owner\n",
                    "    origin: owner\n    bogus: 1\n")
        self.assertIn("E21", codes(self.check()[1]))

    def test_e10_stale_status_and_table(self):
        self.mutate("record/values.yaml", "v: 18", "v: 19")
        self.assertIn("E10", codes(self.check()[1]))

    def test_gates(self):
        code, out = self.check("--gate", "build_operate")
        self.assertEqual(code, 1)
        self.assertTrue({"E20", "E09"} <= codes(out))

    def test_get_refs_brief(self):
        code, out = cli("get", "R-02", "--root", str(self.root))
        self.assertEqual(code, 0)
        self.assertIn("basis D-002:", out)
        code, out = cli("refs", "D-001", "--root", str(self.root))
        self.assertIn("requirement R-01 basis", out)
        code, out = cli("brief", "board", "--root", str(self.root))
        self.assertIn("board.modulus_mpa", out)
        self.assertIn("I-01", out)
        self.assertIn("Q-001", out)
        self.assertEqual(cli("get", "nope", "--root", str(self.root))[0], 1)

    def test_tier(self):
        def run(msg):
            m = Path(self._tmp.name) / "msg.txt"
            m.write_text(msg, encoding="utf-8")
            return cli("tier", "--message", str(m), "--root", str(self.root))
        self.assertEqual(run("Tier: T1\n")[0], 0)
        self.assertIn("E11", run("Fix a thing\n")[1])
        self.assertIn("E11", run("Tier: T9\n")[1])
        self.assertIn("E11", run("Tier: T2\n")[1])
        self.assertIn("E11", run("Tier: T2\nChecks: K-404\n")[1])
        self.assertEqual(run("Tier: T2\nChecks: K-001\n")[0], 0)
        self.assertIn("E12", run("Tier: T3\n")[1])
        self.assertIn("E12", run("Tier: T3\nDecision: D-404\n")[1])
        self.assertEqual(run("Tier: T3\nDecision: D-001\n")[0], 0)


class EmptyRecordTests(unittest.TestCase):
    def test_all_empty_items_pass(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for kind in tdr.KINDFILES:
                p = root / "record" / f"{kind}.yaml"
                p.parent.mkdir(exist_ok=True)
                p.write_text(f"kind: {kind}\nschema: 1\nitems:\n", encoding="utf-8")
            code, out = cli("status", "--root", t)
            self.assertEqual(code, 0)
            self.assertTrue((root / "STATUS.md").is_file())
            code, out = cli("check", "--root", t)
            self.assertEqual((code, out.strip()), (0, "ok"))


class McpTests(unittest.TestCase):
    def test_round_trip(self):
        msgs = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-03-26", "capabilities": {}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "tdr_get", "arguments": {"id": "R-02"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "tdr_check", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 5, "method": "nope"},
        ]
        r = subprocess.run([sys.executable, str(TOOLS / "tdr.py"), "mcp", "--root", str(EXAMPLE)],
                           input="\n".join(json.dumps(m) for m in msgs) + "\n",
                           capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = [json.loads(l) for l in r.stdout.splitlines()]
        self.assertEqual([o["id"] for o in out], [1, 2, 3, 4, 5])
        self.assertEqual(out[0]["result"]["protocolVersion"], "2025-03-26")
        self.assertEqual(out[0]["result"]["serverInfo"]["name"], "tdr")
        names = {t["name"] for t in out[1]["result"]["tools"]}
        self.assertEqual(names, {"tdr_get", "tdr_refs", "tdr_brief", "tdr_status", "tdr_check"})
        self.assertFalse(out[2]["result"]["isError"])
        self.assertIn("design_point", out[2]["result"]["content"][0]["text"])
        self.assertEqual(out[3]["result"]["content"][0]["text"], "ok")
        self.assertEqual(out[4]["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
