from flask import Flask, render_template, request
from flask_caching import Cache
import redis
import asyncio

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
r = redis.Redis(host='localhost', port=6379, db=0)

# 블로그 포스트 데이터
posts = [
    {'id': 1, 'title': '첫 번째 포스트', 'content': '안녕하세요, 첫 번째 포스트입니다.'},
    {'id': 2, 'title': '두 번째 포스트', 'content': '안녕하세요, 두 번째 포스트입니다.'},
    {'id': 3, 'title': '세 번째 포스트', 'content': '안녕하세요, 세 번째 포스트입니다.'},
]

# 비동기 처리를 위한 함수
async def get_posts_async():
    await asyncio.sleep(1)  # 가상의 비동기 작업
    return posts

@app.route('/')
@cache.cached(timeout=60)  # 캐시 설정
def home():
    return render_template('index.html', posts=posts)

@app.route('/posts')
def get_all_posts():
    # 캐시된 데이터 조회
    cached_posts = r.get('cached_posts')
    if cached_posts:
        return cached_posts.decode()

    # 비동기로 포스트 데이터 조회
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_posts_async())
    loop.run_until_complete(task)

    # 데이터 캐싱
    r.setex('cached_posts', 60, str(task.result()))

    return str(task.result())

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return '포스트를 찾을 수 없습니다.'

if __name__ == '__main__':
    app.run(debug=True)
