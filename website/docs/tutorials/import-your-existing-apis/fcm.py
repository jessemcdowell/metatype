# skip:start
from typegraph import TypeGraph, policies, t
from typegraph.providers.prisma.runtimes.prisma import PrismaRuntime

# isort: off
import sys
from pathlib import Path
from typegraph.runtimes.graphql import GraphQLRuntime

sys.path.append(str(Path(__file__).parent))
# skip:end
# highlight-next-line
from google import import_googleapi  # noqa: E402

# skip:next-line
# isort: on
with TypeGraph(
    "fcm",
    # skip:next-line
    cors=TypeGraph.Cors(allow_origin=["https://metatype.dev", "http://localhost:3000"]),
) as g:
    db = PrismaRuntime("database", "POSTGRES_CONN")
    gql = GraphQLRuntime("https://graphqlzero.almansi.me/api")
    # highlight-next-line
    googleapi = import_googleapi()
    public = policies.public()

    user = t.struct({"id": t.string(), "name": t.string()}).named("user")

    message = t.struct(
        {
            "id": t.integer().as_id.config("auto"),
            "title": t.string(),
        }
    ).named("message")

    g.expose(
        create_message=db.create(message),
        list_messages=db.find_many(message),
        users=gql.query(t.struct({}), t.struct({"data": t.array(user)})),
        user=gql.query(t.struct({"id": t.string().as_id}), user),
        # highlight-next-line
        send_notification=googleapi.functions.projectsMessagesSend,
        default_policy=[public],
    )
