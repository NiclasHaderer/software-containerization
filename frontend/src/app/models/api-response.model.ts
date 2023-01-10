export interface UserAccount {
  username: string;
  token: string;
  id: number;
}

export interface Todo {
  heading: string,
  content: string,
  tags: string[],
  imageUrl?: string,
  date: number,
  user_id: number,
  id: number
}

export interface PostTodo {
  heading: string,
  content: string,
  tags: string[],
  imageUrl?: string,
}

export interface Error {
  error: { detail: string }
}
