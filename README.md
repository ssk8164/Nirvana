# Nirvana Project

## How to run

```bash
# The following command will run our API on localhost
python3 health_plan_calculator.py

# Access browser using the following url, it wont return the necessary json as the static apis api1.com, api2.com, api3.com are fake
http://127.0.0.1:8000/get-health-plan?member_id=1
```

# Testing

```bash
python3 test_coalesce.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

## Code Explanation

- constant.py:
  - This file defines all constants to be used throughout the project
- health_plan_calculator.py:
  - This is our main file. It contains code to create our GET api **/get-health-plan** which takes member_id as a parameter
  - For simplicity a static variable api_url has been defined in this file. It can also be defined in a function to be initialized dynamically.
  - The static variable name coalescing_strategy has also been defined in this file. It maps the insurance field to its respective coalescing strategy(average, median, mode) that we wish to use on that field.
- coalesce.py:
  - This is the heart of the project. It has calculate_data function to coalesce the responses of each insurance field using a strategy of choice. The strategies have been defined in the class Strategy and we are using Higher-order function to select which strategy to apply to which insurance field dynamically.
- test_coalesce.py:
  - All unit tests are defined in this file
