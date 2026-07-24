"""Health check endpoints for Election Intelligence Platform."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import time
from datetime import datetime
import psutil
import os


async def health_check(request = None):
    """Comprehensive health check for the application."""
    try:
        # Basic application info
        health_info = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "election-intelligence-platform",
            "version": "0.1.0",
        }

        # System resource information
        try:
            health_info["system"] = {
                "hostname": os.uname()[1],
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_usage": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent
                },
                "disk_usage": psutil.disk_usage('/'),
            }
        except Exception as e:
            health_info["system_error"] = str(e)

        # Database connectivity check
        try:
            from app.core.config import get_db_session
            db_session = get_db_session()
            db_session.execute("SELECT 1")
            health_info["database"] = {
                "status": "connected",
                "latency_ms": time.time() * 1000
            }
        except Exception as e:
            health_info["database"] = {
                "status": "error",
                "error": str(e)
            }
            health_info["status"] = "degraded"

        # Cache service check
        try:
            from app.core.cache import cache_client
            test_key = "health_check_test"
            test_value = {"timestamp": datetime.now().isoformat()}
            await cache_client.setex(test_key, 60, test_value)
            retrieved = await cache_client.get(test_key)
            health_info["cache"] = {
                "status": "operational" if retrieved else "error",
                "test_passed": bool(retrieved)
            }
            await cache_client.delete(test_key)
        except Exception as e:
            health_info["cache"] = {
                "status": "error",
                "error": str(e)
            }
            health_info["status"] = "degraded"

        # File system access check
        try:
            test_file = "/tmp/health_check_test.txt"
            with open(test_file, "w") as f:
                f.write("health check")
            os.remove(test_file)
            health_info["filesystem"] = {"status": "accessible"}
        except Exception as e:
            health_info["filesystem"] = {"status": "error", "error": str(e)}
            health_info["status"] = "degraded"

        return JSONResponse(health_info, status_code=200)

    except Exception as e:
        # Log the error for debugging
        print(f"Health check error: {e}")

        return JSONResponse(
            {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "service": "election-intelligence-platform"
            },
            status_code=503
        )