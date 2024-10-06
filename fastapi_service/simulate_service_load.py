"""Simulates the conditions of sending numerous API requests."""
import time

import numpy as np

from test_service import send_test_request


if __name__ == "__main__":
    # Users with personal history
    user_ids_personal_history = [54791, 78724, 79627, 104829, 152693, 152963, 163049]
    # Random user ids
    user_ids_random = np.random.choice(1000, 7, replace=False).tolist()
    # Combining user ids together and reshuffling
    user_ids = user_ids_personal_history + user_ids_random
    np.random.shuffle(user_ids)

    # Running a series of requests
    for user_id in user_ids:
        user_params = {"user_id": user_id, "k": 5}
        res = send_test_request(
            params=user_params, 
            url="http://0.0.0.0:8000",
            endpoint="/recommendations",
        )
        time.sleep(5)
