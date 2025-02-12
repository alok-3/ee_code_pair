from flask import Flask, jsonify, request
import requests
from functools import lru_cache

api = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/users/{}/gists"
CACHE_SIZE = 128  # Cache size for in-memory caching

@lru_cache(maxsize=CACHE_SIZE)
def fetch_gists_from_github(username, page, per_page):
    """Fetch the public gists of a given GitHub user with pagination."""
    url = f"{GITHUB_API_URL.format(username)}?page={page}&per_page={per_page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@api.route('/<username>', methods=['GET'])
def get_gists(username):
    """Fetch and paginate the public gists of a given GitHub user."""
    try:
        # Get pagination parameters from the request
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Fetch gists with caching
        gists_data = fetch_gists_from_github(username, page, per_page)
        gists = [
            {
                "id": gist.get("id"),
                "description": gist.get("description"),
                "url": gist.get("html_url")
            }
            for gist in gists_data
        ]
        return jsonify(gists), 200
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": "User not found"}), 404
        if e.response.status_code == 403:
            return jsonify({"error": "Rate limit exceeded"}), 403
        return jsonify({"error": "Failed to fetch gists", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000)
