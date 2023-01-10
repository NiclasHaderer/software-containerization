export interface Todo {
  heading: string,
  content: string,
  tags: string[],
  imageUrl?: string,
  date: number,
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
