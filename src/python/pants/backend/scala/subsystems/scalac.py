# Copyright 2021 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import annotations

from pants.option.option_types import ArgsListOption, DictOption
from pants.option.subsystem import Subsystem
from pants.util.strutil import softwrap


class Scalac(Subsystem):
    options_scope = "scalac"
    name = "scalac"
    help = "The Scala compiler."

    default_plugins_lockfile_path = (
        "src/python/pants/backend/scala/subsystems/scalac_plugins.default.lockfile.txt"
    )
    default_plugins_lockfile_resource = (
        "pants.backend.scala.subsystems",
        "scalac_plugins.default.lockfile.txt",
    )

    args = ArgsListOption(example="-encoding UTF-8")

    args_for_resolve = DictOption[list[str]](
        help=softwrap(
            """
            A dictionary mapping JVM resolve names to additional arguments to pass
            to `scalac` for that resolve. These arguments are appended to the
            global `[scalac].args` option when compiling Scala code using the
            resolve.
            """
        ),
    )

    # TODO: see if we can use an actual list mechanism? If not, this seems like an OK option
    plugins_for_resolve = DictOption[str](
        help=softwrap(
            """
            A dictionary, whose keys are the names of each JVM resolve that requires default
            `scalac` plugins, and the value is a comma-separated string consisting of scalac plugin
            names. Each specified plugin must have a corresponding `scalac_plugin` target that specifies
            that name in either its `plugin_name` field or is the same as its target name.
            """
        ),
    )

    def parsed_args_for_resolve(self, resolve_name: str) -> list[str]:
        return list(self.args) + self.args_for_resolve.get(resolve_name, [])

    def parsed_default_plugins(self) -> dict[str, list[str]]:
        return {
            key: [i.strip() for i in value.split(",")]
            for key, value in self.plugins_for_resolve.items()
        }
