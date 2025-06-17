# Aufgabe 7: Erstellen eines Validators für eine Post-Entität mit PydanticZiel:
# Definition eines Schemas für eine Post-Entität mit title, description, author,
# is_moderated, created_at, updated_at.
from datetime import datetime, timezone

from pydantic import BaseModel, constr, conint


class Category(BaseModel):
    title: constr(min_length=3, max_length=50)
    age: conint(gt=0)


class Post(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(min_length=3, max_length=100)
    author: constr(min_length=3, max_length=50)
    is_moderated: bool = False
    created_at: datetime = datetime.now(timezone.utc).isoformat()
    updated_at: datetime = None
    category: Category


category = {
    "title": "Schule",
    "age": 25
}

post_data = {
    "title": "Mein Titel",
    "description": "Eine Beschreibung.",
    "author": "Georg",
    "is_moderated": True,
    "created_at": "2025-06-14T15:30:00",
    "updated_at": "2025-06-14T16:00:00",
    "category": {
        "title": "Schule",
        "age": 25
    }
}


print(Post.model_validate(post_data).model_dump_json())
