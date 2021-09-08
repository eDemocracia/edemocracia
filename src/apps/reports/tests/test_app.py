import pytest


def test_apps():
    from apps.reports.apps import ReportsConfig
    assert ReportsConfig.name == 'reports'
