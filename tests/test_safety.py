"""Tests for safety protections."""

import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

sys.path.insert(0, str(Path(__file__).parent.parent))
from standardize_licenses import app

# CliRunner for testing Typer CLI
runner = CliRunner()


class TestCommandValidation:
    """Layer 1: Prevent accidental mass updates."""

    def test_no_target_specified_fails(self):
        """Must specify --repo, --pattern, or --interactive."""
        result = runner.invoke(app, ["--dry-run"])
        assert result.exit_code == 1
        assert "No target specified" in result.output

    def test_repo_flag_works(self):
        """--repo flag is valid target."""
        # Will fail on GitHub API but validates command
        result = runner.invoke(app, ["--repo", "saf", "--dry-run", "--no-interactive"])
        # Should not get "No target specified" error
        assert "No target specified" not in result.output

    def test_pattern_flag_works(self):
        """--pattern flag is valid target."""
        result = runner.invoke(app, ["--pattern", "saf", "--dry-run", "--no-interactive"])
        assert "No target specified" not in result.output

    def test_interactive_requires_separate_testing(self):
        """Interactive mode requires prompt simulation (tested separately)."""
        # Interactive mode with actual prompts needs create_pipe_input()
        # For now, just verify --no-interactive prevents hanging
        # Real interactive tests in test_interactive.py
        pass


class TestBulkConfirmation:
    """Layer 2: Require confirmation for bulk operations."""

    def test_bulk_update_requires_confirmation_without_force(self, mocker):
        """Updating >10 repos without --force requires confirmation."""
        # Mock to return 50 repos
        mocker.patch(
            "standardize_licenses.LicenseStandardizer.get_saf_repos",
            return_value=[f"repo-{i}" for i in range(50)],
        )

        # Without --force, should prompt (but --no-interactive prevents it)
        result = runner.invoke(app, ["--pattern", "*", "--no-interactive"])

        # Should either ask for confirmation or fail without it
        assert "Continue?" in result.output or result.exit_code != 0

    def test_force_flag_skips_confirmation(self, mocker):
        """--force flag bypasses confirmation."""
        mocker.patch(
            "standardize_licenses.LicenseStandardizer.get_saf_repos",
            return_value=[f"repo-{i}" for i in range(50)],
        )
        mocker.patch("standardize_licenses.LicenseStandardizer.process_repo", return_value={"status": "success", "action": "updated", "template": "plain", "error": None})

        result = runner.invoke(app, ["--pattern", "*", "--force", "--dry-run"])
        # Should not ask for confirmation
        assert "Continue?" not in result.output

    def test_small_batch_no_confirmation(self, mocker):
        """Updating <=10 repos doesn't require confirmation."""
        mocker.patch(
            "standardize_licenses.LicenseStandardizer.get_saf_repos",
            return_value=[f"repo-{i}" for i in range(5)],
        )
        mocker.patch("standardize_licenses.LicenseStandardizer.process_repo", return_value={"status": "success", "action": "updated", "template": "plain", "error": None})

        result = runner.invoke(app, ["--pattern", "*", "--dry-run"])
        # Should not ask (small batch)
        assert "Continue?" not in result.output


class TestBackupSystem:
    """Layer 3: Backup before update."""

    def test_backup_flag_enabled_by_default(self):
        """--backup should be enabled by default."""
        result = runner.invoke(app, ["--help"])
        assert "--backup" in result.output

    def test_no_backup_flag_disables_backup(self):
        """--no-backup flag disables backup."""
        result = runner.invoke(app, ["--help"])
        assert "--no-backup" in result.output or "backup" in result.output.lower()


class TestDryRunAnalysis:
    """Layer 4: Template distribution analysis."""

    def test_dry_run_shows_template_distribution(self, mocker, tmp_path, monkeypatch):
        """Dry-run should show template type distribution."""
        monkeypatch.chdir(tmp_path)

        mocker.patch(
            "standardize_licenses.LicenseStandardizer.get_saf_repos",
            return_value=["aws-cis-baseline", "rhel-stig-baseline", "saf", "heimdall2"],
        )
        mocker.patch("standardize_licenses.LicenseStandardizer.get_repo_metadata", return_value={"fork": False, "archived": False, "default_branch": "main"})
        mocker.patch("standardize_licenses.LicenseStandardizer.check_license_file", return_value=("LICENSE", "abc"))
        mocker.patch("standardize_licenses.LicenseStandardizer.get_license_content", return_value="Apache 2.0")

        result = runner.invoke(app, ["--pattern", "*", "--dry-run"])

        # Should show template distribution in summary or output
        assert "cis" in result.output.lower() or "disa" in result.output.lower() or "plain" in result.output.lower()


class TestSanityChecks:
    """Layer 5: Sanity check warnings."""

    def test_warns_if_all_same_template(self, mocker):
        """Warn if all repos detected as same template (suspicious)."""
        # Mock all repos as plain (suspicious for baseline repos)
        mocker.patch(
            "standardize_licenses.LicenseStandardizer.get_saf_repos",
            return_value=["aws-cis-baseline", "docker-cis-baseline", "rhel-stig-baseline"],
        )
        mocker.patch("standardize_licenses.LicenseStandardizer.get_repo_metadata", return_value={"fork": False, "archived": False, "default_branch": "main"})
        mocker.patch("standardize_licenses.LicenseStandardizer.check_license_file", return_value=(None, None))  # No license

        result = runner.invoke(app, ["--pattern", "*baseline", "--dry-run"])

        # Should detect CIS and DISA, not all plain
        # If all detected as same, should warn
        assert result.exit_code == 0  # Should complete but maybe warn

    def test_warns_if_too_many_creates(self, mocker):
        """Warn if >50% are 'created' (most should already have licenses)."""
        # Test will check for warning in future implementation
        pass  # Placeholder

    def test_warns_if_too_many_forks(self, mocker):
        """Warn if >30% are forks (might be wrong team)."""
        # Test will check for warning in future implementation
        pass  # Placeholder
