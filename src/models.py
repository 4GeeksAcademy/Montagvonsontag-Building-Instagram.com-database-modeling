from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Users(db.Model):
    __tablename__='users'
    #the below attributes are shown up in admin/User
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    #Relationships
    posts: Mapped[list["Posts"]] = relationship(back_populates="users")
    comments: Mapped[list["Comments"]] = relationship(back_populates="users")
    followers: Mapped[list["Followers"]] = relationship(back_populates="user_from")
    following: Mapped[list["Followers"]] = relationship(back_populates="user_to")
    


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            #Object from table "Post":
            "posts": [post.serialize() for post in self.posts]
            # do not serialize the password, its a security breach
        }

class Followers(db.Model): 
    __tablename__='followers'
    #the below attributes are shown up on admin/User
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    # Relationships
    user_from: Mapped["Users"] = relationship(back_populates="follower")
    user_to: Mapped["Users"] = relationship(back_populates="following")

    def serialize(self):
        return {
            "follower": self.user_from_id,
            "following": self.user_to_id,
        }
    
#relacion de uno a muchos entre User y Posts
class Posts(db.Model):
    __tablename__='posts' ## cambiad de post
    id: Mapped[int] = mapped_column(primary_key=True)
    post_text: Mapped[str] = mapped_column(String(250), nullable=False)
    #Connection via foreignkey
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Relationships
    user: Mapped["Users"] = relationship(back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship(back_populates="posts")
  
    def serialize(self):
        return {
           "id": self.id,
            "user": self.user_id,
            "post_text": self.post_text,
            "comments": [comment.serialize() for comment in self.comments],
                
            }          
        
    
class Comments(db.Model):
    __tablename__='comments' 
    comment_id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
    # Connection via Foreignkey
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    #Relationships
    posts: Mapped["Posts"] = relationship(back_populates="comments")
    user: Mapped["Users"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.comment_id,
            "comment": self.comment_text,
            "author": self.author_id,
            "post": self.post_id
        }
   