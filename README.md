# n8n Integration Module

## Overview

This module provides a backend integration with the n8n automation tool, exposing its REST API through a structured and maintainable interface. It acts as a proxy, forwarding requests to a live n8n instance while leveraging FastAPI for routing, Pydantic for schema validation, and an asynchronous HTTP client for non-blocking API calls.

## Features

The integration currently supports the following n8n API resources:

- **Workflows**: List, retrieve, create, update, and delete workflows.
- **Executions**: List, retrieve, and delete workflow executions.
- **Credentials**: Full CRUD functionality for credentials.
- **Users**: List and retrieve users.
- **Tags**: Full CRUD functionality for tags.
- **Audit**: Generate security and risk audit reports.
- **Source Control**: Pull changes from a remote Git repository.
- **Variables**: Full CRUD functionality for instance variables.
- **Projects**: List all projects.
- **Webhooks**: Manage test and production webhooks (Note: webhook management is partially implemented).

## Configuration

To enable the integration, you must configure the following environment variables in your `.env` file:

- `N8N_BASE_URL`: The base URL of your n8n instance (e.g., `https://n8n.example.com/api/v1`).
- `N8N_API_KEY`: Your n8n API key for authentication.

```sh
N8N_BASE_URL=https://your-n8n-instance.com/api/v1
N8N_API_KEY=your-api-key-here
```

## Architecture

The module is organized into four main sub-packages:

- `api/`: Contains the FastAPI routers that define the API endpoints. Each resource has its own router file (e.g., `workflows.py`, `users.py`).
- `schemas/`: Contains the Pydantic models that define the data structures for API requests and responses. These models ensure data validation and serialization.
- `services/`: Contains the business logic for interacting with the n8n API. Each service class encapsulates the HTTP calls for a specific resource.
- `client.py`: Provides a shared, asynchronous HTTP client (`N8nClient`) for making requests to the n8n API. It handles authentication and base URL configuration.

This layered architecture promotes separation of concerns, making the integration easier to test, maintain, and extend.

## Usage

Once the application is running, the n8n API endpoints are available under the `/api/n8n/` prefix. For example, to retrieve a list of all workflows, you can make a GET request to:

```
GET /api/n8n/workflows/
```

Refer to the OpenAPI documentation at `/docs` for a complete and interactive list of all available endpoints, their parameters, and response models.

## Testing

A comprehensive test suite is included, covering all services and API endpoints to ensure correctness and reliability. The tests can be found in the `_tests` directory and run using `pytest`.
