from typing import List

from app.db.models.post import Post
from app.db.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    model = Post

    # async def select(
    #         self,
    #         custom_where=None,
    #         custom_order=None,
    #         custom_limit=None,
    #         custom_offset=None,
    # ) -> List[model]:

