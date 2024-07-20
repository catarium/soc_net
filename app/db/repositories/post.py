from app.db.models.post import Post
from app.db.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    model = Post
