# FROM python:3.12-slim AS builder

# # Set working directory
# WORKDIR /app

# # Copy application code
# COPY . .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# RUN pytest -v

# FROM python:3.12-slim

# COPY --from=builder /app /app
# # Expose port
# EXPOSE 5000

# # Run the application
# CMD ["python", "src/api.py"]


################
# Base Stage - Install dependencies & Run tests
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run tests and FAIL the build if any test fails
RUN ls -ls && PYTHONPATH=.:$PYTHONPATH pytest -v && echo "Tests Passed" || (echo "Tests Failed" && exit 1)

# Production Stage - Only builds if tests pass
FROM python:3.11-slim AS final

WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /app /app

RUN useradd -m myuser
USER myuser
# Expose application port
EXPOSE 5000

# Start the application
CMD ["python", "api.py"]

