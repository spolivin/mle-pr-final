"""Service for outputing online recommendations (item similarity)."""
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request

from .constants import ONLINE_RECS_PATH

# Setting up a logger with uvicorn output stream
logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)


class SimilarItems():
    """Class for displaying online recommendations."""
    def __init__(self) -> None:
        """Initializes a class instance."""
        self._similar_items = None

    def load(self, path: str, **kwargs):
        """Loads online recommendatiions."""
        logger.info("Loading similarity data")
        self._similar_items = pd.read_parquet(path, **kwargs)
        self._similar_items = self._similar_items.sort_values(
            by=["itemid_1", "score"],
            ascending=[True, False],
        )
        self._similar_items = self._similar_items.set_index("itemid_1")
        logger.info("Loaded similarity data")

    def get(self, item_id: int, k: int = 10):
        """Retrieves first k online recommendations."""
        try:
            i2i = self._similar_items.loc[item_id].head(k)
            i2i = i2i[["itemid_2", "score"]].to_dict(orient="list")
        except KeyError:
            logger.error("No recommendations found")
            i2i = {"itemid_2": [], "score": []}
        
        return i2i


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads data on application start-up."""
    sim_items_store = SimilarItems()
    sim_items_store.load(path=ONLINE_RECS_PATH)
    logger.info("Ready for online recommendations")

    yield {"sim_items_store": sim_items_store}


# Creating an app
app = FastAPI(title="features", lifespan=lifespan)

@app.get("/healthy")
async def healthy():
    """Displays status message."""
    return {
        "status": "healthy"
    }

# Adding an endpoint for online recommendations
@app.post("/similar_items")
async def similar_items(request: Request, item_id: int, k: int):
    """Generates online recommendations."""
    # Getting an object with loaded data
    sim_items_store = request.state.sim_items_store
    # Getting recommendations
    i2i = sim_items_store.get(item_id, k)

    return i2i
