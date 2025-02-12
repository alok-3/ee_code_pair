## Reviewer Instructions
If you are reviewing this submission, then you can do so in two ways

* Look at the changes in [this pull request](https://github.com/equalexperts-assignments/equal-experts-academic-friendly-gorgeous-memory-c5d1e69ffc31/pull/2)
* Browse the code on Github
    

# GitHub Gists API Server

A simple Python-based API server that interacts with the GitHub API to fetch a user's publicly available gists. The solution is tested using `pytest` and packaged into a Docker container for easy deployment.

---

## Features

- **Fetch Gists**: Retrieve public gists for any GitHub user via `/USER`.
- **Pagination**: Support for paginated results with `page` and `per_page` query parameters.
- **Caching**: In-memory caching to optimize repeated requests for the same data.
- **Enhanced Error Handling**: Provides detailed error responses for invalid users and rate limit issues.
- **Automated Tests**: Validate the API's functionality using `pytest`.
- **Dockerized Deployment**: Package the API into a Docker container listening on port `8080`.

---

## Prerequisites

- **Python 3.8+**
- **Docker**
- **GitHub API Token (optional)**: Required only for higher API rate limits.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2: Create and Activate a Virtual Environment

```bash
python -m venv venv
```

- **Activate Virtual Environment:**
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
  - On Windows:
    ```bash
    venv\Scripts\activate
    ```

### 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### 4: Run the Application

```bash
python src/api.py
```

````

Access the API at: `http://localhost:8080/<USER>`

Example with pagination:

```bash
http://localhost:8080/octocat?page=2&per_page=5
````

---

## Testing

### Run Tests

```bash
pytest
```

### Run Tests in case you get `ModuleNotFoundError`

```bash
PYTHONPATH=.:$PYTHONPATH pytest
```

---

## Docker Deployment

### 1. Build Docker Image

```bash
docker build -t github-gists-api .
```

### 2. Run Docker Container

```bash
docker run -d -p 8080:8080 github-gists-api
```

Access the API at: `http://localhost:8080/<USER>`

---

## Endpoints

### GET `/USER`

**Description:** Fetches the public gists of the specified GitHub user.

**Query Parameters:**

- `page`: Page number (default: 1)
- `per_page`: Number of gists per page (default: 10)

**Example Request:**

```bash
curl http://localhost:8080/octocat?page=2&per_page=5
```

**Example Response:**

```json
[
  {
    "id": "1",
    "description": "Test Gist",
    "url": "https://gist.github.com/1"
  }
]
```

---

## File Structure

```
.
├── src/
│   ├──api.py              # Main application code
├── tests/
│   ├── test_api.py        # Automated tests
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## Notes

- **GitHub Rate Limits:** Unauthenticated requests are limited. Use a personal access token for higher limits.
- **Optional Features:** Pagination and caching added to optimize performance.
- To stop the virtual environment, run:
  ```bash
  deactivate
  ```
