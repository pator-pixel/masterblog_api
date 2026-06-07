from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    if not sort:
        return jsonify(POSTS), 200

    if sort not in ['title', 'content']:
        return jsonify({
            "error": "Invalid sort field. Use 'title' or 'content'."
        }), 400

    if direction not in ['asc', 'desc']:
        return jsonify({
            "error": "Invalid direction. Use 'asc' or 'desc'."
        }), 400

    reverse = direction == 'desc'
    sorted_posts = sorted(
        POSTS,
        key=lambda post: post[sort].lower(),
        reverse=reverse
    )

    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    missing_fields = []

    if "title" not in data:
        missing_fields.append("title")

    if "content" not in data:
        missing_fields.append("content")

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    new_id = max(post["id"] for post in POSTS) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"Post with id {post_id} not found."
    }), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    for post in POSTS:
        if post["id"] == post_id:
            if "title" in data:
                post["title"] = data["title"]

            if "content" in data:
                post["content"] = data["content"]

            return jsonify(post), 200

    return jsonify({
        "error": f"Post with id {post_id} not found."
    }), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title', '').lower()
    content = request.args.get('content', '').lower()

    results = []

    for post in POSTS:
        title_match = title in post['title'].lower() if title else True
        content_match = content in post['content'].lower() if content else True

        if title_match and content_match:
            results.append(post)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)