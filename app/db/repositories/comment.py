from app.db.models.comment import Comment
from app.db.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    model = Comment