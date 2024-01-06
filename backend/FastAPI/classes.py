from pydantic import BaseModel

# -----------Classes-----------
class Data(BaseModel):
    data: str
    
class Dates(BaseModel):
    start_date: str = None
    stop_date: str = None
    
class Location(BaseModel):
    lat: float
    lon: float
