import { Todo, UserAccount } from '../models/api-response.model';

type TodId = Todo['id'];

export interface TodoState {
  account: UserAccount | null;
  todo: Record<TodId, Todo>;
  tags: string[];
  filterTags: string[];
}
