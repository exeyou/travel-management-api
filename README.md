This is a simple restful api built with django rest framework to help track travel projects. You can add up to 10 places to any given project, add personal notes, and mark them as visited.

Includes:

Pagination, filtering, and search for the endpoints. Basic authentication. Caching. Docker support for easier deployment.

Stack: 

Backend: Django & Django REST Framework 
Database: SQLite External 
API: Art Institute of Chicago 
Infrastructure: Docker

Don't forget to install requirements, migrate and create super user. After running server, use 'docker-compose up --build'. Then go to /api/projects