# skip:start
from typegraph import TypeGraph, policies, t
from typegraph.policies import Policy
from typegraph.runtimes.deno import PureFunMat
from typegraph.runtimes.random import RandomRuntime

# skip:end

with TypeGraph(
    "policies",
    auths=[
        TypeGraph.Auth.basic(["admin", "user"]),
    ],
    cors=TypeGraph.Cors(
        allow_origin=["https://metatype.dev", "http://localhost:3000"],
    ),
) as g:
    random = RandomRuntime(seed=0)
    public = policies.public()

    admin_only = Policy(
        PureFunMat(
            "(args, { context }) => context.username ? context.username === 'admin' : null"
        ),
    )
    user_only = Policy(
        PureFunMat(
            "(args, { context }) => context.username ? context.username === 'user' : null"
        ),
    )

    g.expose(
        public=random.generate(t.string()).add_policy(public),
        admin_only=random.generate(t.string()).add_policy(admin_only),
        user_only=random.generate(t.string()).add_policy(user_only),
        both=random.generate(t.string()).add_policy(user_only, admin_only),
    )
