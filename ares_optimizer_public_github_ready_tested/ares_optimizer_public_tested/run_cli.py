from __future__ import annotations

import argparse
import json

from app import AresOptimizer
from app.schemas import UserRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ARES Optimizer public showcase pipeline.")
    parser.add_argument("message", nargs="?", default="Explain the ARES optimizer architecture")
    args = parser.parse_args()
    response = AresOptimizer().handle(UserRequest(message=args.message))
    print(json.dumps(response.model_dump(), indent=2))


if __name__ == "__main__":
    main()
