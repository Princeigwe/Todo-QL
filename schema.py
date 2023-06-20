from ariadne import QueryType, make_executable_schema, gql, ObjectType
from todo.models import Todo

type_defs = gql("""
    type Query {
        hello: String!
        user: User!
        todoTasks: [Todo]!
    }

    type User {
        firstName: String
        lastName: String!
    }

    type Todo {
        name: String
        description: String
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

@query.field("todoTasks")
def resolve_todoTasks(*_):
    todo_tasks = Todo.objects.all()
    return todo_tasks


user = ObjectType('User')


@user.field('firstName')
def resolve_user_firstName(*_):
    return "Prince"

@user.field('lastName')
def resolve_user_lastName(*_):
    return "Igwe"

todo = ObjectType('Todo')

@todo.field('name')
def resolve_todo_name(*_):
    pass

# making the Python code schema executable in GraphQL
schema = make_executable_schema(type_defs, query, user)