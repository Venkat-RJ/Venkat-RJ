import csv
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from generate import build as build_animation, static_from
from figure import build as build_figure

ROOT=Path(__file__).resolve().parent
SVG_NS='{http://www.w3.org/2000/svg}'

class VisualAssets(unittest.TestCase):
    def test_animation_valid_xml(self):
        for theme in ['dark','light']:
            root=ET.fromstring((ROOT/f'experiment-{theme}.svg').read_text())
            self.assertEqual(root.tag,SVG_NS+'svg')
            self.assertEqual(root.attrib['viewBox'],'0 0 900 340')
    def test_deterministic_animation(self):
        for theme in ['dark','light']:
            self.assertEqual(build_animation(theme),(ROOT/f'experiment-{theme}.svg').read_text())
    def test_deterministic_figure(self):
        for theme in ['dark','light']:
            self.assertEqual(build_figure(theme),(ROOT/f'frontieror-{theme}.svg').read_text())
    def test_no_scripts_or_external_content(self):
        for theme in ['dark','light']:
            root=ET.parse(ROOT/f'experiment-{theme}.svg').getroot()
            names={x.tag.rsplit('}',1)[-1] for x in root.iter()}
            self.assertFalse(names.intersection({'script','image','foreignObject','iframe','filter','style'}))
            for element in root.iter():
                for k,v in element.attrib.items():
                    self.assertNotIn('http:',v)
                    self.assertNotIn('https:',v)
    def test_tracks_have_duration_and_repeat(self):
        for theme in ['dark','light']:
            root=ET.parse(ROOT/f'experiment-{theme}.svg').getroot()
            nodes=[el for el in root.iter() if el.tag in [SVG_NS+'animate',SVG_NS+'animateTransform']]
            self.assertGreaterEqual(len(nodes),50)
            for node in nodes:
                self.assertEqual(node.attrib.get('dur'),'32s')
                self.assertEqual(node.attrib.get('repeatCount'),'indefinite')
                self.assertEqual(node.attrib.get('keyTimes','').split(';')[0],'0.000000')
                self.assertEqual(node.attrib.get('keyTimes','').split(';')[-1],'1.000000')
    def test_light_and_dark_are_different(self):
        self.assertNotEqual((ROOT/'experiment-dark.svg').read_bytes(),(ROOT/'experiment-light.svg').read_bytes())
    def test_static_exports_have_no_animation(self):
        for theme in ['dark','light']:
            content=(ROOT/f'experiment-{theme}.svg').read_text()
            fallback=(ROOT/f'experiment-{theme}-static.svg').read_text()
            ET.fromstring(fallback)
            self.assertNotIn('<animate',fallback)
            self.assertEqual(static_from(content),fallback)
    def test_illustrative_disclaimer(self):
        for theme in ['dark','light']:
            self.assertIn('NOT A DEMO OF A REAL EXPERIMENT.',(ROOT/f'experiment-{theme}.svg').read_text())
    def test_instance_count_and_signs(self):
        rows=list(csv.DictReader((ROOT/'frontieror-instances.csv').open()))
        values=[float(r['normalized_advantage']) for r in rows]
        self.assertEqual(len(values),30)
        self.assertEqual(sum(v>0 for v in values),29)
        self.assertEqual(sum(v<0 for v in values),1)
        self.assertEqual(len({r['stratum'] for r in rows}),6)
    def test_readme_links_real_figures(self):
        r=(ROOT/'README.md').read_text()
        self.assertIn('fig1_probe_comparison.png',r)
        self.assertIn('media/frontieror-dark.svg',r)
        self.assertIn('media/experiment-dark.svg',r)
        self.assertIn('built on [Lattice]',r)
        self.assertIn('open PRs',r)

if __name__=='__main__': unittest.main()
