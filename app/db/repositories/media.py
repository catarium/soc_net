from app.db.models.media import Media
from app.db.repositories.base import BaseRepository


class MediaRepository(BaseRepository[Media]):
    model = Media
