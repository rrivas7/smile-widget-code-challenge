from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products import services
from products.models import Product, GiftCard
import datetime


@api_view(['GET'])
def get_price(request):
    try:
        product = Product.objects.get(code=request.query_params.get('productCode'))
    except Product.DoesNotExist:
        return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    gift_card = None
    if request.query_params.get('giftCardCode'):
        try:
            gift_card = GiftCard.objects.get(code=request.query_params.get('giftCardCode'))
        except GiftCard.DoesNotExist:
            return Response({'message': 'Gift card not found.'}, status=status.HTTP_404_NOT_FOUND)

    date = datetime.datetime.strptime(request.query_params.get('date'), '%Y-%m-%d').date()

    price = services.calculate_amount_due(product, gift_card, date)
    return Response(price)
