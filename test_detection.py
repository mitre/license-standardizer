#!/usr/bin/env python3
"""Unit tests for license template detection logic."""

import unittest
from standardize_licenses import LicenseStandardizer


class TestTemplateDetection(unittest.TestCase):
    """Test template detection logic."""

    def setUp(self):
        """Set up test instance."""
        self.standardizer = LicenseStandardizer(dry_run=True)

    def test_cis_baseline_detection(self):
        """Test CIS baseline repo detection."""
        # Should be CIS
        cis_repos = [
            "aws-foundations-cis-baseline",
            "docker-ce-cis-baseline",
            "kubernetes-cis-baseline",
            "oracle-mysql-ee-5.7-cis-baseline",
            "canonical-ubuntu-18.04-lts-server-cis-baseline",
        ]
        for repo in cis_repos:
            with self.subTest(repo=repo):
                self.assertTrue(
                    self.standardizer.is_cis_baseline_repo(repo),
                    f"{repo} should be detected as CIS baseline"
                )
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "cis", f"{repo} should use CIS template")

    def test_cis_hardening_detection(self):
        """Test CIS hardening repo detection."""
        # Should be CIS
        cis_hardening = [
            "ansible-cis-docker-ce-hardening",
            "ansible-cis-tomcat-hardening",
            "cis-aws-foundations-hardening",
            "chef-cis-docker-ce-hardening",
        ]
        for repo in cis_hardening:
            with self.subTest(repo=repo):
                self.assertTrue(
                    self.standardizer.is_cis_baseline_repo(repo),
                    f"{repo} should be detected as CIS hardening"
                )
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "cis", f"{repo} should use CIS template")

    def test_disa_baseline_detection(self):
        """Test DISA STIG baseline repo detection."""
        # Should be DISA
        disa_repos = [
            "microsoft-windows-server-2019-stig-baseline",
            "redhat-enterprise-linux-7-stig-baseline",
            "oracle-database-12c-stig-baseline",
            "canonical-ubuntu-16.04-lts-stig-baseline",
            "nginx-stig-baseline",
            "apache-couchdb-srg-baseline",
        ]
        for repo in disa_repos:
            with self.subTest(repo=repo):
                self.assertTrue(
                    self.standardizer.is_disa_baseline_repo(repo),
                    f"{repo} should be detected as DISA baseline"
                )
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "disa", f"{repo} should use DISA template")

    def test_plain_saf_tools(self):
        """Test SAF tools are detected as plain (not CIS/DISA)."""
        # Should be plain (SAF tools)
        plain_repos = [
            "saf",
            "saf-cli",
            "saf-baseline-ingestion",
            "saf-training-lab-environment",
            "saf-development-lab-environment",
            "saf-lambda-function",
        ]
        for repo in plain_repos:
            with self.subTest(repo=repo):
                self.assertFalse(
                    self.standardizer.is_cis_baseline_repo(repo),
                    f"{repo} should NOT be CIS"
                )
                self.assertFalse(
                    self.standardizer.is_disa_baseline_repo(repo),
                    f"{repo} should NOT be DISA"
                )
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "plain", f"{repo} should use plain template")

    def test_plain_utilities(self):
        """Test utilities and tools are detected as plain."""
        # Should be plain (utilities)
        plain_repos = [
            "heimdall2",
            "vulcan",
            "inspec_tools",
            "heimdall-lite",
            "ckl2csv",
            "emasser",
        ]
        for repo in plain_repos:
            with self.subTest(repo=repo):
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "plain", f"{repo} should use plain template")

    def test_stigready_is_plain(self):
        """Test stigready repos are plain (not DISA)."""
        # stigready = InSpec ready for STIG, but no DISA content
        stigready_repos = [
            "nginx-stigready-baseline",
            "ansible-nginx-stigready-hardening",
        ]
        for repo in stigready_repos:
            with self.subTest(repo=repo):
                self.assertFalse(
                    self.standardizer.is_disa_baseline_repo(repo),
                    f"{repo} should NOT be DISA (stigready is plain)"
                )
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "plain", f"{repo} should use plain template")

    def test_demo_repos_are_plain(self):
        """Test demo and sample repos are plain."""
        demo_repos = [
            "demo-aws-baseline",
            "demo-aws-hardening",
            "helloworld-web-baseline",
            "sample-mysql-overlay",
        ]
        for repo in demo_repos:
            with self.subTest(repo=repo):
                template = self.standardizer.detect_template_type(repo_name=repo)
                self.assertEqual(template, "plain", f"{repo} should use plain template")

    def test_incorrect_license_correction(self):
        """Test that incorrectly licensed tool repos get fixed to plain."""
        # saf-baseline-ingestion has CIS in LICENSE but is a tool
        content_with_cis = "CIS Benchmarks. Please visit www.cisecurity.org"
        template = self.standardizer.detect_template_type(
            content=content_with_cis,
            repo_name="saf-baseline-ingestion"
        )
        self.assertEqual(
            template, "plain",
            "SAF tool with CIS content should be corrected to plain"
        )

        # saf-training has DISA in LICENSE but is a training env
        content_with_disa = "DISA STIGs. Please visit https://public.cyber.mil/stigs/"
        template = self.standardizer.detect_template_type(
            content=content_with_disa,
            repo_name="saf-training-lab-environment"
        )
        self.assertEqual(
            template, "plain",
            "SAF training env with DISA content should be corrected to plain"
        )


if __name__ == "__main__":
    unittest.main()
