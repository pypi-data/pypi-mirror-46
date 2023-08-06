# -*- coding: utf-8 -*-
import logging

from freckles.adapters import FrecklesAdapter
from frutils import replace_strings_in_obj, dict_merge
from frutils.config import Cnf
from .defaults import (
    DEFAULT_TEMPTINGS_FOLDER,
    TEMPTING_FRECKLET_JINJA_ENV,
    TEMPTING_COMMUNITY_REPO,
)
from .tempting import TemptingContext

log = logging.getLogger("freckles")

DEFAULT_TEMPTING_FRECKLETS = {
    "{{== tempting_name ==}}-file": {
        "doc": "{{== tempting_doc ==}}",
        "args": {"_import": ["file-with-content"]},
        "frecklets": [
            {
                "file-with-content": {
                    "path": "{{:: path ::}}",
                    "group": "{{:: group ::}}",
                    "owner": "{{:: owner ::}}",
                    "mode": "{{:: mode ::}}",
                    "content": "{{== tempting_content ==}}",
                }
            }
        ],
    }
}


class FrecklesAdapterTempting(FrecklesAdapter):
    def __init__(self, name, context):

        super(FrecklesAdapterTempting, self).__init__(
            adapter_name=name, context=context, config_schema={}, run_config_schema={}
        )
        self._tempting_context = None

    @property
    def tempting_context(self):

        if self._tempting_context is None:
            repo_list = self.resource_folder_map.get("temptings")

            if not repo_list:
                repo_list = []

            repos = []
            for r in repo_list:
                repos.append(r["path"])

            cnf = Cnf(self.context.config)

            self._tempting_context = TemptingContext("default", cnf, repos=repos)

        return self._tempting_context

    def get_folders_for_alias(self, alias):

        if alias == "default":
            return ["temptings::{}".format(DEFAULT_TEMPTINGS_FOLDER)]
        elif alias == "community":
            return ["temptings::{}".format(TEMPTING_COMMUNITY_REPO)]
        else:
            return []

    def get_extra_frecklets(self):

        result = {}

        for tempting_name, tempting in self.tempting_context.tempting_index.items():

            try:
                frecklets = tempting.meta.get("freckles", {}).get("frecklets", None)
            except (Exception) as e:
                log.warning(e)
                continue

            if frecklets is None:
                frecklets = DEFAULT_TEMPTING_FRECKLETS

            repl_dict = {
                "tempting_name": tempting_name,
                "tempting_content": tempting.template,
                "tempting_doc": tempting.meta.get("doc", {}),
            }
            replaced = replace_strings_in_obj(
                frecklets, repl_dict, jinja_env=TEMPTING_FRECKLET_JINJA_ENV
            )
            failed = []

            for name, frecklet in replaced.items():
                try:
                    args = frecklet.get("args", {})
                    import_arg = args.pop("_import", [])

                    args = dict_merge(args, tempting.args, copy_dct=True)
                    if "_import" in args.keys():
                        include2 = args["_import"]
                        args["_import"] = include2 + import_arg
                    else:
                        args["_import"] = import_arg
                    frecklet["args"] = args
                except (Exception) as e:
                    log.warning(e)
                    failed.append(name)

            for f_name, f in replaced.items():

                if f_name in failed:
                    continue

                if f_name in result.keys():
                    log.warning(
                        "Duplicate generated frecklet '{}' from tempting, ignoring..."
                    )
                    continue
                result[f_name] = f

        return result

    def get_supported_resource_types(self):

        return ["temptings"]

    def get_supported_task_types(self):

        return []

    def run(self, **kwargs):

        raise Exception("The tempting adapter does not support running frecklets.")
