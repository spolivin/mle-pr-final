# Constants for inter-container communication
MAIN_URL = "http://fastapi_app"
OFFLINE_URL = "http://offline_app"
EVENTS_URL = "http://events_app"
FEATURES_URL = "http://features_app"

# URL for sending API requests
HOST_URL = "http://0.0.0.0"

# Ports for connecting to endpoints between containers
MAIN_APP_PORT = 8000
RECS_OFFLINE_SERVICE_PORT = 8001
EVENTS_SERVICE_PORT = 8002
FEATURES_SERVICE_PORT = 8003

# Paths to recommendation data
PERSONAL_RECS_PATH = "recommendations/candidates_ranked.parquet"
DEFAULT_RECS_PATH = "recommendations/default_recs.parquet"
ONLINE_RECS_PATH = "recommendations/online_recs.parquet"
