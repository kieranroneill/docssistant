from fastapi import APIRouter, Response, status

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@router.get("", status_code=200)
async def healthcheck(response: Response) -> None:
    response.status_code = status.HTTP_200_OK

    return
