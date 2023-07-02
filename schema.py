from ariadne import QueryType, make_executable_schema, gql, ObjectType, MutationType, UnionType, SubscriptionType
from todo.models import Todo, Reminder
from django.core.exceptions import ObjectDoesNotExist
import asyncio
from channels.db import database_sync_to_async


type_defs = gql("""
    type Query {
        hello: String!
        todoTasks: [Todo]!
        todoTask(pk: String!): Todo!
        searchTasks(name: String!): [Task!]
    }

    type Mutation {
        createTask(name:String!, description: String, category: TaskCategory!): Todo!
        updateTask(pk: Int!, name: String, description: String): Todo!
        deleteTask(pk: Int!): String
        deleteTasks: String
        createReminder(name: String!): Reminder!
    }

    type Subscription {
        getTodo: Todo!
    }

    interface Work {
        name: String
    }


    type Todo implements Work {
        pk: String
        name: String
        description: String
        category: TaskCategory!
    }

    type Reminder implements Work {
        name: String
        completed: Boolean!
    }

    enum TaskCategory {
        IMPORTANT
        URGENT
        DEFAULT
    }

    union Task = Todo | Reminder


""")


query = QueryType()

# resolver function for hello field in Query schema
@query.field("hello")
def resolve_hello(*_):
    return "Hello Prince"


@query.field("todoTasks")
async def resolve_todoTasks(obj, info):
    todo_tasks = await database_sync_to_async(lambda: Todo.objects.all())()
    return todo_tasks

# resolver function for todoTask field with a compulsory argument, pk.
@query.field("todoTask")
def resolve_todoTask(*_, pk):
    try:
        todo_task = database_sync_to_async(lambda: Todo.objects.get(pk=pk))()
        return todo_task
    except ObjectDoesNotExist:
        return "Todo task with name does not exist"


@query.field("searchTasks")
def resolve_searchTasks(*_, name):
    reminders = database_sync_to_async(Reminder.objects.filter(name=name))()
    todos = database_sync_to_async(Todo.objects.filter(name=name))()
    items = list(reminders) + list(todos)
    return items


mutation = MutationType()


@mutation.field("createTask")
def resolve_createTask(*_, name, description, category):
    # update create task operation to run synchronous database operation in async environment
    task = database_sync_to_async(lambda: Todo.objects.create(name=name, description=description, category=category))()
    database_sync_to_async(lambda: task.save())()
    return task

@mutation.field("updateTask")
def resolve_updateTask(*_, pk, name=None, description=None):
    task = database_sync_to_async(lambda: Todo.objects.get(pk=pk))()
    if name:
        task.name = name
    if description:
        task.description = description
    database_sync_to_async(lambda: task.save())()
    return task

@mutation.field("deleteTask")
def resolve_deleteTask(*_, pk):
    task = Todo.objects.get(pk=pk)
    task.delete()
    return "Task deleted"

@mutation.field("deleteTasks")
def resolve_deleteTasks(*_):
    tasks = Todo.objects.all()
    tasks.delete()
    return "Tasks deleted"

@mutation.field("createReminder")
def resolve_createReminder(obj, info, name):
    reminder = Reminder.objects.create(name=name)
    reminder.save()
    return reminder


subscription = SubscriptionType()

@subscription.source("getTodo")
async def retrieve_todo_created(*_):
    while True:
        await asyncio.sleep(1)
        # yield await database_sync_to_async(lambda: Todo.objects.last())()
        last_todo = await database_sync_to_async(Todo.objects.last)()
        yield last_todo

@subscription.field("getTodo")
async def resolve_getTodo(todo, obj):
    return todo


task = UnionType("Task")

# If obj is an instance of the Reminder model, the function returns the string "Reminder" as the resolved type name.
# If obj is an instance of the Todo model, the function returns the string "Todo" as the resolved type name.
# If obj is not an instance of either Reminder or Todo, the function returns None.

@task.type_resolver
def resolve_taskType(obj, *_):
    if isinstance(obj, Reminder):
        return "Reminder"
    if isinstance(obj, Todo):
        return "Todo"
    return None


# making the Python code schema executable in GraphQL
schema = make_executable_schema(type_defs, query, mutation, subscription, task)