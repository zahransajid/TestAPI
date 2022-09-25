from API import testing
from API.route import APIRoute

r = APIRoute("route1")

# Hits the route1 API endpoint with up 100 requests
# at once and plots the curve of average response time
# versus number of requests
testing.stress_expn(r,100)

r2 = APIRoute("route4")
r2.execute()