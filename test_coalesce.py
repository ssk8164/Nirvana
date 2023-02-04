import unittest
from unittest import mock
from coalesce import Coalesce, Strategy
import constant as ct

mocked_coalescing_strategy1 = {
    ct.DEDUCTIBLE: Strategy.calculate_average,
    ct.STOP_LOSS: Strategy.calculate_average,
    ct.OOP_MAX: Strategy.calculate_average
}

mocked_coalescing_strategy2 = {
    ct.DEDUCTIBLE: Strategy.calculate_average,
    ct.STOP_LOSS: Strategy.get_most_frequent,
    ct.OOP_MAX: Strategy.get_median
}

# Using mocked_requests_get function to replace requests.get being called in Coalesce.calculate_data()


def mocked_requests_get(url):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if url == 'https://api1.com?member_id=1':
        return MockResponse({"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}, 200)
    elif url == 'https://api2.com?member_id=1':
        return MockResponse({"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}, 200)
    elif url == 'https://api3.com?member_id=1':
        return MockResponse({"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}, 200)
    return MockResponse(None, 404)


# Unit tests

class CalcualteDataTestCase(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):
        # test1 : Both member id and url are valid, use mocked_coalescing_strategy1
        result, response_code = Coalesce.calculate_data(
            1, ["api1.com", "api2.com", "api3.com"], mocked_coalescing_strategy1)
        self.assertEqual(
            result, {"deductible": 1066, "stop_loss": 11000, "oop_max": 5666})
        self.assertEqual(response_code, 200)

        # test2 : Both member id and url are valid, use mocked_coalescing_strategy2
        result, response_code = Coalesce.calculate_data(
            1, ["api1.com", "api2.com", "api3.com"], mocked_coalescing_strategy2)
        self.assertEqual(
            result, {"deductible": 1066, "stop_loss": 10000, "oop_max": 6000})
        self.assertEqual(response_code, 200)

        # test3 :  member id is valid and url is invalid
        result, response_code = Coalesce.calculate_data(
            1, "fake.com", mocked_coalescing_strategy1)
        self.assertIsNone(result)
        self.assertEqual(response_code, 404)

        # test4 :  member id is invalid and url is valid
        result, response_code = Coalesce.calculate_data(
            -2, ["api1.com", "api2.com", "api3.com"], mocked_coalescing_strategy1)
        self.assertIsNone(result)
        self.assertEqual(response_code, 404)

        # test5 :  Both member id and url are invalid
        result, response_code = Coalesce.calculate_data(
            -1, "fake.com", mocked_coalescing_strategy1)
        self.assertIsNone(result)
        self.assertEqual(response_code, 404)


if __name__ == '__main__':
    unittest.main()
