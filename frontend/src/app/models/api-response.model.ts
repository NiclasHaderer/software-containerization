export interface Todo {
  heading: string,
  content: string,
  tags: string[],
  image_url?: string,
  created: number,
  id: string
}

export interface PostTodo {
  heading: string,
  content: string,
  tags: string[],
  image_url?: string,
}

export interface Error {
  error: { detail: string }
}
