import { Todo } from '../models/api-response.model';

type TodId = Todo['id'];

export interface TodoState {
  todo: Record<TodId, Todo>;
  tags: string[];
  filterTags: string[];
}
