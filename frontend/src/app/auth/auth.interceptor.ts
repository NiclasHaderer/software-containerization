import { HTTP_INTERCEPTORS, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { ErrorHandler, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { TodoStore } from '../state/todo.state';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private store: TodoStore
  ) {
  }

  public intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const account = this.store.state.account;
    if (account) {
      const modifiedReq = req.clone({
        headers: req.headers.set('Authorization', account.token),
      });
      return next.handle(modifiedReq);
    }
    return next.handle(req);
  }

}

@Injectable()
class AuthErrorHandler implements ErrorHandler {

  constructor(
    private store: TodoStore
  ) {
  }

  public handleError(error: any): void {
    if (error?.rejection?.status === 403) {
      this.store.dispatch("logout");
    }
  }
}


export const AUTH_INTERCEPTOR_PROVIDER = {
  provide: HTTP_INTERCEPTORS,
  useClass: AuthInterceptor,
  multi: true
};

export const AUTH_ERROR_PROVIDER = {
  provide: ErrorHandler,
  useClass: AuthErrorHandler,
};
