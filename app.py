"""
Robot Fleet Recovery Under Cascading Failures
Complete simulation for VS Code / educational use.

Features:
- Multiple robots in a fleet
- Random or forced failures
- Cascading effect (one failure overloads neighbors)
- Detection + layered recovery (local → peer → fleet)
- Task reassignment
- Connectivity restoration
- Live console log + optional matplotlib visualization
"""

import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# ====================== CONFIG ======================
NUM_ROBOTS = 8
MAX_LOAD = 100.0
FAILURE_PROB = 0.08          # chance a healthy robot fails each step
CASCADE_THRESHOLD = 85.0     # load above this can trigger cascade
STEPS = 60
SEED = 42
random.seed(SEED)

# ====================== DATA STRUCTURES ======================
class RobotState(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"

@dataclass
class Robot:
    id: int
    load: float = 0.0
    state: RobotState = RobotState.HEALTHY
    neighbors: Set[int] = field(default_factory=set)
    tasks: List[str] = field(default_factory=list)
    failure_time: Optional[int] = None

    def is_active(self) -> bool:
        return self.state in (RobotState.HEALTHY, RobotState.DEGRADED)

# ====================== FLEET SIMULATOR ======================
class RobotFleet:
    def __init__(self, n: int):
        self.robots: Dict[int, Robot] = {}
        self.step = 0
        self.history = []          # for plotting
        self.recovery_log = []

        # Create robots in a ring + some extra edges (connected fleet)
        for i in range(n):
            self.robots[i] = Robot(id=i)

        for i in range(n):
            self.robots[i].neighbors.add((i - 1) % n)
            self.robots[i].neighbors.add((i + 1) % n)
            # add a few long-range links for robustness
            if i % 3 == 0:
                self.robots[i].neighbors.add((i + 3) % n)

        # Initial task distribution
        self._distribute_tasks()

    def _distribute_tasks(self):
        tasks = [f"Task-{t}" for t in range(1, 25)]
        active = [r for r in self.robots.values() if r.is_active()]
        if not active:
            return
        for i, task in enumerate(tasks):
            robot = active[i % len(active)]
            robot.tasks.append(task)
            robot.load = min(MAX_LOAD, robot.load + random.uniform(8, 15))

    def inject_failure(self, robot_id: int, reason: str = "spontaneous"):
        r = self.robots[robot_id]
        if r.state == RobotState.FAILED:
            return
        r.state = RobotState.FAILED
        r.failure_time = self.step
        r.load = 0.0
        print(f"  💥 Robot {robot_id} FAILED ({reason}) at step {self.step}")
        self._cascade_from(robot_id)

    def _cascade_from(self, failed_id: int):
        """Propagate load to neighbors → possible secondary failures"""
        failed = self.robots[failed_id]
        extra_load = sum(15 for _ in failed.tasks)  # redistribute its tasks
        failed.tasks.clear()

        neighbors = list(failed.neighbors)
        if not neighbors:
            return

        share = extra_load / len(neighbors)
        for nid in neighbors:
            n = self.robots[nid]
            if not n.is_active():
                continue
            n.load += share
            n.tasks.extend([f"reassigned-from-{failed_id}"])
            if n.load > CASCADE_THRESHOLD and n.state == RobotState.HEALTHY:
                n.state = RobotState.DEGRADED
                print(f"  ⚠️  Robot {nid} became DEGRADED (load={n.load:.1f})")
            if n.load > MAX_LOAD * 0.98:
                self.inject_failure(nid, reason=f"cascade from {failed_id}")

    def detect_and_recover(self):
        """Layered recovery: local → peer → fleet"""
        failed = [r for r in self.robots.values() if r.state == RobotState.FAILED]
        degraded = [r for r in self.robots.values() if r.state == RobotState.DEGRADED]

        # 1. Local recovery attempts for degraded robots
        for r in degraded:
            if random.random() < 0.4:          # 40% chance local fix works
                r.state = RobotState.HEALTHY
                r.load *= 0.7
                print(f"  ✅ Robot {r.id} self-recovered (local)")
                self.recovery_log.append((self.step, r.id, "local"))

        # 2. Peer-assisted recovery
        for r in failed:
            for nid in r.neighbors:
                peer = self.robots[nid]
                if peer.is_active() and peer.load < CASCADE_THRESHOLD * 0.7:
                    # Peer takes temporary responsibility + helps restore
                    peer.load += 10
                    r.state = RobotState.RECOVERING
                    print(f"  🤝 Peer Robot {nid} assisting Robot {r.id}")
                    self.recovery_log.append((self.step, r.id, "peer"))
                    break

        # 3. Fleet-level reassignment & connectivity repair
        active = [r for r in self.robots.values() if r.is_active() or r.state == RobotState.RECOVERING]
        if len(active) < 2:
            return

        # Re-balance load
        total_load = sum(r.load for r in active)
        avg = total_load / len(active)
        for r in active:
            if r.load > avg * 1.3:
                excess = r.load - avg
                r.load = avg
                # give excess to least loaded
                least = min(active, key=lambda x: x.load)
                least.load += excess * 0.6

        # Restore some failed robots after a few steps (fleet recovery)
        for r in failed:
            if r.failure_time is not None and self.step - r.failure_time > 8:
                if random.random() < 0.55:
                    r.state = RobotState.HEALTHY
                    r.load = random.uniform(20, 40)
                    print(f"  🔄 Fleet recovered Robot {r.id}")
                    self.recovery_log.append((self.step, r.id, "fleet"))

    def step_simulation(self):
        self.step += 1

        # Natural small load fluctuations
        for r in self.robots.values():
            if r.is_active():
                r.load += random.uniform(-3, 5)
                r.load = max(0, min(MAX_LOAD, r.load))

        # Random spontaneous failures
        for r in list(self.robots.values()):
            if r.state == RobotState.HEALTHY and random.random() < FAILURE_PROB:
                self.inject_failure(r.id)

        # Detection & recovery every step
        self.detect_and_recover()

        # Record state for visualization
        states = {
            "healthy": sum(1 for r in self.robots.values() if r.state == RobotState.HEALTHY),
            "degraded": sum(1 for r in self.robots.values() if r.state == RobotState.DEGRADED),
            "failed": sum(1 for r in self.robots.values() if r.state == RobotState.FAILED),
            "recovering": sum(1 for r in self.robots.values() if r.state == RobotState.RECOVERING),
            "avg_load": np.mean([r.load for r in self.robots.values() if r.is_active()] or [0])
        }
        self.history.append(states)

        # Console summary
        print(f"\n=== Step {self.step} ===")
        print(f"Healthy: {states['healthy']} | Degraded: {states['degraded']} | "
              f"Failed: {states['failed']} | Recovering: {states['recovering']} | "
              f"Avg Load: {states['avg_load']:.1f}")

# ====================== MAIN + VISUALIZATION ======================
def run_simulation():
    fleet = RobotFleet(NUM_ROBOTS)

    print("🚀 Starting Robot Fleet Recovery Simulation")
    print("=" * 55)

    # Force one early cascading failure for demonstration
    time.sleep(0.5)
    fleet.inject_failure(3, reason="forced demo failure")

    for _ in range(STEPS):
        fleet.step_simulation()
        time.sleep(0.15)          # slow down so you can read the log

    print("\n" + "=" * 55)
    print("✅ Simulation finished")
    print(f"Total recovery events: {len(fleet.recovery_log)}")
    for t, rid, method in fleet.recovery_log:
        print(f"  Step {t}: Robot {rid} recovered via {method}")

    # ---- Optional live-style plot ----
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
        steps = range(1, len(fleet.history) + 1)

        healthy = [h["healthy"] for h in fleet.history]
        degraded = [h["degraded"] for h in fleet.history]
        failed = [h["failed"] for h in fleet.history]
        recovering = [h["recovering"] for h in fleet.history]
        avg_load = [h["avg_load"] for h in fleet.history]

        ax1.stackplot(steps, healthy, degraded, recovering, failed,
                      labels=["Healthy", "Degraded", "Recovering", "Failed"],
                      colors=["#2ecc71", "#f1c40f", "#3498db", "#e74c3c"], alpha=0.8)
        ax1.set_ylabel("Number of Robots")
        ax1.set_title("Robot Fleet State Over Time (Cascading Failures + Recovery)")
        ax1.legend(loc="upper right")
        ax1.set_ylim(0, NUM_ROBOTS + 1)
        ax1.grid(True, alpha=0.3)

        ax2.plot(steps, avg_load, color="#9b59b6", linewidth=2)
        ax2.axhline(CASCADE_THRESHOLD, color="orange", linestyle="--", label="Cascade Threshold")
        ax2.set_xlabel("Simulation Step")
        ax2.set_ylabel("Average Load of Active Robots")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"(Plot skipped – matplotlib issue: {e})")

if __name__ == "__main__":
    run_simulation()