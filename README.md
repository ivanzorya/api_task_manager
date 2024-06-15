# api_task_manager
Technical Description of the TaskManager Project

### User Roles

- **Anonymous** — can register.
- **Authenticated user (user)** — can create, read, and update their tasks. Can view the task change history.

### User Registration Algorithm
1. The user sends a POST request with the parameters `username` and `password` to `/api/v1/auth/`.
2. The user sends a POST request with the parameters `username` and `password` to `/api/v1/token/`, and in response to the request, they receive a JWT token (`access`).

These operations are performed once during user registration. As a result, the user receives a token and can work with the API, sending this token with each request.

### API Resources

- **AUTH Resource**: registration.
- **TOKEN Resource**: authentication.
- **TASKS Resource**: tasks and change history.

Each resource is described in the documentation at `/redoc/`: endpoints, allowed request types, access rights, and additional parameters, if necessary.

### Related Data and Cascading Deletion
- When a task is deleted, its change history is deleted.
- When a user is deleted, their tasks are deleted.
