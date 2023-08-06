#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2019 Würth Phoenix S.r.l.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""Tests for `rlog_generator` package."""


import logging
import os
import unittest

from click.testing import CliRunner

from rlog_generator import rlog_generator, utils, cli


logging.getLogger().addHandler(logging.NullHandler())


class TestRlogGenerator(unittest.TestCase):
    """Tests for `rlog_generator.rlog_generator` module."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.pattern_file = "tests/conf/patterns/apache_commons.yml"
        self.pattern = utils.load_config(self.pattern_file)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_log_generator(self):
        """Test log_generator function."""
        nr_logs = rlog_generator.log_generator(self.pattern)
        self.assertEqual(nr_logs, 10)
        self.assertTrue(os.path.exists("/tmp/apache.log"))

        with open("/tmp/apache.log") as f:
            lines = len(f.readlines())

        self.assertEqual(lines, 10)
        self.assertEqual(nr_logs, lines)

        patterns_err = "tests/conf/patterns_err/apache_commons.yml"
        pattern = utils.load_config(patterns_err)

        with self.assertRaises(ValueError):
            rlog_generator.log_generator(pattern)

    def test_core(self):
        patterns_err = "tests/conf/patterns_err"
        with self.assertRaises(ValueError):
            rlog_generator.core(patterns_err, 2)

        patterns_empty = "tests/conf/patterns_empty"
        res = rlog_generator.core(patterns_empty, 2)
        self.assertEqual(res, 0)

        patterns = "tests/conf/patterns"
        res = rlog_generator.core(patterns, 2)
        self.assertEqual(res, 11)

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--patterns', 'fake'])
        assert result.exit_code == 0
        assert "There aren't logs to generate" in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help' in help_result.output
        assert '--patterns' in help_result.output
        assert '--max-concur-req' in help_result.output
        assert '--log-level' in help_result.output
        assert '--progress-bar' in help_result.output
        assert '--version' in help_result.output
