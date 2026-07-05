from fastapi import FastAPI , Depends , HTTPException , Query
from sqlalchemy.orm import Session
from database import engine , sesslocal
import models , schemas
from auth import create_token,verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB dependnce
def get_db():
    db = sesslocal()
    try :
        yield db
    finally:
        db.close()

#login API
@app.post("/login")
def login():
    return{
        "access_token" : create_token({"user" : "admin"}),
        "token_type" : "bearer"
    }

#Home route
@app.get("/home")
def home():
    return{
        "message" : "blog api started"
    }

#Create Blog(protected)
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog : schemas.BlogCreate , db : Session = Depends(get_db),user=Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Get ALL Blogs
@app.get("/blogs")
def get_blogs(page: int =1,
              limit: int = 5,
              search:str = Query(default=""),
              db: Session = Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()

    return{
        "page": page,
        "limit": limit,
        "total": total,
        "data":blogs
    }

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
def update_blog(title:str, content:str ,blog:schemas.BlogCreate, blog_id : int , db : Session = Depends(get_db),user=Depends(verify_token)):
    new_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not new_blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    
    new_blog.title = blog.title # type: ignore
    new_blog.content = blog.content # type: ignore

    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blogs/{blog_id}",response_model=schemas.BlogResponse)
def delete_blog(blog_id : int , db : Session = Depends(get_db),user=Depends(verify_token)):
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