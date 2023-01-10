import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
// TODO: (Taiga UI migration) TuiColorModule has been deleted in 3.0, please use CSS custom properties
import { TuiButtonModule, TuiColorModule, TuiDataListModule, TuiDialogModule, TuiHostedDropdownModule, TuiModeModule, TuiRootModule, TuiScrollbarModule, TuiSvgModule, TuiTextfieldControllerModule, TuiThemeNightModule, TuiAlertModule, TuiDropdownModule, TuiErrorModule } from '@taiga-ui/core';
import { TuiAvatarModule, TuiBadgeModule, TuiCheckboxLabeledModule, TuiDataListWrapperModule, TuiInputModule, TuiInputPasswordModule, TuiInputTagModule, TuiMarkerIconModule, TuiToggleModule, TuiFieldErrorPipeModule } from '@taiga-ui/kit';
import { NgxTipTapEditorModule } from 'ngx-tiptap-editor';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TodoComponent } from './components/todo/todo.component';
import { TodoListComponent } from './components/todo-list/todo-list.component';
import { HeaderComponent } from './components/header/header.component';
import { ThemeToggleComponent } from './components/theme-toggle/theme-toggle.component';
import { CardComponent } from './components/card/card.component';
import { FabComponent } from './components/fab/fab.component';
import { TagSelectionComponent } from './components/tag-selection/tag-selection.component';
import { HomeComponent } from './components/home-component/home.component';
import { LoginComponent } from './components/login/login.component';
import { AUTH_INTERCEPTOR_PROVIDER, AUTH_ERROR_PROVIDER } from './auth/auth.interceptor';
import { EditTodoComponent } from './components/edit-todo/edit-todo.component';

@NgModule({
  declarations: [
    AppComponent,
    TodoComponent,
    TodoListComponent,
    HeaderComponent,
    ThemeToggleComponent,
    CardComponent,
    FabComponent,
    TagSelectionComponent,
    HomeComponent,
    LoginComponent,
    EditTodoComponent,
  ],
  imports: [
    TuiAlertModule,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    TuiRootModule,
    TuiThemeNightModule,
    TuiModeModule,
    TuiToggleModule,
    FormsModule,
    ReactiveFormsModule,
    TuiHostedDropdownModule,
    TuiDropdownModule,
    TuiDataListModule,
    TuiAvatarModule,
    TuiSvgModule,
    TuiMarkerIconModule,
    TuiBadgeModule,
    TuiInputTagModule,
    TuiTextfieldControllerModule,
    TuiDataListWrapperModule,
    TuiCheckboxLabeledModule,
    TuiScrollbarModule,
    TuiInputModule,
    TuiInputPasswordModule,
    TuiButtonModule,
    TuiDialogModule,
    NgxTipTapEditorModule,
    TuiColorModule,
    TuiFieldErrorPipeModule,
      TuiErrorModule
],
  providers: [
    AUTH_INTERCEPTOR_PROVIDER,
    AUTH_ERROR_PROVIDER
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
