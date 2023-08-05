# -*- coding: utf-8 -*-
"""
Knowledge base of all built-in formatters.
"""

from __future__ import  absolute_import
from Pyautomators.formatter import _registry


# -----------------------------------------------------------------------------
# DATA:
# -----------------------------------------------------------------------------
# SCHEMA: formatter.name, formatter.class(_name)
_BUILTIN_FORMATS = [
    # pylint: disable=bad-whitespace
    ("plain",   "Pyautomators.formatter.plain:PlainFormatter"),
    ("pretty",  "Pyautomators.formatter.pretty:PrettyFormatter"),
    ("json",    "Pyautomators.formatter.json:JSONFormatter"),
    ("json.pretty", "Pyautomators.formatter.json:PrettyJSONFormatter"),
    ("null",      "Pyautomators.formatter.null:NullFormatter"),
    ("progress",  "Pyautomators.formatter.progress:ScenarioProgressFormatter"),
    ("progress2", "Pyautomators.formatter.progress:StepProgressFormatter"),
    ("progress3", "Pyautomators.formatter.progress:ScenarioStepProgressFormatter"),
    ("rerun",     "Pyautomators.formatter.rerun:RerunFormatter"),
    ("tags",          "Pyautomators.formatter.tags:TagsFormatter"),
    ("tags.location", "Pyautomators.formatter.tags:TagsLocationFormatter"),
    ("steps",         "Pyautomators.formatter.steps:StepsFormatter"),
    ("steps.doc",     "Pyautomators.formatter.steps:StepsDocFormatter"),
    ("steps.catalog", "Pyautomators.formatter.steps:StepsCatalogFormatter"),
    ("steps.usage",   "Pyautomators.formatter.steps:StepsUsageFormatter"),
    ("sphinx.steps",  "Pyautomators.formatter.sphinx_steps:SphinxStepsFormatter"),
    ("json.report","Pyautomators.formatter.sphinx_steps:SphinxStepsFormatter"),
    ("json_cucumber","Pyautomators.formatter.cucumber_json:CucumberJSONFormatter"),
    ("json_cucumber.pretty","Pyautomators.formatter.cucumber_json:PrettyCucumberJSONFormatter")
]

# -----------------------------------------------------------------------------
# FUNCTIONS:
# -----------------------------------------------------------------------------
def setup_formatters():
    """Register all built-in formatters (lazy-loaded)."""
    _registry.register_formats(_BUILTIN_FORMATS)