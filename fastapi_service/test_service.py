"""Tests the recommendations service."""
import logging
import unittest

import requests

from recsys_app.constants import (
    HOST_URL,
    MAIN_APP_PORT,
    EVENTS_SERVICE_PORT,
)

# Request components
headers = {"Content-type": "application/json", "Accept": "text/plain"}
main_app_url = HOST_URL + ":" + str(MAIN_APP_PORT)
events_url = HOST_URL + ":" + str(EVENTS_SERVICE_PORT)

# Configuring the logger
logger = logging.getLogger("unittest_logger")
logger.setLevel(logging.INFO)
# Configuring handler for logging to file
file_handler = logging.FileHandler("test_service.log")
file_handler.setLevel(logging.INFO)
# Configuring formatter for log message format
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
file_handler.setFormatter(formatter)
# Adding all configs to the logger
logger.addHandler(file_handler)


def get_server_info(response):
    logger.info(
        f">>> Request: url='{response.request.url}', method='{response.request.method}'"
    )
    logger.info(
        f"<<< Response: status_code='{response.status_code}', data='{response.text}'"
    )


def send_test_request(params, url, endpoint, headers=headers):
    """Sends a test request to a url/endpoint."""
    resp = requests.post(url + endpoint, headers=headers, params=params)
    get_server_info(response=resp)
    if resp.status_code == 200:
        recs = resp.json()
    else:
        recs = []
        print(f"status code: {resp.status_code}")

    return recs


class TestRecommendationsService(unittest.TestCase):
    """Class for testing a recommendation service."""

    def test_1_connection(self):
        """Tests connection to all services comprising the application."""
        logger.info('Test 1: "Healthcheck status"')
        response = requests.get(main_app_url + "/healthy")
        get_server_info(response=response)
        response = response.json()
        response = response["status"]

        self.assertEqual(response, "healthy")
        logger.info("Test 1 PASS")

    def test_2_default_users(self, user_id_1: int = 5, user_id_2: int = 1):
        """Tests recs for users without personal recs / online history."""
        # Getting recommendations for user_id=5
        logger.info("-" * 69)
        logger.info('Test 2: "Default users check"')
        params_user_5 = {"user_id": user_id_1, "k": 5}
        response_user_5 = send_test_request(
            params=params_user_5,
            url=main_app_url,
            endpoint="/recommendations",
        )
        # Getting recommendations for user_id=1
        params_user_1 = {"user_id": user_id_2, "k": 5}
        response_user_1 = send_test_request(
            params=params_user_1,
            url=main_app_url,
            endpoint="/recommendations",
        )

        self.assertEqual(response_user_5["recs"], response_user_1["recs"])
        logger.info("Test 2 PASS")

    def test_3_no_empty_recs_1(self, user_id: int = 54791):
        """Tests the non-emptiness of recommendations (user with personal recs)."""
        logger.info("-" * 69)
        logger.info('Test 3: "User with personal recs check"')
        params = {"user_id": user_id, "k": 5}
        response = send_test_request(
            params=params,
            url=main_app_url,
            endpoint="/recommendations",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])
        logger.info("Test 3 PASS")

    def test_4_no_empty_recs_2(self, user_id: int = 1):
        """Tests the non-emptiness of recommendations (user without personal recs)."""
        logger.info("-" * 69)
        logger.info('Test 4: "User without personal recs check"')
        params = {"user_id": user_id, "k": 5}
        response = send_test_request(
            params=params,
            url=main_app_url,
            endpoint="/recommendations",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])
        logger.info("Test 4 PASS")

    def test_5_online_history(
        self,
        user_id: int = 1403769,
        events: list = [869, 22926],
    ):
        """Tests if the online history is added upon request."""
        logger.info("-" * 69)
        logger.info('Test 5: "Online events test"')
        for item_id in events:
            response = send_test_request(
                url=events_url,
                endpoint="/put",
                params={"user_id": user_id, "item_id": item_id},
            )
        online_history = send_test_request(
            params={"user_id": user_id, "k": 10},
            url=events_url,
            endpoint="/get",
        )

        self.assertIsInstance(online_history["events"], list)
        self.assertNotEqual(online_history["events"], [])
        logger.info("Test 5 PASS")

    def test_6_online_recommendations(self, user_id: int = 1403769):
        """Tests if user with online history gets non-empty recommendations."""
        logger.info("-" * 69)
        logger.info('Test 6: "User with online events check"')
        params = {"user_id": user_id}
        response = send_test_request(
            params=params,
            url=main_app_url,
            endpoint="/recommendations_online",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])
        logger.info("Test 6 PASS")

    def test_7_offline_recommendations(self, user_id: int = 1403769):
        """Tests if user with online history gets correct offline recs."""
        logger.info("-" * 69)
        logger.info('Test 7: "Offline recs check"')
        params = {"user_id": user_id, "k": 5}
        response = send_test_request(
            params=params,
            url=main_app_url,
            endpoint="/recommendations_offline",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])
        logger.info("Test 7 PASS")

    def test_8_blended_recommendations(self, user_id: int = 1403769):
        """Tests blended recs for user with offline/online recs."""
        logger.info("-" * 69)
        logger.info('Test 8: "Blended recommendations check"')
        params = {"user_id": user_id, "k": 5}
        response = send_test_request(
            params=params,
            url=main_app_url,
            endpoint="/recommendations",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])
        logger.info("Test 8 PASS")

    def test_9_service_stats(self):
        """Tests if service statistics are changing after requests."""
        # Requesting stats
        logger.info("-" * 69)
        logger.info('Test 9: "Stats check"')
        response = requests.get(main_app_url + "/stats")
        get_server_info(response=response)
        response = response.json()
        # Separating stats
        response_default_stats = response["request_default_count"]
        response_personal_stats = response["request_personal_count"]

        self.assertGreater(response_default_stats, 0)
        self.assertGreater(response_personal_stats, 0)
        logger.info("Test 9 PASS")


if __name__ == "__main__":
    unittest.main()
