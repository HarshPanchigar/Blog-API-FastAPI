from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
from database import engine , sesslocal
import models , schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB dependnce
def get_db():
    db = sesslocal()
    try :
        yield db
    finally:
        db.close()

#Home route
@app.get("/home")
def home():
    return{
        "message" : "blog api started"
    }

#Create Blog
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog : schemas.BlogCreate , db : Session = Depends(get_db)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Get ALL Blogs
@app.get("/blogs",response_model=list[schemas.BlogResponse])
def show_blogs(db : Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

#Get Blogs By ID
@app.get("/blogs/{blog_id}",response_model=schemas.BlogResponse)
def show_blog(blog_id : int , db : Session = Depends(get_db)):
    if not blog_id:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    return db.get(models.Blog,blog_id)

#Update blogs
@app.put("/blogs/{blog_id}",response_model=schemas.BlogResponse)
def update_blog(title:str, content:str ,blog:schemas.BlogCreate, blog_id : int , db : Session = Depends(get_db)):
    new_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not new_blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    
    new_blog.title = blog.title
    new_blog.content = blog.content

    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blogs/{blog_id}",response_model=schemas.BlogResponse)
def delete_blog(blog_id : int , db : Session = Depends(get_db)):
    blog = db.get(models.Blog,blog_id)

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    
    db.delete(blog)
    db.commit()
    return{
        "message" : "Blog Deleted Successfully"
    }