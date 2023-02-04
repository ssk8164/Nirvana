import requests
import statistics
import constant as ct


class Coalesce:

    def calculate_data(member_id, api_url, coalescing_strategy):
        endpoint_data = {}
        data_map = {
            ct.DEDUCTIBLE: [],
            ct.STOP_LOSS: [],
            ct.OOP_MAX: []
        }
        for url in api_url:
            url = "https://" + url + "?member_id=" + str(member_id)
            try:
                response = requests.get(url)
            except requests.exceptions.ConnectionError:
                return None, 502
            if response.status_code == 200:
                result = response.json()
                data_map[ct.DEDUCTIBLE].append(result[ct.DEDUCTIBLE])
                data_map[ct.STOP_LOSS].append(result[ct.STOP_LOSS])
                data_map[ct.OOP_MAX].append(result[ct.OOP_MAX])
            else:
                return None, response.status_code

        for term in coalescing_strategy:
            # call the coalescing strategy function based on the map defined in health_plan_calculator.py
            endpoint_data[term] = Strategy.fun(
                coalescing_strategy[term], data_map[term])

        return endpoint_data, response.status_code


class Strategy:
    # Higher-order function
    def fun(generic, list):
        result = generic(list)
        return result

    def calculate_average(list):
        # Strategy 1: Calculate average:
        total = sum(list)
        return total // len(list)

    def get_most_frequent(list):
        # Strategy 2: Return the most frequent value
        return max(set(list), key=list.count)

    def get_median(list):
        # Strategy 3: Return the median of the list
        return statistics.median(list)
