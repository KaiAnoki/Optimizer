from __future__ import annotations

import argparse
import json

from app import AresOptimizer
from app.schemas import UserRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect an ARES routing decision.")
    parser.add_argument("message", nargs="?", default="Explain the ARES optimizer architecture")
    args = parser.parse_args()
    response = AresOptimizer().handle(UserRequest(message=args.message))
    print(json.dumps(response.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()
