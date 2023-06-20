from ariadne import QueryType, make_executable_schema, gql, ObjectType, MutationType
from todo.models import Todo
from django.core.exceptions import ObjectDoesNotExist

type_defs = gql("""
    type Query {
        hello: String!
        user: User!
        todoTasks: [Todo]!
        todoTask(pk: String!): Todo!
    }

    type Mutation {
        createTask(name:String!, description: String): Todo!
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

# resolver function for todoTask field with a compulsory argument, pk.
@query.field("todoTask")
def resolve_todoTask(*_, pk):
    try:
        todo_task = Todo.objects.get(pk=pk)
        return todo_task
    except ObjectDoesNotExist:
        return "Todo task with name does not exist"


mutation = MutationType()

@mutation.field("createTask")
def resolve_createTask(*_, name, description):
    task = Todo.objects.create(name=name, description=description)
    task.save()
    return task


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
schema = make_executable_schema(type_defs, user, query, mutation)