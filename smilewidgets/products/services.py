def calculate_amount_due(product, gift_card, date):
    amount_due = product.price_on_date(date)
    if gift_card:
        amount_due -= gift_card.amount

    return max([0, amount_due])
