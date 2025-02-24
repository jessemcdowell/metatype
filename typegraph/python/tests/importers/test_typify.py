# Copyright Metatype OÜ, licensed under the Mozilla Public License Version 2.0.
# SPDX-License-Identifier: MPL-2.0

from os import path

from typegraph import types as t
from typegraph.graph.typegraph import TypeGraph
from typegraph.importers.base.typify import Typify
from typegraph.importers.graphql import GraphQLImporter

importer = GraphQLImporter(
    "test",
    "https://example.com/api",
    file=path.join(path.dirname(__file__), "graphql_full_introspection.json"),
)


class TestImporterTypify:
    def test_simple_types(self, overridable):
        tp = Typify(importer)
        with TypeGraph(""):
            assert tp(t.boolean()) == overridable("t.boolean()")
            assert tp(t.float()) == overridable("t.float()")
            assert tp(t.integer()) == overridable("t.integer()")
            assert tp(t.string()) == overridable("t.string()")

    def test_simple_types_with_constraints(self, overridable):
        tp = Typify(importer)
        with TypeGraph(""):
            assert tp(t.float(x_min=0, x_max=10)) == overridable(
                "t.float().x_min(0).x_max(10)"
            )
            assert tp(t.uuid()) == overridable("t.string().format('uuid')")

    def test_optional(self, overridable):
        tp = Typify(importer)
        with TypeGraph(""):
            assert tp(t.optional(t.float())) == overridable("t.float().optional()")
            assert tp(t.string(min=12)) == overridable("t.string().min(12)")

    def test_struct(self, overridable):
        tp = Typify(importer)
        with TypeGraph("") as g:
            assert tp(
                t.struct(
                    {
                        "id": t.uuid(),
                        "email": t.email(),
                        "friends": g("User"),
                        "bestFriend": g("User").optional(),
                    }
                ).named("User")
            ) == overridable(
                "t.struct({'id': t.string().format('uuid'), 'email': t.string().format('email'), 'friends': t.proxy(renames['User']), 'bestFriend': t.proxy(renames['User']).optional()})"
            )
