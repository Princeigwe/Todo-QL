from ariadne import QueryType, make_executable_schema, gql, ObjectType

type_defs = gql("""
    type Query {
        hello: String!
        user: User!
    }

    type User {
        firstName: String
        lastName: String!
    }
""")


query = QueryType()

# resolver function for hello field in Query schema
@query.field("hello")
def resolve_hello(*_):
    return "Hello Prince"

@query.field('user')
def resolve_user(obj, info):
    return user


user = ObjectType('User')


@user.field('firstName')
def resolve_user_firstName(*_):
    return "Prince"

@user.field('lastName')
def resolve_user_lastName(*_):
    return "Igwe"

# making the Python code schema executable in GraphQL
schema = make_executable_schema(type_defs, query, user)