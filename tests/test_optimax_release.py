"""Offline contracts for the Optimax release advertised by each supported host."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = "0.2.0"
RELEASE_SHA = "4a39c1e2740a9459f0c9777a5194f4da5cc797c3"
HOSTS = (
    (".agents/plugins/marketplace.json", "alo-labs-codex",
     {"source": "url", "url": "https://github.com/alo-exp/optimax.git"}),
    (".claude-plugin/marketplace.json", "alo-labs",
     {"source": "github", "repo": "alo-exp/optimax"}),
)


class OptimaxReleaseTests(unittest.TestCase):
    def load_optimax(self, path):
        catalog = json.loads((ROOT / path).read_text(encoding="utf-8"))
        self.assertIsInstance(catalog["plugins"], list)
        entries = [plugin for plugin in catalog["plugins"]
                   if plugin.get("name") == "optimax"]
        self.assertEqual(len(entries), 1, f"{path}: expected one Optimax entry")
        return catalog, entries[0]

    def test_host_catalog_shapes_and_source_identities(self):
        for path, marketplace_name, identity in HOSTS:
            with self.subTest(host=marketplace_name):
                catalog, plugin = self.load_optimax(path)
                self.assertEqual(catalog["name"], marketplace_name)
                if marketplace_name == "alo-labs-codex":
                    self.assertIsInstance(catalog["interface"]["displayName"], str)
                    self.assertEqual(plugin["policy"]["installation"], "AVAILABLE")
                else:
                    self.assertIsInstance(catalog["owner"]["name"], str)
                    self.assertIsInstance(catalog["metadata"]["version"], str)
                    self.assertIs(plugin["strict"], True)
                source = plugin["source"]
                self.assertEqual(set(source), set(identity) | {"ref", "sha"})
                self.assertEqual({key: source[key] for key in identity}, identity)

    def test_advertised_version_and_ref_match_release(self):
        for path, marketplace_name, _ in HOSTS:
            _, plugin = self.load_optimax(path)
            for field, actual, expected in (
                ("version", plugin["version"], RELEASE_VERSION),
                ("ref", plugin["source"]["ref"], f"v{RELEASE_VERSION}"),
            ):
                with self.subTest(host=marketplace_name, field=field):
                    self.assertEqual(actual, expected)

    def test_pins_are_full_accepted_release_revision(self):
        for path, marketplace_name, _ in HOSTS:
            with self.subTest(host=marketplace_name):
                _, plugin = self.load_optimax(path)
                self.assertRegex(plugin["source"]["sha"], r"^[0-9a-f]{40}$")
                self.assertEqual(plugin["source"]["sha"], RELEASE_SHA)

    def test_hosts_advertise_the_same_release(self):
        releases = []
        for path, _, _ in HOSTS:
            _, plugin = self.load_optimax(path)
            releases.append((plugin["version"], plugin["source"]["ref"],
                             plugin["source"]["sha"]))
        self.assertEqual(releases[0], releases[1])


if __name__ == "__main__":
    unittest.main()
