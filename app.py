from chalice import Chalice, Response
from chalicelib.authorizer import Athenticator
from geopy.distance import geodesic

app = Chalice(app_name='safe-transit-api')

@app.route('/transport', methods=['POST'], authorizer=Athenticator())
def transport():
    request = app.current_request
    body = request.json_body
    initial_location = body.get('initial_location')
    end_location = body.get('end_location')
    if not initial_location or not end_location:
        return Response(body={'error': 'Missing location1 or location2'},
                        status_code=400)
    distance = geodesic(initial_location, end_location).km
    if distance < 2:
        transport_type = 'a pé'
        price = 0
    elif distance < 10:
        transport_type = 'ônibus'
        price = 4.5
    elif distance < 20:
        transport_type = 'metrô'
        price = 5.5
    else:
        transport_type = 'táxi'
        price = distance * 2.5
    return {'transport_type': transport_type, 'price': price}
