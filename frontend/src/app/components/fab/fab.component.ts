import { ChangeDetectionStrategy, Component, Inject, Injector } from '@angular/core';
import { TuiDialogService } from '@taiga-ui/core';
import { PolymorpheusComponent } from '@tinkoff/ng-polymorpheus';
import { PostTodo } from '../../models/api-response.model';
import { TodoStore } from '../../state/todo.state';
import { EditTodoComponent } from '../edit-todo/edit-todo.component';

@Component({
  selector: 'app-fab',
  templateUrl: './fab.component.html',
  styleUrls: ['./fab.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FabComponent {
  private readonly dialog = this.dialogService.open<void | PostTodo>(
    new PolymorpheusComponent(EditTodoComponent, this.injector), {
      size: 'l',
    }
  );

  constructor(
    @Inject(TuiDialogService) private readonly dialogService: TuiDialogService,
    @Inject(Injector) private readonly injector: Injector,
    private store: TodoStore
  ) {
  }

  public openDialog(): void {
    this.dialog.subscribe(value => {
      if (!value) return;
      this.store.dispatch("createTodo", value);
    });
  }
}
