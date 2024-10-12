"""Service for outputing offline recommendations (personal and top-popular)."""
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request

from .constants import PERSONAL_RECS_PATH, DEFAULT_RECS_PATH

# Setting up a logger with uvicorn output stream
logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)


class Recommender:
    """Class for generating offline recommendations."""

    def __init__(self):
        """Initializes a class instance."""
        # Attribute for storing rec-data
        self._recs = {
            "personal": None,
            "default": None,
        }
        # Attribute for storing request counts
        self._stats = {
            "request_personal_count": 0,
            "request_default_count": 0,
        }

    def load(self, rec_type, path, **kwargs):
        """Loads offline recommendations."""
        logger.info(f"Loading recommendations: {rec_type}")
        self._recs[rec_type] = pd.read_parquet(path, **kwargs)
        self._recs[rec_type] = self._recs[rec_type].sort_values(by="id")
        if rec_type == "personal":
            self._recs[rec_type] = self._recs[rec_type].sort_values(
                by=["user_id", "cb_score"],
                ascending=[True, False],
            )
            self._recs[rec_type] = self._recs[rec_type].set_index("user_id")
        logger.info("Recommendations loaded")

    def get(self, user_id: int, k: int = 10):
        """Generates k offline recommendations for user."""
        if user_id in self._recs["personal"].index:
            recs = self._recs["personal"].loc[user_id]
            recs = recs["item_id"].tolist()[:k]
            self._stats["request_personal_count"] += 1
            logger.info(f"user {user_id} - using personal history")
        else:
            recs = self._recs["default"]
            recs = recs["item_id"].tolist()[:k]
            self._stats["request_default_count"] += 1
            logger.info(f"user {user_id} - using default")

        return recs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads data on application start-up."""
    rec_store = Recommender()
    rec_store.load(rec_type="personal", path=PERSONAL_RECS_PATH)
    rec_store.load(rec_type="default", path=DEFAULT_RECS_PATH)

    yield {"rec_store": rec_store}


# Creating an app
app = FastAPI(title="recommendations_offline", lifespan=lifespan)


# Endpoint for getting offline recommendations
@app.post("/get_recs")
async def recommendations(request: Request, user_id: int, k: int):
    """Generates offline recommendations."""
    rec_store = request.state.rec_store

    i2i = rec_store.get(user_id, k)

    return i2i


@app.get("/healthy")
async def healthy():
    """Displays status message."""
    return {"status": "healthy"}


@app.get("/get_stats")
async def get_stats(request: Request):
    """Displays service statistics."""
    rec_store = request.state.rec_store

    return rec_store._stats
