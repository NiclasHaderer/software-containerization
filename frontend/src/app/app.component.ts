import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ThemeService } from './services/theme.service';
import { TodoStore } from './state/todo.state';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent implements OnInit {

  constructor(
    private store: TodoStore,
    public theme: ThemeService
  ) {
  }

  public async ngOnInit(): Promise<void> {
  }
}
