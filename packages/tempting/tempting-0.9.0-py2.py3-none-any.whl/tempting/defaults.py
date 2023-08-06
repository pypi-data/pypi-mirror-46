# -*- coding: utf-8 -*-
import os

from jinja2 import Environment
from jinja2.nativetypes import NativeEnvironment

from freckles_adapter_nsbl.defaults import NSBL_COMMUNITY_FRECKLET_REPO
from frutils import JINJA_DELIMITER_PROFILES, jinja2_filters

DEFAULT_TEMPTINGS_FOLDER = os.path.join(
    os.path.dirname(__file__), "external", "temptings"
)

DEFAULT_TEMPTING_JINJA_ENV = NativeEnvironment(**JINJA_DELIMITER_PROFILES["freckles"])
for filter_name, filter_details in jinja2_filters.ALL_FRUTIL_FILTERS.items():
    DEFAULT_TEMPTING_JINJA_ENV.filters[filter_name] = filter_details["func"]

TEMPTING_FRECKLET_JINJA_ENV = Environment(**JINJA_DELIMITER_PROFILES["documentation"])

# TEMPTING_COMMUNITY_REPO_URL = "https://gitlab.com/frecklets/temptings-community.git"
TEMPTING_COMMUNITY_REPO_URL = (
    "https://gitlab.com/frecklets/frecklets-nsbl-community.git"
)

TEMPTING_COMMUNITY_REPO = NSBL_COMMUNITY_FRECKLET_REPO

TEMPTING_CONTEXT_SCHEMA = {}
TEMPTING_LOAD_CONFIG = {
    "class_name": "Tempting",
    "attributes": [
        {
            "FrontmatterAndContentAttribute": {
                "metadata_name": "meta",
                "content_name": "template",
                "source_attr_name": "ting_content",
            }
        },
        {"FileStringContentAttribute": {"target_attr_name": "ting_content"}},
        {
            "ArgsAttribute": {
                "source_attr_name": "meta",
                "target_attr_name": "args",
                "index_attr_name": "_meta_parent_repo",
                "validate_list_attr": "template_keys",
                "filtered_attr_name": "args_filtered",
            }
        },
        {
            "TemplateKeysAttribute": {
                "source_attr_name": "template",
                "target_attr_name": "template_keys",
                "jinja_env": DEFAULT_TEMPTING_JINJA_ENV,
            }
        },
        {
            "CliArgsAttribute": {
                "target_attr_name": "cli_args",
                "var_names_attr_name": "template_keys",
                "args_attr_name": "args",
            }
        },
        {"DocAttribute": {"target_attr_name": "doc", "source_attr_name": "meta"}},
    ],
    "ting_id_attr": "tempting_name",
    "mixins": [],
    "loaders": {
        "tempting_files": {
            "class": "ting.tings.FileTings",
            "load_config": {"folder_load_file_match_regex": "\\.j2$"},
            "attributes": [
                "FileStringContentAttribute",
                {
                    "MirrorAttribute": {
                        "source_attr_name": "filename_no_ext",
                        "target_attr_name": "tempting_name",
                    }
                },
            ],
        }
    },
}
