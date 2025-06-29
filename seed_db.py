from crm.models import Customer, Product
Customer.objects.create(name="Test", email="test@example.com")
Product.objects.create(name="Widget", price=19.99, stock=50)