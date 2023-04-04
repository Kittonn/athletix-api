from fastapi import APIRouter, HTTPException, status
from ..database import stadium
from ..internal.news import News

router = APIRouter(
    prefix="/news", tags=["news"], responses={404: {"description": "Not found"}})


@router.get("/")
async def get_news():
  return stadium.get_news()


@router.get("/{id}")
async def get_news_by_id(id: str):
  news = stadium.get_news_by_id(id)
  if news is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
  return news


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_news(body: dict):
  new_news = News(title=body["title"], content=body["content"],
                  image_url=body["image_url"], author=body["author"], draft=body["draft"])

  news = stadium.get_news_by_title(body["title"])

  print(news)

  if news is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="News already existed")

  stadium.add_news(new_news)
  return new_news


@router.patch("/{id}")
async def update_news(id: str, body: dict):
  updated_news = stadium.update_news(id, body)

  if updated_news is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="News not found")

  return updated_news


@router.delete("/{id}")
async def delete_news(id: str):
  deleted_news = stadium.delete_news(id)
  if deleted_news is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
  return HTTPException(status_code=status.HTTP_200_OK, detail="Delete news successfully")
