# ALX Backend GraphQL CRM

This is a Django-based CRM backend powered by **GraphQL**, designed to handle customer, product, and order data with robust filtering, validation, and bulk operations.

## Features

- GraphQL endpoint with `graphiql` UI at `/graphql`
- Mutations to:
  - Create single and bulk customers with validation
  - Create products with stock and price constraints
  - Create orders with nested customer and product references
- Filters for:
  - Customers (name, email, phone pattern, date range)
  - Products (name, price range, stock)
  - Orders (amount range, customer/product name, specific product ID)
- Custom error handling and friendly messages for invalid input

## Tech Stack

- Django & Graphene-Django
- Django Filters (`django-filter`)
- SQLite (default) or other Django-supported DB engines

## Setup Instructions

```bash
git clone https://github.com/<your-username>/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
