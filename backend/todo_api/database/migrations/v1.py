from databases import Database


# class PostTodo(BaseModel):
#     tags: List[str] = Field(default_factory=list)


async def migrate(db: Database):
    await db.execute("""CREATE TABLE todos
(
    id       serial PRIMARY KEY,
    heading  text NOT NULL,
    content  text NOT NULL,
    done     bool NOT NULL,
    imageURL text,
    date     float
)
    """)


async def rollback(db: Database):
    await db.execute("DROP TABLE todos")
