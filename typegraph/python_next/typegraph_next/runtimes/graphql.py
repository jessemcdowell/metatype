# Copyright Metatype OÜ, licensed under the Mozilla Public License Version 2.0.
# SPDX-License-Identifier: MPL-2.0

from typing import List
from dataclasses import dataclass

from typegraph_next.runtimes.base import Materializer, Runtime
from typegraph_next.gen.types import Err
from typegraph_next.gen.exports.runtimes import (
    BaseMaterializer,
    Effect,
    EffectNone,
    GraphqlRuntimeData,
    MaterializerGraphqlQuery,
)
from typegraph_next.wit import runtimes, store
from typegraph_next import t


@dataclass
class QueryMat(Materializer):
    path: List[str]


@dataclass
class MutationMat(Materializer):
    path: List[str]


class GraphQLRuntime(Runtime):
    endpoint: str

    def __init__(self, endpoint: str):
        runtime_id = runtimes.register_graphql_runtime(
            store, GraphqlRuntimeData(endpoint=endpoint)
        )
        if isinstance(runtime_id, Err):
            raise Exception(runtime_id.value)

        super().__init__(runtime_id.value)
        self.endpoint = endpoint

    def query(self, inp: "t.struct", out: "t.typedef", *, path: List[str] = list()):
        mat_id = runtimes.graphql_query(
            store,
            BaseMaterializer(runtime=self.id, effect=EffectNone()),
            MaterializerGraphqlQuery(path=path),
        )

        if isinstance(mat_id, Err):
            raise Exception(mat_id.value)

        return t.func(inp, out, QueryMat(mat_id.value, effect=EffectNone(), path=path))

    def mutation(
        self,
        inp: "t.struct",
        out: "t.typedef",
        effect: Effect,
        *,
        path: List[str] = list()
    ):
        mat_id = runtimes.graphql_mutation(
            store,
            BaseMaterializer(runtime=self.id, effect=effect),
            MaterializerGraphqlQuery(path=path),
        )

        if isinstance(mat_id, Err):
            raise Exception(mat_id.value)

        return t.func(inp, out, MutationMat(mat_id.value, effect=effect, path=path))
