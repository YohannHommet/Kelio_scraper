#!/usr/bin/env python3
"""
Error handler module to manage and log errors.
"""

def handle_error(error):
    """Handle an error by logging it appropriately. Extend this function based on error types."""
    # For now, simply print the error, but this can be expanded to log to a file or external service.
    print(f"Error occurred: {error}")


if __name__ == "__main__":
    try:
        # Example simulation of error
        raise ValueError("An example error")
    except Exception as e:
        handle_error(e)
