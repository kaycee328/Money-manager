transactions = [{"title": "IPNX (January Sub)", "amount": 19650.0, "expense_type": "Negative"}, {"title": "Cash withdrawal", "amount": 30000.0, "expense_type": "Negative"}, {"title": "Carpet washing", "amount": 6000.0, "expense_type": "Negative"}, {"title": "Somtoo's acceptance fee(remitta)", "amount": 30000.0, "expense_type": "Negative"}, {"title": "Refund of cash", "amount": 30000.0, "expense_type": "Positive"}, {"title": "Uncle Mike", "amount": 900000.0, "expense_type": "Positive"}, {"title": "Mr. Austin", "amount": 500000.0, "expense_type": "Positive"}, {"title": "IPNX february", "amount": 19650.0, "expense_type": "Negative"}, {"title": "New Fridge", "amount": 501000.0, "expense_type": "Negative"}, {"title": "Transport new fridge", "amount": 10000.0, "expense_type": "Negative"}]

with open('transactions.txt', 'w') as f:    
    for i in transactions:
        f.write(str(i)+'\n')

