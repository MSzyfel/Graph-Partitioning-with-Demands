"""Calculate the dense 3D approximation-ratio mesh for PGFPlots.

This script writes numeric coordinates only. The standalone TeX source uses
PGFPlots to render every point and surface; this script does no plotting.
"""

from __future__ import annotations

import csv
import math
from collections.abc import Callable
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent / "generated"
RHO_MIN = 0.005
RHO_MAX = 0.995
RHO_SAMPLES = 101
MAIN_T_SAMPLES = 512
DIRECT_T_SAMPLES = 51
RATIO_CAP = 12.0


def linspace(start: float, stop: float, count: int) -> list[float]:
    if count < 2:
        raise ValueError("A mesh axis needs at least two samples")
    return [start + (stop - start) * i / (count - 1) for i in range(count)]


def floor_log2(value: float) -> int:
    """Return the mathematical floor, snapping floating-point exact powers."""
    exponent = math.log2(value)
    nearest_integer = round(exponent)
    if abs(exponent - nearest_integer) <= 4 * math.ulp(exponent):
        exponent = float(nearest_integer)
    return math.floor(exponent)


def tree_ratio(rho: float, t: float) -> float:
    """Evaluate the proved minimum bound at eta=rho+(1-rho)t, capped at 12."""
    eta_minus_rho = (1.0 - rho) * t
    eta = rho + eta_minus_rho
    eta = min(eta, math.nextafter(1.0, 0.0))

    anchored_lp = 2.0 * eta / eta_minus_rho
    recursive = floor_log2(1.0 / t) + 1
    hybrid = (
        4.0 * eta / (rho + 2.0 * eta_minus_rho)
        + floor_log2((rho + 2.0 * eta_minus_rho) / eta_minus_rho)
        + 1
    )
    return min(RATIO_CAP, anchored_lp, float(recursive), hybrid)


def write_mesh(
    path: Path,
    t_at: Callable[[int, float], float],
    row_count: int,
    rho_values: list[float],
    ratio_at: Callable[[float, float], float],
) -> int:
    """Write a row-major PGFPlots lattice: t rows, rho columns."""
    point_count = 0
    with path.open("w", newline="", encoding="ascii") as output:
        writer = csv.writer(output, delimiter=" ", lineterminator="\n")
        writer.writerow(("rho", "eta", "ratio"))
        for row in range(row_count):
            for rho in rho_values:
                t = t_at(row, rho)
                eta = rho + (1.0 - rho) * t
                ratio = ratio_at(rho, t)
                writer.writerow(
                    (
                        format(rho, ".15g"),
                        format(eta, ".15g"),
                        format(ratio, ".15g"),
                    )
                )
                point_count += 1
    return point_count


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rho_values = linspace(RHO_MIN, RHO_MAX, RHO_SAMPLES)

    main_points = write_mesh(
        OUTPUT_DIR / "tree_approximation_ratio_3d_main.dat",
        lambda row, _rho: 1e-5 * 50000.0 ** (row / (MAIN_T_SAMPLES - 1)),
        MAIN_T_SAMPLES,
        rho_values,
        tree_ratio,
    )

    cap_points = write_mesh(
        OUTPUT_DIR / "tree_approximation_ratio_3d_cap.dat",
        lambda row, _rho: 1e-5 * row,
        2,
        rho_values,
        lambda _rho, _t: RATIO_CAP,
    )

    def direct_t(row: int, rho: float) -> float:
        # Match the 2D plot's threshold+0.0001 start for each fixed rho.
        first_t = 0.5 + 1e-4 / (1.0 - rho)
        last_t = 0.99999
        return first_t + (last_t - first_t) * row / (DIRECT_T_SAMPLES - 1)

    direct_points = write_mesh(
        OUTPUT_DIR / "tree_approximation_ratio_3d_direct.dat",
        direct_t,
        DIRECT_T_SAMPLES,
        rho_values,
        lambda _rho, _t: 1.0,
    )

    total_points = main_points + cap_points + direct_points
    print(f"Main-bound mesh: {main_points:,} vertices ({RHO_SAMPLES} x {MAIN_T_SAMPLES})")
    print(f"Capped boundary strip: {cap_points:,} vertices ({RHO_SAMPLES} x 2)")
    print(f"Direct-DP region: {direct_points:,} vertices ({RHO_SAMPLES} x {DIRECT_T_SAMPLES})")
    print(f"Total: {total_points:,} vertices; {total_points / 312:.2f}x the original 312-point mesh")
    print(f"Wrote coordinate tables to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
