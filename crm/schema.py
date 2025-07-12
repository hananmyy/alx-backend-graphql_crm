import graphene
import re
from graphene_django import DjangoObjectType
from django.utils.timezone import now
from .models import Customer, Product, Order
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from .filters import CustomerFilter, ProductFilter, OrderFilter

# GraphQL Types

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node,)

# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(default_value=0)

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

class BulkCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

# Utility

def is_valid_phone(phone):
    return re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', phone)

# Mutations 

class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        input = CustomerInput(required=True)

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")

        if input.phone and not is_valid_phone(input.phone):
            raise Exception("Invalid phone number format")

        customer = Customer.objects.create(**input)
        return CreateCustomer(customer=customer, message="Customer created successfully!")

class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(BulkCustomerInput, required=True)

    def mutate(self, info, input):
        created = []
        errors = []

        for i, customer_input in enumerate(input):
            if Customer.objects.filter(email=customer_input.email).exists():
                errors.append(f"[{i}] Email {customer_input.email} already exists")
                continue
            if customer_input.phone and not is_valid_phone(customer_input.phone):
                errors.append(f"[{i}] Invalid phone format: {customer_input.phone}")
                continue
            try:
                customer = Customer.objects.create(
                    name=customer_input.name,
                    email=customer_input.email,
                    phone=customer_input.phone
                )
                created.append(customer)
            except Exception as e:
                errors.append(f"[{i}] {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        input = ProductInput(required=True)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be a positive number")
        if input.stock < 0:
            raise Exception("Stock must be non-negative")

        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock
        )
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        input = OrderInput(required=True)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer not found")

        if not input.product_ids:
            raise Exception("At least one product ID is required")

        products = Product.objects.filter(id__in=input.product_ids)
        if products.count() != len(input.product_ids):
            raise Exception("One or more product IDs are invalid")

        total = sum(product.price for product in products)
        order_date = input.order_date or now()
        order = Order.objects.create(
            customer=customer,
            order_date=order_date,
            total_amount=total
        )
        order.products.set(products)
        return CreateOrder(order=order)

# Query and Mutation 
class Query(graphene.ObjectType):
    pass

"""class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()"""


class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
    all_products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
    all_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)



import graphene
from crm.models import Product

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed for this mutation

    updated = graphene.List(graphene.String)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated.append(f"{product.name} (new stock: {product.stock})")

        return UpdateLowStockProducts(updated=updated, message="Products restocked.")