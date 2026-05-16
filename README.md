# Redis Lua Atomic Realtime Updates

This example demonstrates how to achieve high-performance, atomic real-time updates using Redis and Lua scripting. A Python script connects to Redis, loads a Lua script, and then executes it thousands of times. The Lua script atomically increments a counter and updates a timestamp for a given key, showcasing how Redis's single-threaded nature combined with Lua's atomic execution ensures data consistency and high throughput for real-time API scenarios.

## Language

`python`

## How to Run

1. Ensure a Redis server is running (e.g., `redis-server`).
2. Install the Redis Python client: `pip install redis`
3. Run the Python script: `python main.py`

## Original Article

This example accompanies the Turkish article: [Gerçek Zamanlı API'ler Sandığınızdan Daha Basit: Redis, Lua ve Saniyede 4000 Güncelleme](https://fatihsoysal.com/blog/gercek-zamanli-apiler-sandiginizdan-daha-basit-redis-lua-ve-saniyede-4000-guncelleme/).

## License

MIT — see [LICENSE](LICENSE).
