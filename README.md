# Cloud Metadata API

A RESTful API service for managing cloud resource metadata and lifecycle operations. This project demonstrates scalable API design, database management, and cloud infrastructure concepts.

## Features

- **RESTful API** with full CRUD operations for cloud resources
- **Metadata Management** for tracking cloud infrastructure
- **Lifecycle Tracking** with status monitoring (provisioning, active, terminated, etc.)
- **Region-based Querying** to filter resources by geographic location
- **Type-based Filtering** to organize resources by category
- **Statistics Dashboard** for resource summaries
- **Automatic API Documentation** with Swagger/OpenAPI
- **SQLite Database** with SQLAlchemy ORM

## Tech Stack

- **FastAPI** - Modern, high-performance web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server for production
- **SQLite** - Lightweight database (easily upgradeable to PostgreSQL)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions (Windows)

1. **Create project folder and files**
   - Create a folder called `cloud-metadata-api`
   - Inside it, create folders: `app` and `tests`
   - Copy all the files I provided into the correct locations

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
```bash
# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the API

### Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### Access the interactive API documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Health check endpoint

### Resource Management
- `POST /resources/` - Create a new resource
- `GET /resources/` - List all resources (with pagination)
- `GET /resources/{resource_id}` - Get a specific resource
- `PUT /resources/{resource_id}` - Update a resource
- `DELETE /resources/{resource_id}` - Delete a resource

### Query Endpoints
- `GET /resources/region/{region}` - Get resources by region
- `GET /resources/type/{resource_type}` - Get resources by type
- `GET /resources/status/{status}` - Get resources by status

### Statistics
- `GET /stats/summary` - Get resource summary statistics

## Example Usage

### Create a Resource

```bash
curl -X POST "http://localhost:8000/resources/" \
  -H "Content-Type: application/json" \
  -d '{
    "resource_id": "vm-eastus-001",
    "resource_type": "virtual_machine",
    "region": "eastus",
    "status": "active",
    "tags": {
      "size": "Standard_D2s_v3",
      "os": "Ubuntu 22.04",
      "owner": "engineering-team"
    }
  }'
```

### List All Resources

```bash
curl http://localhost:8000/resources/
```

### Get Resources by Region

```bash
curl http://localhost:8000/resources/region/eastus
```

### Get Statistics

```bash
curl http://localhost:8000/stats/summary
```

## Database Schema

### Resource Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| resource_id | String | Unique identifier for the resource |
| resource_type | String | Type of resource (e.g., vm, storage, database) |
| region | String | Geographic region |
| status | String | Lifecycle status (provisioning, active, terminated) |
| tags | JSON | Additional key-value metadata |
| created_at | DateTime | Timestamp when resource was created |
| updated_at | DateTime | Timestamp when resource was last updated |

## Push to GitHub

### First Time Setup:

1. **Create a new repository on GitHub:**
   - Go to https://github.com
   - Click the "+" icon > "New repository"
   - Name it: `cloud-metadata-api`
   - Keep it public
   - **Don't** initialize with README
   - Click "Create repository"

2. **In your terminal:**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Cloud Metadata API"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/A-Bak-tech/cloud-metadata-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

3. **Refresh your GitHub repository page** - your code is now live!

## Future Enhancements

- [ ] Add authentication and authorization
- [ ] Implement rate limiting
- [ ] Add caching layer (Redis)
- [ ] Migrate to PostgreSQL for production
- [ ] Add Docker containerization
- [ ] Implement health monitoring and alerts
- [ ] Add GraphQL endpoint
- [ ] Deploy to cloud platform (Azure/AWS)

## License

This project is open source and available under the MIT License.

## Contact

Alyssa Baker - [LinkedIn](https://linkedin.com/in/alyssa-baker-541b272b1)

Project Link: https://github.com/A-Bak-tech/cloud-metadata-api