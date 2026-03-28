from flask import Flask, request, jsonify
import json


app = Flask(__name__)

def read_customer_file():
	with open('data/customers.json') as customers_file:
		file_contents= customers_file.read()
	return json.loads(file_contents)


# customers.json stays loaded in memory for 
customer_array = read_customer_file()

customer_index = {customer['customer_id']: customer for customer in customer_array}
	
def parse_positive_int(value, default = None):
	if value is None:
		return default
	try:
		int_value = int(value)
		if int_value < 1:
			raise ValueError()
		return int_value
	except (TypeError, ValueError):
		return default

@app.get("/api/health")
def health_check():
	"""
    GET /health
    Returns:
      200: Server Running (simple health check)
	"""
	return {
		"status": "Server running"
	}, 200

# Query params:
@app.get("/api/customers")
def paginated_customers():
	"""
    GET /api/customers
    Query parameters:
      - page (int, optional): Page number, default 1. Must be >= 1.
      - limit (int, optional): Customers per page, default 5. Must be >= 1.
    Response:
      200: JSON list of customers with pagination metadata.
	"""
	page_no = parse_positive_int(request.args.get('page'), 1)
	limit = parse_positive_int(request.args.get('limit'), 5)
	
	start_index = (page_no-1)*limit
	paginated_data = customer_array[start_index:start_index+limit]
	total = len(customer_array)
	return {
		"data": paginated_data,
		"total": total,
		"page": page_no,
		"limit": limit
	}, 200


@app.get("/api/customers/<customer_id>")
def single_customer(customer_id):
	"""
    GET /api/customers/<customer_id>
    Path parameter:
      - customer_id (str, required): Customer ID
    Response:
      200: JSON object with customer data.
	  404: Customer not found.
	"""
	if customer_id in customer_index:
		return customer_index[customer_id], 200
	else:
		return {
			"error": "resource_not_found",
			"message": "The requested customer does not exist",
		}, 404

app.run(host='0.0.0.0', port=5000, debug=False)