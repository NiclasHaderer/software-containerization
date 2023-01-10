import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { cache } from '../helpers/cache';
import { PostTodo, Todo, UserAccount } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class TodoApiService {

  constructor(
    private http: HttpClient
  ) {
  }

  public login(username: string, password: string): Observable<UserAccount> {
    return this.http.post<UserAccount>(`${environment.apiURL}/login`, {username, password});
  }

  @cache()
  public getAccount(): Observable<UserAccount> {
    return this.http.get<UserAccount>(`${environment.apiURL}/account`);
  }

  public getTodos(): Observable<Todo[]> {
    return this.http.get<Todo[]>(`${environment.apiURL}/todo`);
  }

  @cache()
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

  public createAccount(username: string, password: string): Observable<null> {
    return this.http.post<null>(`${environment.apiURL}/create-account/`, {username, password});
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
