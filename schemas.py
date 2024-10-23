from pydantic import BaseModel
from typing import Optional

class Song(BaseModel):
    title: str
    artist: str
    album: str
    year: int
    
    
class SongResponse(BaseModel):
    id: int 
    title: str
    artist: str
    album: str
    year: int


class SongUpdate(BaseModel):
    title: Optional[str] = None
    album: Optional[str] = None
    year: Optional[int] = None
    artist: Optional[str] = None

class CreatedUserRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str