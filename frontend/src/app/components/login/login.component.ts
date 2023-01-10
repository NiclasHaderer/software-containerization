import {ChangeDetectionStrategy, Component, Inject, OnInit} from "@angular/core"
import {UntypedFormControl, UntypedFormGroup, Validators} from "@angular/forms"
import {Router} from "@angular/router"
import { TuiNotification, TuiAlertService } from "@taiga-ui/core"
import {lastValueFrom} from "rxjs"
import {TodoStore} from "../../state/todo.state"

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent implements OnInit {
  public formControl!: UntypedFormGroup
  public mode: "login" | "signup" = "login"

  constructor(
    private store: TodoStore,
    @Inject(TuiAlertService) private readonly notificationsService: TuiAlertService,
    private router: Router
  ) {
  }

  public ngOnInit(): void {
    const mode = this.router.parseUrl(this.router.url).queryParams.mode
    if (mode === "signup") {
      this.mode = "signup"
    } else {
      this.mode = "login"
    }


    this.formControl = new UntypedFormGroup({
      username: new UntypedFormControl("", Validators.required),
      password: new UntypedFormControl("", Validators.required),
      rememberLogin: new UntypedFormControl(false)
    })
  }

  public login(): void {
    const userPass = this.extractFormData()
    if (!userPass) return

    const rememberLogin: boolean = this.formControl.get("rememberLogin")!.value
    try {
      this.store.dispatch("login", userPass.username, userPass.password, rememberLogin).subscribe(async () => {
        await this.router.navigate(["/"])
      })
    } catch (e) {
      this.showError(e)
    }
  }


  public async signup(): Promise<void> {
    const userPass = this.extractFormData()
    if (!userPass) return

    try {
      await lastValueFrom(this.store.dispatch("createAccount", userPass.username, userPass.password))
      await this.router.navigate(["/login"])
      this.notificationsService.open("Successfully created Account", {
        status: TuiNotification.Success,
        hasCloseButton: false,
      }).subscribe()
      this.mode = "login"
      this.formControl.get("username")?.setValue("")
      this.formControl.get("password")?.setValue("")
      this.formControl.markAsPristine()
      this.formControl.markAsUntouched()
    } catch (e) {
      this.showError(e)
    }
  }

  private extractFormData(): { username: string, password: string } | null {
    if (!this.formControl.valid) {
      this.formControl.markAllAsTouched()
      Object.values(this.formControl.controls).forEach(control => control.updateValueAndValidity())
      return null
    }
    const username = this.formControl.get("username")!.value
    const password = this.formControl.get("password")!.value
    return {username, password}
  }

  private showError(e: any) {
    this.notificationsService.open(e.error.detail, {
      label: "Something went wrong",
      status: TuiNotification.Error,
      hasCloseButton: false,
    }).subscribe()
  }

  public async enterHotkey(event: KeyboardEvent): Promise<void> {
    if (event.key !== "Enter") return event.stopPropagation()

    if (this.mode === "login") {
      await this.login()
    } else {
      await this.signup()
    }

  }
}
