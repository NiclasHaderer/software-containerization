import {Injectable} from "@angular/core"
import {Store, StoreContext} from "rx-observable-state"
import {lastValueFrom} from "rxjs"
import {PostTodo, Todo} from "../models/api-response.model"
import {TodoApiService} from "../services/todo-api.service"
import {TodoState} from "./state.model"


type TodoStoreContext = StoreContext<TodoState, StoreSelector, StoreDispatcher>

class StoreSelector {
  public filteredTodos(state: TodoState): Record<string, Todo> {
    const {filterTags, todo} = state
    const todoList = Object.values(todo).filter(todo => todo.tags.some(i => filterTags.includes(i)))
    if (todoList.length === 0) return todo
    return todoList.reduce((todoMap, todoItem) => {
      todoMap[todoItem.id] = todoItem
      return todoMap
    }, {} as Record<string, Todo>)
  }

}

class StoreDispatcher {
  constructor(private todoApi: TodoApiService) {
  }

  public async getTodos(context: TodoStoreContext): Promise<void> {
    const todos = await lastValueFrom(this.todoApi.getTodos())
    let todosToPatch = context.state.todo
    for (let todo of todos) {
      todosToPatch = {
        ...todosToPatch,
        [todo.id]: todo
      }
    }
    context.patch(todosToPatch, "todo")
  }

  public async getTodo(context: TodoStoreContext, todoId: number): Promise<void> {
    const todo = await lastValueFrom(this.todoApi.getTodo(todoId))
    let todosToPatch = context.state.todo
    todosToPatch = {
      ...todosToPatch,
      [todo.id]: todo
    }
    context.patch(todosToPatch, "todo")
  }

  public async getTodoByTag(context: TodoStoreContext, tagName: string): Promise<void> {
    const taggedTodos = await lastValueFrom(this.todoApi.getTaggedTodos(tagName))
    let todosToPatch = context.state.todo
    for (let todo of taggedTodos) {
      todosToPatch = {
        ...todosToPatch,
        [todo.id]: todo
      }
    }

    context.patch(todosToPatch, "todo")
  }

  public async deleteTodo(context: TodoStoreContext, todoId: number): Promise<void> {
    await lastValueFrom(this.todoApi.deleteTodo(todoId))
    const {[todoId]: value, ...newValue} = context.state.todo
    context.patch(newValue, "todo")
    await context.dispatch("getTags")
  }

  public async updateTodo(context: TodoStoreContext, todoId: number, todo: Partial<PostTodo>): Promise<void> {
    const updatedTodo = await lastValueFrom(this.todoApi.updateTodo(todoId, todo))
    const newValue = {
      ...context.state.todo,
      [todoId]: updatedTodo
    }
    context.patch(newValue, "todo")

  }

  public async createTodo(context: TodoStoreContext, todo: PostTodo): Promise<void> {
    const newTodo = await lastValueFrom(this.todoApi.createTodo(todo))
    const newValue = {
      ...context.state.todo,
      [newTodo.id]: newTodo
    }
    context.patch(newValue, "todo")
    context.patch(Array.from(new Set([...context.state.tags, ...newTodo.tags])), "tags")
  }

  public async getTags(context: TodoStoreContext): Promise<void> {
    const tags = await lastValueFrom(this.todoApi.getTags())
    context.patch(tags, "tags")
  }

  public filterByTag(context: TodoStoreContext, tags: Record<string, boolean>): void {
    const selectedTags = []
    for (const tag of Object.keys(tags)) {
      if (tags[tag]) selectedTags.push(tag)
    }
    context.patch(selectedTags, "filterTags")
  }
}


@Injectable({providedIn: "root"})
export class TodoStore extends Store<TodoState, StoreDispatcher, StoreSelector> {
  constructor(
    private todoApi: TodoApiService,
  ) {
    super({
      todo: {},
      tags: [],
      filterTags: []
    }, {
      selector: new StoreSelector(),
      dispatcher: new StoreDispatcher(todoApi)
    })
  }
}
