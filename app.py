from chalice import Chalice, Response
from chalicelib.authorizer import Autenticator
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


@app.route('/payment', methods=['POST'])
def payment():
    request = app.current_request
    body = request.json_body
    transport_type = body.get('transport_type')
    price = body.get('price')
    payment_method = body.get('payment_method')
    if not transport_type or not price or not payment_method:
        return Response(body={'error': 'Missing transport_type, price or payment_method'},
                        status_code=400)
    
    delay = random.randint(1, 5)
    time.sleep(delay)
    
    if payment_method == 'credit_card':
        card_number = body.get('card_number')
        card_expiry_date = body.get('card_expiry_date')
        card_cvv = body.get('card_cvv')
        if not card_number or not card_expiry_date or not card_cvv:
            return Response(body={'error': 'Missing credit card information'},
                            status_code=400)
        if len(card_number) != 16 or len(card_cvv) != 3:
            return Response(body={'error': 'Invalid credit card information'},
                            status_code=400)
        return {'status': 'success'}
    
    elif payment_method == 'debit_card':
        card_number = body.get('card_number')
        card_expiry_date = body.get('card_expiry_date')
        card_cvv = body.get('card_cvv')
        if not card_number or not card_expiry_date or not card_cvv:
            return Response(body={'error': 'Missing debit card information'},
                            status_code=400)
        if len(card_number) != 16 or len(card_cvv) != 3:
            return Response(body={'error': 'Invalid debit card information'},
                            status_code=400)
        return {'status': 'success'}
    
    elif payment_method == 'cash':
        amount_received = body.get('amount_received')
        if not amount_received:
            return Response(body={'error': 'Missing amount_received'},
                            status_code=400)
        if amount_received < price:
            return Response(body={'error': 'Insufficient amount received'},
                            status_code=400)
        change = amount_received - price
        return {'status': 'success', 'change': change}
    
    else:
        return Response(body={'error': 'Invalid payment_method'},
                        status_code=400)
