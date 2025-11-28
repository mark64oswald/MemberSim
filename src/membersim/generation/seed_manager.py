"""Seed management for reproducible generation."""

from __future__ import annotations

import hashlib
from typing import Iterator


class SeedManager:
    """Manage random seeds for reproducible parallel generation.

    Generates deterministic child seeds from a master seed, ensuring:
    1. Same master seed always produces same child seeds
    2. Child seeds are well-distributed (no clustering)
    3. Works correctly across parallel execution

    Example:
        manager = SeedManager(master_seed=42)

        # Generate members with reproducible seeds
        for i in range(100):
            member_seed = manager.get_seed(f"member_{i}")
            member = generate_member(seed=member_seed)
    """

    def __init__(self, master_seed: int = 42):
        """Initialize with master seed.

        Args:
            master_seed: The root seed for all derived seeds.
        """
        self.master_seed = master_seed
        self._cache: dict[str, int] = {}

    def get_seed(self, key: str) -> int:
        """Get a deterministic seed for a given key.

        Args:
            key: Unique identifier (e.g., "member_0", "claim_123")

        Returns:
            Deterministic seed derived from master_seed and key.
        """
        if key in self._cache:
            return self._cache[key]

        # Create deterministic seed using hash
        combined = f"{self.master_seed}:{key}"
        hash_bytes = hashlib.sha256(combined.encode()).digest()
        seed = int.from_bytes(hash_bytes[:8], byteorder="big")

        self._cache[key] = seed
        return seed

    def get_seeds(self, prefix: str, count: int) -> Iterator[int]:
        """Generate a sequence of deterministic seeds.

        Args:
            prefix: Key prefix for the sequence
            count: Number of seeds to generate

        Yields:
            Deterministic seeds for each index.
        """
        for i in range(count):
            yield self.get_seed(f"{prefix}_{i}")

    def child_manager(self, namespace: str) -> "SeedManager":
        """Create a child SeedManager with derived master seed.

        Useful for isolating different generation domains.

        Args:
            namespace: Namespace for the child manager

        Returns:
            New SeedManager with derived seed.
        """
        child_seed = self.get_seed(f"namespace:{namespace}")
        return SeedManager(master_seed=child_seed)

    def reset(self) -> None:
        """Clear the seed cache."""
        self._cache.clear()
