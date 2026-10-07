#!/usr/bin/env python3
"""Tests for scripts/brand_render.py: the size registry, content-only job validation, token
injection, the tokens-versus-identity check, PNG helpers, and one real render that is skipped
when no Chrome is installed. Brand files live in a temp folder per test, never the live brand/.

Run from the repo root:  python3 -m unittest scripts/test_brand_render.py
"""

import json
import os
import struct
import sys
import tempfile
import unittest
import urllib.parse
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand_render as br  # noqa: E402

TOKENS = {
    "colors": {"primary": "#7c3aed", "secondary": "", "background": "#0B1020", "text": "#FFFFFF", "accent": "#22D3EE"},
    "fonts": {"heading": "fonts/Heading.woff2", "body": "Inter", "fallback": "system-ui, sans-serif"},
    "logo": {"primary": "logos/primary.svg", "mark": "logos/mark.svg", "primary_inverse": "", "mark_inverse": ""},
}
IDENTITY = """# Visual identity

| Role | Hex | Usage |
| --- | --- | --- |
| Primary | `#7C3AED` | |
| Secondary | `#______` | |
| Background | `#0B1020` | |
| Text | `#FFFFFF` | |
| Accent / success / warning | `#22D3EE` | |

- Headings: Heading, self-hosted
- Body: Inter
"""


def write_png(path, w, h):
    raw = b"".join(b"\x00" + b"\x00\x00\x00\x00" * w for _ in range(h))
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + br._chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                + br._chunk(b"IDAT", zlib.compress(raw)) + br._chunk(b"IEND", b""))


class BrandDir(unittest.TestCase):
    """A temp brand/ with a logo, a mark, a font and a screenshot."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.brand = Path(self.tmp.name) / "brand"
        for rel in ("logos/primary.svg", "logos/mark.svg", "fonts/Heading.woff2", "screenshots/app.png"):
            (self.brand / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.brand / rel).write_text("x")
        self.saved = br.BRAND, br.SCREENSHOTS
        br.BRAND, br.SCREENSHOTS = self.brand, self.brand / "screenshots"
        self.sizes = br.load_sizes()

    def tearDown(self):
        br.BRAND, br.SCREENSHOTS = self.saved
        self.tmp.cleanup()


class Registry(unittest.TestCase):
    def test_registry_is_valid(self):
        sizes = br.load_sizes()
        ids = [s["id"] for s in sizes]
        self.assertEqual(len(ids), len(set(ids)), "duplicate preset ids")
        for s in sizes:
            self.assertIn(s["template"], br.TEMPLATE_PARAMS, s["id"])
            self.assertEqual(len(s["safe"]), 4, s["id"])
            self.assertLess(s["safe"][1] + s["safe"][3], s["w"], s["id"])
            self.assertLess(s["safe"][0] + s["safe"][2], s["h"], s["id"])
            if s.get("verified"):
                self.assertTrue(s["source"].startswith("https://"), f"{s['id']} is verified but has no source")
                self.assertRegex(s["verified"], r"^\d{4}-\d{2}-\d{2}$")
            for k in (s.get("params") or {}):
                self.assertIn(k, br.TEMPLATE_PARAMS[s["template"]], s["id"])

    def test_the_usual_surfaces_are_there(self):
        ids = {s["id"] for s in br.load_sizes()}
        for pid in ("og", "linkedin-post", "linkedin-cover", "linkedin-profile-cover", "x-post", "x-header",
                    "youtube-banner", "square", "portrait-4x5", "app-icon"):
            self.assertIn(pid, ids)

    def test_parse_size(self):
        self.assertEqual(br.parse_size("1600x400"), (1600, 400))
        for bad in ("1600", "1600x", "ax400", ""):
            with self.assertRaises(br.BrandError):
                br.parse_size(bad)


class Jobs(BrandDir):
    def test_preset_job_takes_template_size_safe_and_params(self):
        template, w, h, params = br.resolve_job(self.sizes, {"preset": "slack-icon", "file": "x.png"})
        self.assertEqual((template, w, h), ("icon", 1024, 1024))
        self.assertEqual(params["bg"], "brand")
        self.assertEqual(params["safe"], "0,0,0,0")

    def test_size_overrides_preset_and_drops_its_safe_area(self):
        template, w, h, params = br.resolve_job(self.sizes, {"preset": "og", "size": "1600x400", "headline": "Hi"})
        self.assertEqual((template, w, h, params["w"]), ("banner", 1600, 400, "1600"))
        self.assertNotIn("safe", params)

    def test_style_params_are_rejected(self):
        for bad in ({"motif": "aurora"}, {"theme": "blue"}, {"color": "#ff0000"}, {"sub": "more"}):
            with self.assertRaises(br.BrandError):
                br.resolve_job(self.sizes, {"preset": "og", "headline": "Hi", **bad})

    def test_headline_rules(self):
        self.assertEqual(br.check_headline("Turn calls into *battle cards*", "banner"), [])
        self.assertTrue(br.check_headline("*one* and *two*", "banner"))
        self.assertTrue(br.check_headline("a *very long gradient phrase*", "banner"))
        self.assertTrue(br.check_headline("unbalanced *star", "post"))
        self.assertTrue(br.check_headline("x" * 46, "banner"))
        self.assertEqual(br.check_headline("x" * 46, "post"), [])
        with self.assertRaises(br.BrandError):
            br.resolve_job(self.sizes, {"preset": "og", "headline": "*one* and *two*"})

    def test_stat_shot_and_focus(self):
        _, _, _, params = br.resolve_job(self.sizes, {"preset": "square", "headline": "Hi", "stat": "41%"})
        self.assertEqual(params["stat"], "41%")
        _, _, _, params = br.resolve_job(self.sizes, {"preset": "square", "shot": "app.png", "focus": "0.2,1"})
        self.assertEqual(params["focus"], "0.2,1")
        for bad in ({"stat": "1234567"}, {"stat": "3x", "shot": "app.png"}, {"shot": "../app.png"},
                    {"shot": "missing.png"}, {"shot": "/etc/passwd"}, {"focus": "1.2,0"}, {"focus": "a,b"}):
            with self.assertRaises(br.BrandError):
                br.resolve_job(self.sizes, {"preset": "square", **bad})
        with self.assertRaises(br.BrandError):
            br.resolve_job(self.sizes, {"preset": "og", "headline": "Hi", "stat": "3x"})

    def test_shot_and_icon_validation(self):
        template, _, _, params = br.resolve_job(self.sizes, {"template": "shot", "size": "1600x1000", "shot": "app.png", "fit": "cover"})
        self.assertEqual((template, params["fit"]), ("shot", "cover"))
        for bad in ({}, {"shot": "app.png", "fit": "stretch"}, {"shot": "app.png", "headline": "Hi"}):
            with self.assertRaises(br.BrandError):
                br.resolve_job(self.sizes, {"template": "shot", "size": "1600x1000", **bad})
        for bad in ({"pad": "0.9"}, {"pad": "x"}, {"bg": "red"}, {"mark": "symbol"}):
            with self.assertRaises(br.BrandError):
                br.resolve_job(self.sizes, {"preset": "app-icon", **bad})


class Tokens(BrandDir):
    def query(self, tokens, template="banner", params=None):
        url, notes = br.build_url(template, params or {"headline": "Hi *there*", "w": "1200", "h": "630"}, tokens)
        return dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query)), notes

    def test_empty_tokens_render_the_neutral_default_and_say_so(self):
        q, notes = self.query({})
        self.assertEqual((q["c_bg"], q["c_fg"], q["c_primary"], q["c_accent"]), tuple(br.NEUTRAL[k] for k in ("bg", "fg", "primary", "accent")))
        self.assertNotIn("logo", q)
        self.assertTrue(any("neutral default" in n for n in notes))
        self.assertTrue(any("no logo" in n for n in notes))

    def test_filled_tokens_reach_the_template(self):
        q, notes = self.query(TOKENS)
        self.assertEqual((q["c_bg"], q["c_fg"], q["c_primary"], q["c_accent"]), ("0B1020", "FFFFFF", "7C3AED", "22D3EE"))
        self.assertEqual((q["heading"], q["heading_src"]), ("Heading", "../fonts/Heading.woff2"))
        self.assertEqual(q["body"], "Inter")
        self.assertNotIn("body_src", q)
        self.assertEqual(q["logo"], "../logos/primary.svg")
        self.assertEqual(q["headline"], "Hi *there*")
        self.assertEqual(notes, [])

    def test_icon_uses_the_mark_and_inverse_falls_back_with_a_note(self):
        q, _ = self.query(TOKENS, "icon", {"bg": "brand"})
        self.assertEqual((q["logo"], q["bg"], q["c_bg"]), ("../logos/mark.svg", "brand", "0B1020"))
        q, notes = self.query(TOKENS, "icon", {"bg": "inverse"})
        self.assertEqual(q["logo"], "../logos/mark.svg")
        self.assertTrue(any("mark_inverse" in n for n in notes))
        q, _ = self.query({**TOKENS, "logo": {**TOKENS["logo"], "primary_inverse": "logos/mark.svg"}},
                          "banner", {"theme": "inverse"})
        self.assertEqual(q["logo"], "../logos/mark.svg")

    def test_screenshot_resolves_under_brand(self):
        q, _ = self.query(TOKENS, "post", {"shot": "app.png"})
        self.assertEqual(q["shot"], "../screenshots/app.png")

    def test_another_brand_folder_loads_assets_by_absolute_url(self):
        (self.brand / "tokens.json").write_text(json.dumps(TOKENS))
        saved = br.TOKENS, br.IDENTITY, br.OUT_DEFAULT, br.EXTERNAL_BRAND
        try:
            br.use_brand(self.brand)
            q, _ = self.query(br.load_tokens(), "post", {"shot": "app.png"})
            to = lambda rel: Path(os.path.relpath(self.brand.resolve() / rel, br.TEMPLATES)).as_posix()  # noqa: E731
            self.assertEqual(q["logo"], to("logos/primary.svg"))
            self.assertEqual(q["shot"], to("screenshots/app.png"))
            self.assertEqual(br.OUT_DEFAULT, self.brand.resolve() / "renders")
            lib = br.library_data(br.load_tokens(), "## Logo usage\n\n- Never **stretch** it.\n", {"name": "Acme"})
            self.assertEqual(lib["logos"][0]["src"], "../logos/primary.svg")
            self.assertEqual(lib["screenshots"][0]["src"], "../screenshots/app.png")
            self.assertEqual(lib["templates"], Path(os.path.relpath(br.TEMPLATES, self.brand.resolve() / "library")).as_posix())
            self.assertIn("c_bg=0B1020", lib["query"]["banner"])
            self.assertIn("<strong>stretch</strong>", lib["identity"]["logo"])
            self.assertEqual(lib["name"], "Acme")
        finally:
            br.TOKENS, br.IDENTITY, br.OUT_DEFAULT, br.EXTERNAL_BRAND = saved

    def test_bad_tokens_are_refused(self):
        for tokens in ({"colors": {"primary": "blue"}}, {"logo": {"primary": "logos/missing.svg"}},
                       {"logo": {"primary": "../../etc/passwd"}}, {"fonts": {"heading": "fonts/missing.ttf"}}):
            with self.assertRaises(br.BrandError):
                self.query(tokens)


class IdentityCheck(BrandDir):
    def test_agreeing_files_pass(self):
        self.assertEqual(br.identity_check(TOKENS, IDENTITY, self.brand), [])

    def test_disagreements_are_named(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["colors"]["primary"] = "#123456"
        tokens["fonts"]["body"] = "Lato"
        tokens["logo"]["mark"] = "logos/gone.svg"
        problems = br.identity_check(tokens, IDENTITY, self.brand)
        self.assertTrue(any("colors.primary" in p and "#123456" in p for p in problems))
        self.assertTrue(any("Lato" in p for p in problems))
        self.assertTrue(any("logos/gone.svg" in p for p in problems))

    def test_a_color_only_in_the_identity_is_drift(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["colors"]["accent"] = ""
        self.assertTrue(any("colors.accent" in p for p in br.identity_check(tokens, IDENTITY, self.brand)))


class Files(BrandDir):
    def test_png_size_crop_and_limits(self):
        p = self.brand / "a.png"
        write_png(p, 12, 9)
        br.crop_png_height(p, 7)
        self.assertEqual(br.png_size(p), (12, 7))
        self.assertEqual(br.check_png(p, 12, 7), [])
        self.assertIn("expected 10x7", br.check_png(p, 10, 7)[0])

    def test_svg_size(self):
        p = self.brand / "logos" / "wide.svg"
        p.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 64"></svg>')
        self.assertEqual(br.svg_size(p), (300.0, 64.0))
        p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="120px" height="40px"></svg>')
        self.assertEqual(br.svg_size(p), (120.0, 40.0))

    def test_logo_jobs_keep_the_aspect_ratio(self):
        (self.brand / "logos" / "primary.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 60"/>')
        (self.brand / "logos" / "mark.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"/>')
        jobs = br.logo_jobs(self.brand / "logos")
        sizes = {Path(out).name: (w, h) for _, w, h, out in jobs}
        self.assertEqual(sizes["primary-1024.png"], (1024, 205))
        self.assertEqual(sizes["mark-512.png"], (512, 512))

    def test_kit_spec(self):
        kit = self.brand / "kit" / "kit.json"
        kit.parent.mkdir()
        kit.write_text(json.dumps({"jobs": [{"file": "logo.png", "preset": "slack-icon"},
                                            {"file": "og.png", "preset": "og", "headline": "Hi"}]}))
        jobs, _ = br.kit_jobs(kit, TOKENS)
        self.assertEqual([Path(j[3]).name for j in jobs], ["logo.png", "og.png"])
        self.assertEqual(Path(jobs[0][3]).parent, br.OUT_DEFAULT / "kit")
        self.assertEqual(jobs[0][4], 2048)
        kit.write_text(json.dumps({"jobs": [{"file": "../x.png", "preset": "og"}, {"file": "b.png", "preset": "nope"}]}))
        with self.assertRaises(br.BrandError) as e:
            br.kit_jobs(kit, TOKENS)
        self.assertIn("job 1", str(e.exception))
        self.assertIn("job 2", str(e.exception))

    def test_og_title_from_the_draft(self):
        piece = self.brand / "2026-10-piece"
        piece.mkdir()
        (piece / "draft.md").write_text("---\nstatus: draft\n---\n\n# Why plain text wins\n\nBody.\n")
        self.assertEqual(br.draft_title(piece), "Why plain text wins")


@unittest.skipUnless(br.chrome_path(), "no Chrome or Chromium installed")
class Render(unittest.TestCase):
    def test_renders_exact_size(self):
        with tempfile.TemporaryDirectory() as td:
            template, w, h, params = br.resolve_job(br.load_sizes(), {"preset": "og", "headline": "Test *render*"})
            url, _ = br.build_url(template, params, {})
            out = br.render(url, w, h, Path(td) / "og.png")
            self.assertEqual(br.png_size(out), (1200, 630))


if __name__ == "__main__":
    unittest.main()
