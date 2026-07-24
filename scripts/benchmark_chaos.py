import asyncio
import time
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.production.chaos import ChaosRunner, FaultInjector

async def measure_event_loop_lag():
    """Runs a background task that measures event loop responsiveness."""
    lags = []
    start_time = time.time()
    while time.time() - start_time < 1.0: # Run for 1 second
        loop_start = time.time()
        await asyncio.sleep(0.01) # Yield control
        loop_end = time.time()
        lags.append(loop_end - loop_start - 0.01)

    if lags:
        max_lag = max(lags)
        avg_lag = sum(lags) / len(lags)
        print(f"Event Loop Lag - Max: {max_lag:.4f}s, Avg: {avg_lag:.4f}s")
    return lags

async def run_benchmark():
    num_requests = 10
    print(f"Running benchmark with {num_requests} concurrent chaos experiments...")

    # We will modify the FaultInjector's default latency to be higher for benchmark
    # to better demonstrate the blocking behavior.
    # The default is 0.01s, let's change it to 0.1s for the benchmark purposes.
    # Actually run_chaos_experiment hardcodes latency_delay_sec=0.01
    # We will test 100 requests to make it 1 second of blocking.
    num_requests = 100
    print(f"Running benchmark with {num_requests} concurrent chaos experiments (0.01s latency each)...")

    start_time = time.time()

    # Check if run_chaos_experiment is async
    is_async = asyncio.iscoroutinefunction(ChaosRunner.run_chaos_experiment)

    # Start the background task to measure loop lag
    lag_task = asyncio.create_task(measure_event_loop_lag())

    if is_async:
        print("Using async run_chaos_experiment")
        tasks = [ChaosRunner.run_chaos_experiment("db_latency_experiment") for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
    else:
        print("Using sync run_chaos_experiment")
        async def run_one():
            # In a real app running in async context without threadpool, it runs like this
            return ChaosRunner.run_chaos_experiment("db_latency_experiment")

        tasks = [run_one() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total execution time: {total_time:.4f} seconds")
    print(f"Average time per request: {total_time / num_requests:.4f} seconds")

    # Wait for lag task to finish if it hasn't
    await asyncio.sleep(1.0)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
