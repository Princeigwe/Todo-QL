from ariadne import QueryType, make_executable_schema, gql, ObjectType, MutationType
from todo.models import Todo
from django.core.exceptions import ObjectDoesNotExist

type_defs = gql("""
    type Query {
        hello: String!
        todoTasks: [Todo]!
        todoTask(pk: String!): Todo!
    }

    type Mutation {
        createTask(name:String!, description: String): Todo!
        updateTask(pk: Int!, name: String, description: String): Todo!
        deleteTask(pk: Int!): String
    }


    type Todo {
        pk: String
        name: String
        description: String
    }
""")


query = QueryType()

# resolver function for hello field in Query schema
@query.field("hello")
def resolve_hello(*_):
    return "Hello Prince"


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

@mutation.field("updateTask")
def resolve_updateTask(*_, pk, name=None, description=None):
    task = Todo.objects.get(pk=pk)
    if name:
        task.name = name
    if description:
        task.description = description
    task.save()
    return task

@mutation.field("deleteTask")
def resolve_deleteTask(*_, pk):
    task = Todo.objects.get(pk=pk)
    task.delete()
    return "Task deleted"


# making the Python code schema executable in GraphQL
schema = make_executable_schema(type_defs, query, mutation)