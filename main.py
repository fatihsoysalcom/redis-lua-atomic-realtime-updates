import redis
import time
import os

# --- Configuration ---
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
UPDATE_KEY = "realtime:data:stock_A" # The Redis key to update
NUM_UPDATES = 5000 # Number of simulated updates to perform

# --- Lua Script for Atomic Update ---
# This script increments a counter and updates a timestamp atomically.
# KEYS[1]: The Redis key to operate on (e.g., "realtime:data:stock_A")
# ARGV[1]: The current timestamp to set
LUA_SCRIPT = """
    local key = KEYS[1]
    local current_time = ARGV[1]

    -- Atomically increment the 'updates_count' field in a hash
    local new_count = redis.call('HINCRBY', key, 'updates_count', 1)

    -- Atomically set the 'last_updated' field in the same hash
    redis.call('HSET', key, 'last_updated', current_time)

    -- Return the new count
    return new_count
"""

def run_example():
    try:
        # Connect to Redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        r.ping()
        print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")

        # Clear previous data for a clean run
        r.delete(UPDATE_KEY)
        print(f"Cleared key: {UPDATE_KEY}")

        # Load the Lua script into Redis. This returns a SHA1 hash of the script.
        # Redis caches the script, so subsequent calls use the hash, saving bandwidth.
        script_sha = r.script_load(LUA_SCRIPT)
        print(f"Lua script loaded. SHA: {script_sha}")

        print(f"\nSimulating {NUM_UPDATES} real-time updates for '{UPDATE_KEY}'...")
        start_time = time.perf_counter()

        for i in range(NUM_UPDATES):
            current_timestamp = int(time.time() * 1000) # Millisecond timestamp
            # Execute the Lua script using its SHA1 hash.
            # KEYS and ARGV are passed as separate lists. The script runs atomically on the Redis server,
            # ensuring consistency even with high concurrency.
            r.evalsha(script_sha, 1, UPDATE_KEY, current_timestamp)

        end_time = time.perf_counter()
        duration = end_time - start_time
        updates_per_second = NUM_UPDATES / duration

        print(f"\nCompleted {NUM_UPDATES} updates in {duration:.4f} seconds.")
        print(f"Achieved {updates_per_second:.2f} updates/second.")

        # Fetch the final state of the key
        final_data = r.hgetall(UPDATE_KEY)
        print(f"\nFinal state of '{UPDATE_KEY}':")
        print(f"  Updates Count: {final_data.get('updates_count', 'N/A')}")
        print(f"  Last Updated (ms): {final_data.get('last_updated', 'N/A')}")

    except redis.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to Redis. Please ensure Redis server is running.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_example()
