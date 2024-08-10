from typing import List

from app.db.models.post import Post
from app.db.repositories.base import BaseRepository, ModelType


class PostRepository(BaseRepository[Post]):
    model = Post

    # async def create(self, media**obj_in_data) -> ModelType:

