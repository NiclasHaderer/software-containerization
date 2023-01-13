import {ChangeDetectionStrategy, ChangeDetectorRef, Component, NgZone, OnDestroy, OnInit} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {filter, Subscription} from "rxjs";

@Component({
  selector: 'app-version',
  template: `
    Backend Version: {{version}}
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VersionDisplayComponent implements OnInit, OnDestroy {
  protected version: string | undefined
  private subscription: Subscription | undefined;

  constructor(
    private http: HttpClient,
    private ngZone: NgZone,
    private cd: ChangeDetectorRef
  ) {
  }

  public ngOnInit() {
    this.ngZone.runOutsideAngular(() => {
      this.checkForVersionChange()
      setInterval(() => this.checkForVersionChange(), 1000)
    })
  }

  public ngOnDestroy() {
    this.subscription?.unsubscribe()
  }

  public checkForVersionChange() {
    this.subscription = this.http.get<{ version: string }>(`${environment.apiURL}/version`).pipe(
      filter(({version}) => version !== this.version)
    ).subscribe(({version}) => {
      this.version = version;
      this.cd.detectChanges()
    })
  }

}
