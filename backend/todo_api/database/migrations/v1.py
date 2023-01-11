from databases import Database


# class PostTodo(BaseModel):
#     tags: List[str] = Field(default_factory=list)


async def migrate(db: Database):
    await db.execute("""CREATE TABLE todos
(
    id        uuid PRIMARY KEY,
    heading   text NOT NULL,
    content   text NOT NULL,
    done      bool NOT NULL,
    tags      text[] NOT NULL,
    image_url text,
    created   float NOT NULL 
)
    """)


async def rollback(db: Database):
    await db.execute("DROP TABLE todos")
