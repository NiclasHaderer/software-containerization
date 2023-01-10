import {
  AfterViewInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  Inject,
  Injector,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges
} from "@angular/core"
import {UntypedFormControl} from "@angular/forms"
import {TuiDialogService} from "@taiga-ui/core"
import {PolymorpheusComponent} from "@tinkoff/ng-polymorpheus"
import {Extensions} from "@tiptap/core"
import {Observable, Subscription} from "rxjs"
import {map} from "rxjs/operators"
import {extensions} from "../../helpers/extensions"
import {PostTodo, Todo} from "../../models/api-response.model"
import {TodoStore} from "../../state/todo.state"
import {EditTodoComponent} from "../edit-todo/edit-todo.component"

@Component({
  selector: "app-todo[todo]",
  templateUrl: "./todo.component.html",
  styleUrls: ["./todo.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TodoComponent implements OnInit, AfterViewInit, OnDestroy, OnChanges {
  @Input() todo!: Todo
  public readonly control = new UntypedFormControl([])
  public filteredTags$: Observable<string[]> | undefined
  public search: string = ""
  public extensions: Extensions = extensions
  private controlSubscription!: Subscription
  private readonly dialog = this.dialogService.open<PostTodo | void>(
    new PolymorpheusComponent(EditTodoComponent, this.injector), {
      size: "l",
      data: this
    }
  )

  constructor(
    private store: TodoStore,
    private cd: ChangeDetectorRef,
    @Inject(TuiDialogService) private readonly dialogService: TuiDialogService,
    @Inject(Injector) private readonly injector: Injector,
  ) {
  }

  public ngOnInit(): void {
    this.controlSubscription = this.control.valueChanges.subscribe(this.updateTagsForTodo.bind(this))
    this.filteredTags$ = this.store.on("tags").pipe(
      map(tags => tags.filter(tag => tag.toLocaleLowerCase().includes(this.search.toLocaleLowerCase())))
    )
  }

  public ngAfterViewInit(): void {
    this.cd.detectChanges()
  }

  public ngOnChanges(changes: SimpleChanges): void {
    this.control.setValue(this.todo.tags)
  }

  public ngOnDestroy(): void {
    this.controlSubscription.unsubscribe()
  }

  private updateTagsForTodo(tags: string[]) {
    this.store.dispatch("updateTodo", this.todo.id, {tags}).subscribe(() => {
      this.store.dispatch("getTags")
    })
  }

  public deleteTodo(): void {
    this.store.dispatch("deleteTodo", this.todo.id)
  }

  public editTodo(): void {
    this.dialog.subscribe(todo => todo && this.store.dispatch("updateTodo", this.todo.id, todo))
  }
}
