# Copyright Metatype OÜ, licensed under the Mozilla Public License Version 2.0.
# SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass

from typegraph_next.gen.exports.core import MaterializerId, RuntimeId
from typegraph_next.gen.exports.runtimes import Effect


@dataclass
class Runtime:
    id: RuntimeId


@dataclass
class Materializer:
    id: MaterializerId
    effect: Effect
