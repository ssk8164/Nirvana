from flask import Flask, jsonify, request, abort
from coalesce import Coalesce, Strategy
import constant as ct

app = Flask(__name__)

# The variable api_url is currently static but we can introduce a function here
# that gets all the urls dynamically.
api_url = ["api1.com", "api2.com", "api3.com"]

# The variable coalescing_strategy is static, although if we need to change a
# strategy for any field we just need to update the value of this variable with
# the new function name
coalescing_strategy = {
    ct.DEDUCTIBLE: Strategy.calculate_average,
    ct.STOP_LOSS: Strategy.get_most_frequent,
    ct.OOP_MAX: Strategy.get_median
}


@app.route('/get-health-plan', methods=['GET'])
def get_health_plan():

    member_id = request.args.get('member_id')

    if member_id == None or member_id == "":
        abort(400)

    else:
        endpoint_data, status_code = Coalesce.calculate_data(
            member_id, api_url, coalescing_strategy)
        if status_code != 200:
            abort(status_code)
        return jsonify(endpoint_data)


if __name__ == '__main__':

    app.run(debug=True, port=8000)
