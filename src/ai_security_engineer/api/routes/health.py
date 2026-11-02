from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Service health check")
def health_check() -> dict[str, str]:
    """Return a minimal liveness response without querying external systems."""
    return {"status": "ok"}
