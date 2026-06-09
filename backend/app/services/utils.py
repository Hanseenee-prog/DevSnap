from datetime import datetime, timezone

def check_elapsed_time(result: dict) -> int:
    # Get the current time and the time the OTP was created

    # I'm using updatedat so that I can be able to update sth when the user successfully
    # sends a request to resend the OTP, so I won't have to create multiple rows for the same user in the OTP metadata collection, which would make it hard to track the elapsed time for each OTP request
    created_at = datetime.fromisoformat(result.updatedat)
    elapsed_time = (datetime.now(timezone.utc) - created_at).total_seconds()

    print(f"Elapsed time: {elapsed_time}")

    return elapsed_time