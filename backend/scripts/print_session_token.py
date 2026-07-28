"""One-off: print a signed session token for a given email, for manual QA of
authenticated flows (e.g. billing portal) against an account whose inbox
can't receive the normal login-code email (test-checkout@example.com bounces
at Resend, since example.com isn't a deliverable domain)."""

import sys

from app.core.security import create_access_token


def main() -> None:
    email = sys.argv[1]
    print(create_access_token({"sub": email}))


if __name__ == "__main__":
    main()
