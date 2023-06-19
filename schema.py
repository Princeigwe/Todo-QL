from ariadne import QueryType, make_executable_schema, gql

type_defs = gql("""
    type Query {
        hello: String!
    }
""")


query = QueryType()

# resolver function for hello field in Query schema
@query.field("hello")
def resolve_hello(*_):
    return "Hello Prince"

# making the Python code schema executable in GraphQL
schema = make_executable_schema(type_defs, query)