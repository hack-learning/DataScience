from typing import Optional

from pydantic import BaseModel

class MyException(Exception):
    pass

class News(BaseModel):
    
	title: str
	overview: str
	url: str
	body: str
	pub_date: str
    
