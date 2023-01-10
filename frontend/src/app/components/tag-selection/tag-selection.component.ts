import {ChangeDetectionStrategy, Component, OnDestroy, OnInit} from "@angular/core"
import {UntypedFormBuilder, UntypedFormControl, UntypedFormGroup} from "@angular/forms"
import {Observable, Subscription} from "rxjs"
import {tap} from "rxjs/operators"
import {TodoStore} from "../../state/todo.state"

@Component({
  selector: "app-tag-selection",
  templateUrl: "./tag-selection.component.html",
  styleUrls: ["./tag-selection.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TagSelectionComponent implements OnInit, OnDestroy {
  public formGroup: UntypedFormGroup
  public tags$!: Observable<string[]>
  private subscription!: Subscription

  constructor(
    private store: TodoStore,
    private formBuilder: UntypedFormBuilder,
  ) {
    this.formGroup = this.formBuilder.group({})
  }

  ngOnInit(): void {
    this.tags$ = this.store.on("tags").pipe(
      tap((tagList: string[]) => {
        for (let tag of tagList) {
          if (!this.formGroup.get(tag)) {
            this.formGroup.addControl(tag, new UntypedFormControl(false))
          }
        }
      })
    )
    this.subscription = this.formGroup.valueChanges.subscribe(v => this.store.dispatch("filterByTag", v))
  }


  ngOnDestroy(): void {
    this.subscription.unsubscribe()
  }

}
