import { DOCUMENT } from '@angular/common';
import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { getThemeString, storeThemeValue, ThemeType } from '../helpers/theme';

// @dynamic
@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private _theme$: BehaviorSubject<ThemeType>;
  public theme$: Observable<ThemeType>;

  constructor(
    @Inject(DOCUMENT) private document: Document
  ) {
    const theme = getThemeString();
    this._theme$ = new BehaviorSubject(theme);
    this.theme$ = this._theme$.asObservable();
    this.theme = theme;
  }

  public get theme(): ThemeType {
    return this._theme$.value;
  }

  public set theme(value: ThemeType) {
    storeThemeValue(value);
    this.document.body.classList.remove(this.theme);
    this.document.body.classList.add(value);
    this._theme$.next(value);
  }
}
