"""Tests for tools/tdr.py. Run: python tools/tests/test_tdr.py"""
import io
import json
import re
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


MODELS = """kind: model
schema: 1
items:
  - id: MD-01
    title: Deflection of the shelf board
    role: analysis
    files:
      - sim/beam.py
    entry: sim.beam:run
    method: Simple beam under a central load
    basis:
      - P1
    scope: Static bending of a rectangular board
    params:
      - name: load
        unit: N
        min: 0
        max: 1000
      - name: span
        unit: mm
    results:
      - name: deflection
        unit: mm
"""

RUNS = """kind: model_run
schema: 1
items:
  - id: MD-01.01
    model: MD-01
    date: 2026-10-29
    by: assistant
    version: "sha-000000000000"
    stamp: "sha-000000000000"
    command: python -m sim.beam
    inputs:
      - param: load
        key: shelf.load_n
      - param: span
        key: shelf.span_mm
    settings:
      - name: step
        v: 0.5
        unit: mm
    seed: 1
    outputs:
      - result: deflection
        key: shelf.model_deflection_mm
    tol: 0.000001
"""

VALUE = """  - key: shelf.model_deflection_mm
    v: 1.5
    unit: mm
    status: calculated
    basis:
      - MD-01.01
"""


class ModelTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write("sim/beam.py", "def run(load, span):\n    return load * span\n")
        self.write("record/models.yaml", MODELS)
        self.write("record/model_runs/MD-01.yaml", RUNS)
        with (self.root / "record" / "values.yaml").open("a", newline="\n") as f:
            f.write(VALUE)
        self.restamp()

    def restamp(self):
        """Write the version and stamp that the tool computes into the run file."""
        rec = tdr.Record(self.root)
        md = rec.index["MD-01"]
        run = rec.index["MD-01.01"]
        ver = tdr.model_version(rec, md)
        st = tdr.run_stamp(rec, run, ver)
        p = self.root / "record" / "model_runs" / "MD-01.yaml"
        s = p.read_text(encoding="utf-8")
        s = re.sub(r'version: "sha-[0-9a-f]{12}"', f'version: "{ver}"', s)
        s = re.sub(r'stamp: "sha-[0-9a-f]{12}"', f'stamp: "{st}"', s)
        p.write_text(s, encoding="utf-8", newline="\n")
        self.refresh()

    def refresh(self):
        cli("tables", "--root", str(self.root))
        cli("status", "--root", str(self.root))

    def test_a_fresh_model_passes(self):
        self.assertEqual(self.check(), (0, "ok\n"))

    def test_version_ignores_line_ends_and_is_quoted_hex(self):
        rec = tdr.Record(self.root)
        v1 = tdr.model_version(rec, rec.index["MD-01"])
        self.assertRegex(v1, r"^sha-[0-9a-f]{12}$")
        p = self.root / "sim" / "beam.py"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(tdr.model_version(tdr.Record(self.root), rec.index["MD-01"]), v1)
        self.assertEqual(self.check(), (0, "ok\n"))

    def test_e23_code_edit(self):
        with (self.root / "sim" / "beam.py").open("a", newline="\n") as f:
            f.write("# changed\n")
        code, out = self.check()
        self.assertEqual(code, 1)
        self.assertIn("E23", codes(out))
        self.assertIn("current sha-", out)

    def test_e23_input_change(self):
        self.mutate("record/values.yaml", "v: 200", "v: 250")
        self.assertIn("E23", codes(self.check()[1]))

    def test_e23_setting_change(self):
        self.mutate("record/model_runs/MD-01.yaml", "v: 0.5", "v: 0.25")
        self.assertIn("E23", codes(self.check()[1]))

    def test_e23_history_run_is_not_checked(self):
        """A run that nothing cites is history and may be stale."""
        self.mutate("record/values.yaml", "      - MD-01.01\n", "      - D-001\n")
        self.mutate("record/values.yaml", "status: calculated\n    basis:\n      - D-001",
                    "status: decided\n    basis:\n      - D-001")
        with (self.root / "sim" / "beam.py").open("a", newline="\n") as f:
            f.write("# changed\n")
        self.refresh()
        self.assertEqual(self.check(), (0, "ok\n"))

    def test_e23_used_model_changes_the_version(self):
        self.write("sim/wind.py", "WIND = 1\n")
        self.write("record/models.yaml", MODELS + """  - id: MD-02
    title: Wind
    role: analysis
    files:
      - sim/wind.py
    entry: sim.wind:run
    method: A constant wind
    basis:
      - P1
    scope: Nothing real
    params:
      - name: u
        unit: m/s
    results:
      - name: f
        unit: N
""")
        self.mutate("record/models.yaml", "    files:\n      - sim/beam.py\n",
                    "    files:\n      - sim/beam.py\n    uses:\n      - MD-02\n")
        self.restamp()
        self.assertEqual(self.check(), (0, "ok\n"))
        with (self.root / "sim" / "wind.py").open("a", newline="\n") as f:
            f.write("# changed\n")
        self.assertIn("E23", codes(self.check()[1]))

    def test_e23_written_file_tag(self):
        self.mutate("record/model_runs/MD-01.yaml", "    tol: 0.000001\n",
                    "    tol: 0.000001\n    writes:\n      - sim/out.js\n")
        self.restamp()
        self.write("sim/out.js", "// no tag here\n")
        self.assertIn("E23", codes(self.check()[1]))
        st = tdr.Record(self.root).index["MD-01.01"].d["stamp"]
        self.write("sim/out.js", f"// tdr-run: MD-01.01 {st}\n")
        self.refresh()
        self.assertEqual(self.check(), (0, "ok\n"))

    def test_e03_missing_file_and_unknown_basis(self):
        self.mutate("record/models.yaml", "- sim/beam.py", "- sim/none.py")
        self.assertIn("E03", codes(self.check()[1]))
        self.mutate("record/models.yaml", "- sim/none.py", "- sim/beam.py")
        self.mutate("record/models.yaml", "      - P1\n", "      - P9\n")
        self.assertIn("E03", codes(self.check()[1]))

    def test_e22_forms(self):
        cases = [
            ("record/models.yaml", "role: analysis", "role: onboard"),
            ("record/models.yaml", "- sim/beam.py", "- ../beam.py"),
            ("record/models.yaml", "id: MD-01", "id: MD-1"),
            ("record/model_runs/MD-01.yaml", "id: MD-01.01", "id: MD-02.01"),
            ("record/model_runs/MD-01.yaml", "param: load", "param: nope"),
            ("record/model_runs/MD-01.yaml", "result: deflection", "result: nope"),
            ("record/model_runs/MD-01.yaml", "stamp: \"sha-", "stamp: \"abc-"),
            ("record/model_runs/MD-01.yaml", "        key: shelf.load_n\n",
             "        key: shelf.load_n\n        run: MD-01.01\n"),
        ]
        for rel, old, new in cases:
            with self.subTest(new=new):
                self.mutate(rel, old, new)
                self.assertIn("E22", codes(self.check()[1]))
                self.mutate(rel, new, old)
        self.assertEqual(self.check(), (0, "ok\n"))

    def test_e22_uses_cycle(self):
        self.mutate("record/models.yaml", "    files:\n      - sim/beam.py\n",
                    "    files:\n      - sim/beam.py\n    uses:\n      - MD-01\n")
        self.assertIn("E22", codes(self.check()[1]))

    def test_e22_check_of_a_model_needs_its_version(self):
        with (self.root / "record" / "checks.yaml").open("a", newline="\n") as f:
            f.write("  - id: K-002\n    target:\n      - MD-01\n    tier: T2\n"
                    "    method: refute\n    result: pass\n    by: checker\n    date: 2026-10-29\n")
        self.assertIn("E22", codes(self.check()[1]))
        with (self.root / "record" / "checks.yaml").open("a", newline="\n") as f:
            f.write("    version: sha-0123456789ab\n")
        self.assertEqual(self.check(), (0, "ok\n"))

    def test_e26_value_not_in_outputs(self):
        self.mutate("record/model_runs/MD-01.yaml", "key: shelf.model_deflection_mm",
                    "key: shelf.load_n")
        self.restamp()
        self.assertIn("E26", codes(self.check()[1]))

    def test_e26_output_not_calculated_from_the_run(self):
        self.mutate("record/values.yaml", "status: calculated\n    basis:\n      - MD-01.01",
                    "status: decided\n    basis:\n      - D-001")
        self.mutate("record/model_runs/MD-01.yaml", "    outputs:", "    outputs:\n"
                    "      - result: deflection\n        key: shelf.load_n")
        self.write("record/values2.yaml", "kind: value\nschema: 1\nitems:\n"
                   "  - key: shelf.calc2_mm\n    v: 1\n    unit: mm\n    status: calculated\n"
                   "    basis:\n      - MD-01.01\n")
        self.restamp()
        self.assertIn("E26", codes(self.check()[1]))

    def test_e05_measured_may_not_cite_a_design_run(self):
        self.mutate("record/values.yaml", "status: calculated", "status: measured")
        self.assertIn("E05", codes(self.check()[1]))

    def test_e05_withdrawn_is_never_a_basis(self):
        self.mutate("record/values.yaml", "key: board.width_mm\n    v: 200\n    unit: mm\n"
                    "    status: decided", "key: board.width_mm\n    v: 200\n    unit: mm\n"
                    "    status: withdrawn")
        self.refresh()
        self.assertEqual(self.check()[0], 0)
        self.mutate("record/model_runs/MD-01.yaml", "key: shelf.load_n", "key: board.width_mm")
        self.restamp()
        self.assertIn("E05", codes(self.check()[1]))

    def test_references_of_the_smaller_changes(self):
        self.mutate("record/requirements.yaml", "    parts:\n      - board\n      - bracket",
                    "    parts:\n      - board\n      - bracket\n    values:\n      - shelf.nope")
        self.assertIn("E03", codes(self.check()[1]))
        self.mutate("record/requirements.yaml", "shelf.nope", "shelf.load_n")
        self.assertEqual(self.check()[0], 0)
        self.mutate("record/parts.yaml", "id: board\n", "id: board\n    price: board.cost\n")
        self.assertIn("E03", codes(self.check()[1]))

    def test_supersedes_list_and_scalar(self):
        self.mutate("record/decisions.yaml", "  - id: D-002\n", "  - id: D-002\n"
                    "    supersedes: D-001\n")
        self.assertEqual(self.check()[0], 0)
        self.mutate("record/decisions.yaml", "supersedes: D-001", "supersedes:\n      - D-001\n"
                    "      - D-099")
        self.assertIn("E03", codes(self.check()[1]))

    def test_section_ids_are_resolved_when_used(self):
        base = "kind: value\nschema: 1\nitems:\n  - key: a.b\n    v: 1\n    status: calculated\n" \
               "    basis:\n      - "
        self.write("docs/plain.md", "# Plain\n\n## No ids here\n")
        self.write("record/v3.yaml", base + "docs/plain.md#anything\n")
        self.refresh()
        self.assertEqual(self.check()[0], 0, "a file without {#id} headings is not checked")
        self.write("record/v3.yaml", base + "docs/03-design.md#deflection\n")
        self.assertEqual(self.check()[0], 0)
        self.write("record/v3.yaml", base + "docs/03-design.md#other\n")
        self.assertIn("E03", codes(self.check()[1]))

    def test_open_after_and_read_query(self):
        self.mutate("record/open.yaml", "    opened: 2026-10-21\n",
                    "    opened: 2026-10-21\n    after:\n      - Q-404\n")
        self.assertIn("E03", codes(self.check()[1]))
        self.mutate("record/open.yaml", "Q-404", "Q-001")
        self.assertEqual(self.check()[0], 0)
        self.mutate("record/sources.yaml", "read: not_read", "read: query")
        self.assertIn("E22", codes(self.check()[1]), "query needs the retrieved date")

    def test_tables_regenerates(self):
        self.mutate("record/values.yaml", "v: 18", "v: 19")
        self.assertIn("E10", codes(self.check()[1]))
        code, out = cli("tables", "--root", str(self.root))
        self.assertEqual(code, 0)
        cli("status", "--root", str(self.root))
        self.assertEqual(self.check(), (0, "ok\n"))
        self.assertEqual(cli("tables", "--root", str(self.root))[1].strip(), "0 file(s) changed")

    def test_stamp_command(self):
        code, out = cli("stamp", "MD-01.01", "--root", str(self.root))
        run = tdr.Record(self.root).index["MD-01.01"].d
        self.assertEqual(code, 0)
        self.assertIn(f"version: {run['version']}", out)
        self.assertIn(f"stamp: {run['stamp']}", out)
        self.assertEqual(cli("stamp", "R-01", "--root", str(self.root))[0], 1)

    def test_tier_accepts_a_comma_list_of_decisions(self):
        m = Path(self._tmp.name) / "msg.txt"
        m.write_text("Tier: T3\nDecision: D-001, D-002\n", encoding="utf-8")
        self.assertEqual(cli("tier", "--message", str(m), "--root", str(self.root))[0], 0)
        m.write_text("Tier: T3\nDecision: D-001, D-404\n", encoding="utf-8")
        self.assertIn("E12", cli("tier", "--message", str(m), "--root", str(self.root))[1])


class TemplateTests(unittest.TestCase):
    def test_template_and_example_still_pass(self):
        for root in (REPO / "template", EXAMPLE):
            self.assertEqual(cli("check", "--root", str(root)), (0, "ok\n"))


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
