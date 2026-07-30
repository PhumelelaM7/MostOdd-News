# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django

# Add the Django project root to the Python path
sys.path.insert(0, os.path.abspath("../.."))

# Configure Django settings
os.environ["DJANGO_SETTINGS_MODULE"] = "news_project.settings"
django.setup()

# -- Project information -----------------------------------------------------

project = "MostOdd News"
copyright = "2026, Phumelela Mdingi"
author = "Phumelela Mdingi"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]