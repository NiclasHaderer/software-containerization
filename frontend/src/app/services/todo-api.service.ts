import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from '../../environments/environment';
import {PostTodo, Todo} from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class TodoApiService {

  constructor(
    private http: HttpClient
  ) {
  }

  public getTodos(): Observable<Todo[]> {
    return this.http.get<Todo[]>(`${environment.apiURL}/todo`);
  }

  public getTodo(todoID: number): Observable<Todo> {
    return this.http.get<Todo>(`${environment.apiURL}/todo/${todoID}`);
  }

  public deleteTodo(todoID: number): Observable<null> {
    return this.http.delete<null>(`${environment.apiURL}/todo/${todoID}`);
  }

  public updateTodo(todoID: number, newData: Partial<PostTodo>): Observable<Todo> {
    return this.http.patch<Todo>(`${environment.apiURL}/todo/${todoID}`, newData);
  }

  public createTodo(todo: PostTodo): Observable<Todo> {
    return this.http.post<Todo>(`${environment.apiURL}/todo/`, todo);
  }

  public getTags(): Observable<string[]> {
    return this.http.get<string[]>(`${environment.apiURL}/tags`);
  }

  public getTaggedTodos(tagName: string): Observable<Todo[]> {
    return this.http.get<Todo[]>(`${environment.apiURL}/tags/${tagName}`);
  }

  public search(query: string): Observable<Todo[]> {
    return this.http.get<Todo[]>(`${environment.apiURL}/search?q=${query}`);
  }
}
