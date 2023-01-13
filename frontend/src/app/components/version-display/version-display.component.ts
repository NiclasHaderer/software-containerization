import {ChangeDetectionStrategy, ChangeDetectorRef, Component, NgZone, OnDestroy, OnInit} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {filter} from "rxjs";

@Component({
  selector: 'app-version',
  template: `
    <span (click)="toggleVersionCheck()">Backend Version: {{version}}</span>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VersionDisplayComponent implements OnInit, OnDestroy {
  protected version: string | undefined
  private intervalID: number | undefined

  constructor(
    private http: HttpClient,
    private ngZone: NgZone,
    private cd: ChangeDetectorRef
  ) {
  }

  public ngOnInit() {
    this.ngZone.runOutsideAngular(() => this.startVersionCheck())
  }

  public ngOnDestroy() {
    clearInterval(this.intervalID)
  }

  public checkForVersionChange() {
    this.http.get<{ version: string }>(`${environment.apiURL}/version`).pipe(
      filter(({version}) => version !== this.version)
    ).subscribe(({version}) => {
      this.version = version;
      this.cd.detectChanges()
    })
  }

  protected toggleVersionCheck() {
    if (this.intervalID) {
      clearInterval(this.intervalID)
      this.intervalID = undefined
    } else {
      this.startVersionCheck()
    }
  }

  private startVersionCheck() {
    this.checkForVersionChange()
    this.intervalID = setInterval(() => this.checkForVersionChange(), 1000) as unknown as number
  }
}
