from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from configs.database import session, engine, Base
from models import Song as SongModel
from sqlalchemy.orm import Session
from schemas import SongResponse, Song, SongUpdate
from auth import verify_token


router = APIRouter(prefix="/songs", tags=["songs"])
Base.metadata.create_all(bind= engine) 

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/add-song", response_model=SongResponse)
async def create_song(request: Song, db: db_dependency, user: dict = Depends(verify_token)):
    new_song = SongModel(
        title=request.title,
        artist=request.artist,
        album=request.album,
        year=request.year
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

@router.get("/", response_model= List[SongResponse])
async def get_songs(db: db_dependency, skip:int = 0, limit:int = 10, user: dict = Depends(verify_token)):
    songs = db.query(SongModel).offset(skip).limit(limit).all()
    return songs

@router.get("/{song_id}", response_model= SongResponse)
async def get_songs(song_id: int, db: db_dependency , user: dict = Depends(verify_token)):
    return get_song_or_404(song_id, db);

@router.put("/{song_id}")
async def update_song(song_id: int, song_request: SongUpdate, db: db_dependency , user: dict = Depends(verify_token)):
    db_song = get_song_or_404(song_id, db)
    
    db_song.title = song_request.title if song_request.title is not None else db_song.title 
    db_song.album = song_request.album if song_request.album is not None else db_song.album 
    db_song.year = song_request.year if song_request.year is not None else db_song.year 
    db_song.artist = song_request.artist if song_request.artist is not None else db_song.artist
    
    db.commit()
    db.refresh(db_song)
    return db_song 

@router.delete("/{song_id}", response_model=SongResponse)
async def delete_song(song_id: int, db: db_dependency, user: dict = Depends(verify_token)):
    db_song = get_song_or_404(song_id=song_id, db=db)
    db.delete(db_song)
    db.commit()
    return {"message": "Song deleted successfully"}



def get_song_or_404(song_id: int, db: Session):
    song = db.query(SongModel).filter(SongModel.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    
    return song



