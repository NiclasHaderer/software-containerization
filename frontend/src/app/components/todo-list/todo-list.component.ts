import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import {merge, Observable} from "rxjs"
import { map } from 'rxjs/operators';
import { Todo } from '../../models/api-response.model';
import { TodoStore } from '../../state/todo.state';

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TodoListComponent implements OnInit {
  public todoList$: Observable<Todo[]>;

  constructor(private store: TodoStore) {
    this.todoList$ = store.select("filteredTodos").pipe(map(todo => Object.values(todo)));
  }

  public async ngOnInit(): Promise<void> {
    this.store.dispatch("getTodos");
    this.store.dispatch("getTags");
  }

}
