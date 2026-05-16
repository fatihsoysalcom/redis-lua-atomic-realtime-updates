# redis-lua-atomic-realtime-updates
This example demonstrates how to achieve high-performance, atomic real-time updates using Redis and Lua scripting. A Python script connects to Redis, loads a Lua script, and then executes it thousands of times. The Lua script atomically increments a counter and updates a timestamp for a given key, showcasing how Redis's single-threaded nature combi
