# REST API URL Template Guidelines

## Base URL Structure

```
https://api.tapay.com/v1/
```

## Role-Based Endpoints

### User Endpoints

```
/v1/users/{userId}/orders          # List user's orders
/v1/users/{userId}/orders/{orderId} # Get specific order
/v1/users/{userId}/orders          # Create new order
/v1/users/{userId}/orders/{orderId}/cancel # Cancel order
/v1/users/{userId}/orders/{orderId}/track  # Track order status
```

### Merchant Admin Endpoints

```
/v1/merchants/{merchantId}/orders          # List all merchant orders
/v1/merchants/{merchantId}/orders/{orderId} # Get specific order
/v1/merchants/{merchantId}/orders/{orderId}/status # Update order status
/v1/merchants/{merchantId}/orders/{orderId}/fulfill # Fulfill order
/v1/merchants/{merchantId}/orders/{orderId}/refund  # Process refund
```

## Resource Naming Conventions

### 1. Use Nouns, Not Verbs

-   ✅ `/users/{userId}/orders`
-   ❌ `/getUserOrders` or `/createUserOrder`

### 2. Use Plural Nouns

-   ✅ `/merchants/{merchantId}/orders`
-   ❌ `/merchant/{merchantId}/order`

### 3. Use Lowercase Letters

-   ✅ `/users/{userId}/order-history`
-   ❌ `/Users/{userId}/OrderHistory`

### 4. Use Hyphens for Multi-word Resources

-   ✅ `/merchants/{merchantId}/order-status`
-   ❌ `/merchants/{merchantId}/orderStatus`

## HTTP Methods and Their Usage

| Method | Description            | User Example                                    | Merchant Example                                        |
| ------ | ---------------------- | ----------------------------------------------- | ------------------------------------------------------- |
| GET    | Retrieve resources     | `GET /users/{userId}/orders`                    | `GET /merchants/{merchantId}/orders`                    |
| POST   | Create new resource    | `POST /users/{userId}/orders`                   | `POST /merchants/{merchantId}/orders/{orderId}/fulfill` |
| PUT    | Update entire resource | `PUT /users/{userId}/orders/{orderId}`          | `PUT /merchants/{merchantId}/orders/{orderId}`          |
| PATCH  | Partial update         | `PATCH /users/{userId}/orders/{orderId}/cancel` | `PATCH /merchants/{merchantId}/orders/{orderId}/status` |
| DELETE | Remove resource        | `DELETE /users/{userId}/orders/{orderId}`       | `DELETE /merchants/{merchantId}/orders/{orderId}`       |

## Resource Relationships

### 1. User Order Management

```
/users/{userId}/orders                    # List all user orders
/users/{userId}/orders/{orderId}          # Get specific order
/users/{userId}/orders/{orderId}/items    # Get order items
/users/{userId}/orders/{orderId}/tracking # Get tracking info
```

### 2. Merchant Order Management

```
/merchants/{merchantId}/orders                    # List all merchant orders
/merchants/{merchantId}/orders/{orderId}          # Get specific order
/merchants/{merchantId}/orders/{orderId}/items    # Get order items
/merchants/{merchantId}/orders/{orderId}/status   # Update order status
/merchants/{merchantId}/orders/{orderId}/refund   # Process refund
```

### 3. Filtering and Search

```
# User filters
/users/{userId}/orders?status=pending
/users/{userId}/orders?date_from=2024-01-01&date_to=2024-03-31

# Merchant filters
/merchants/{merchantId}/orders?status=processing
/merchants/{merchantId}/orders?customer_id=123&status=completed
```

### 4. Pagination

```
/users/{userId}/orders?page=1&limit=10
/merchants/{merchantId}/orders?page=1&limit=20
```

## Examples

### User Order Operations

```
GET    /v1/users/{userId}/orders                    # List orders
POST   /v1/users/{userId}/orders                    # Create order
GET    /v1/users/{userId}/orders/{orderId}          # Get order details
PATCH  /v1/users/{userId}/orders/{orderId}/cancel   # Cancel order
GET    /v1/users/{userId}/orders/{orderId}/tracking # Track order
```

### Merchant Order Operations

```
GET    /v1/merchants/{merchantId}/orders                    # List all orders
GET    /v1/merchants/{merchantId}/orders/{orderId}          # Get order details
PATCH  /v1/merchants/{merchantId}/orders/{orderId}/status   # Update status
POST   /v1/merchants/{merchantId}/orders/{orderId}/fulfill  # Fulfill order
POST   /v1/merchants/{merchantId}/orders/{orderId}/refund   # Process refund
```

## Best Practices

1. **Role Separation**: Clearly separate user and merchant endpoints
2. **Consistency**: Maintain consistent URL structure within each role
3. **Security**: Implement proper authentication and authorization
4. **Documentation**: Document all endpoints with their required permissions
5. **Error Handling**: Use appropriate HTTP status codes
6. **Versioning**: Include version in URL: `/v1/...`
7. **Query Parameters**: Use consistent parameter names across roles
8. **Response Format**: Use consistent response structure

## Response Format

All responses should follow this structure:

```json
{
    "status": "success",
    "data": {
        // Response data
    },
    "meta": {
        // Pagination, sorting, filtering info
    }
}
```

## Error Response Format

```json
{
    "status": "error",
    "message": "Error description",
    "code": "ERROR_CODE",
    "errors": [
        {
            "field": "field_name",
            "message": "Error message"
        }
    ]
}
```
