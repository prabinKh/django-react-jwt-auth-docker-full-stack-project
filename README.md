# Dockerized Application

This project contains a Dockerized full-stack application with React frontend, Django backend, and PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Architecture

The application consists of three main services:

1. **Frontend** (React with Nginx) - Serves the web interface on port 3000
2. **Backend** (Django) - Provides the API on port 8000
3. **Database** (PostgreSQL) - Stores data on port 5432

### Nginx Configuration

The frontend uses Nginx as a reverse proxy to serve the React application and proxy API requests to the backend:
- All requests to `/` serve the React application
- All requests to `/api/` are proxied to the backend service

## Scripts

### Start the application
```bash
./start.sh
```

This will build and start all services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Database: localhost:5432 (PostgreSQL)

### Stop the application
```bash
./stop.sh
```

This will stop all running services.

### Clean up Docker resources
```bash
./cleanup.sh
```

This will remove all containers, images, and volumes related to this project.

### Remove All Docker Resources

To remove all Docker containers, images, volumes, and networks (not just project-related):

```bash
# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Remove all networks
docker network prune -f

# Remove build cache
docker builder prune -a -f
```

**Warning**: These commands will remove Docker resources for all projects, not just this one. Use with caution.

## Manual Commands

### Docker Compose Commands

Start services:
```bash
docker-compose up --build
```

Start services in detached mode:
```bash
docker-compose up --build -d
```

Stop services:
```bash
docker-compose down
```

Stop services and remove volumes:
```bash
docker-compose down -v
```

### Docker Commands

List running containers:
```bash
docker-compose ps
```

View logs for all services:
```bash
docker-compose logs
```

View logs for a specific service:
```bash
docker-compose logs [service-name]
```

Execute a command in a running container:
```bash
docker-compose exec [service-name] [command]
```

For example, to access the Django shell:
```bash
docker-compose exec backend python manage.py shell
```

### Port Information

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432 (PostgreSQL)

### Superuser Credentials

A superuser is automatically created during the backend startup:
- Username: admin
- Password: admin
- Email: admin@gmail.com

You can access the Django admin interface at: http://localhost:8000/admin/

## Development

### Making Changes

1. Frontend changes are automatically reflected when running in development mode
2. Backend changes require rebuilding the Docker image:
   ```bash
   docker-compose up --build
   ```

### Database Migrations

Django migrations are automatically applied when the backend container starts.

To create new migrations:
```bash
docker-compose exec backend python manage.py makemigrations
```

To apply migrations manually:
```bash
docker-compose exec backend python manage.py migrate
```