from fastapi import FastAPI, Response, status, HTTPException
from .models import Post, UserCreate
from .database import cursor, conn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hruthi": "KR"}

# --- USER ENDPOINTS ---

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    # In a real app, you would hash the password here (e.g., using passlib/bcrypt)
    cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """,
                   (user.email, user.password))
    new_user = cursor.fetchone()
    conn.commit()
    return {"data": new_user}

# --- POST ENDPOINTS ---

@app.get("/posts")
def get_posts():
    # This is the SQL JOIN! It pulls data from both 'posts' and 'users' in one query.
    cursor.execute("""
        SELECT posts.*, users.email AS owner_email 
        FROM posts 
        LEFT JOIN users ON posts.owner_id = users.id
    """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, owner_id: int):
    # We now take an owner_id to link the post to a user
    cursor.execute("""INSERT INTO posts (title, content, published, rating, owner_id) VALUES (%s, %s, %s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published, post.rating, owner_id))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    # Joining here too so we get the owner email for a single post
    cursor.execute("""
        SELECT posts.*, users.email AS owner_email 
        FROM posts 
        LEFT JOIN users ON posts.owner_id = users.id 
        WHERE posts.id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, post.rating, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"data": updated_post}