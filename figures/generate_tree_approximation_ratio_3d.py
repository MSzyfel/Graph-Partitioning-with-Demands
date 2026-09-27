"""Calculate the dense 3D approximation-ratio mesh for PGFPlots.

This script writes numeric coordinates only. The standalone TeX source uses
PGFPlots to render every point and surface; this script does no plotting.
"""

from __future__ import annotations

import csv
import math
from collections.abc import Callable
from pathlib import Path


# Write the numeric PGFPlots input tables beside this script, independent of
# the working directory used to run it.
OUTPUT_DIR = Path(__file__).resolve().parent / "generated"

# Sample rho over a near-full interval, avoiding the singular endpoints 0 and
# 1. Both endpoints are included in the mesh.
RHO_MIN = 0.001
RHO_MAX = 0.999

# Number of equally spaced rho columns in each mesh. More samples make the
# surface smoother horizontally, at the cost of larger data files/render time.
RHO_SAMPLES = 256

# Number of base samples in the main-bound region, logarithmically spaced in t
# from 1e-5 to 0.5. Here eta = rho + (1-rho)*t; centroid coverage gives ratio
# 1 at t=0.5, corresponding to eta=(1+rho)/2.
MAIN_T_SAMPLES = 512

# Include exact e^{-k} values where the standalone centroid depth changes.
COVERAGE_EXPONENTIAL_LEVELS = range(1, 11)

# Number of samples above the centroid unit-ratio threshold, from eta just
# above (1+rho)/2 to nearly 1. This separate mesh is flat at ratio 1.
UNIT_RATIO_T_SAMPLES = 51

# Maximum displayed approximation ratio. Larger bounds are clipped to this
# height; the narrow strip next to eta=rho is filled at this capped height.
RATIO_CAP = 8.0

def linspace(start: float, stop: float, count: int) -> list[float]:
    if count < 2:
        raise ValueError("A mesh axis needs at least two samples")
    return [start + (stop - start) * i / (count - 1) for i in range(count)]


def ceil_ln(value: float) -> int:
    """Return ceil(ln(value)), snapping floating-point exact exponentials."""
    exponent = math.log(value)
    nearest_integer = round(exponent)
    if abs(exponent - nearest_integer) <= 4 * math.ulp(exponent):
        exponent = float(nearest_integer)
    return math.ceil(exponent)


def tree_ratio(rho: float, t: float) -> float:
    """Evaluate the best proved tree bound, capped at RATIO_CAP."""
    eta_minus_rho = (1.0 - rho) * t
    eta = rho + eta_minus_rho
    eta = min(eta, math.nextafter(1.0, 0.0))

    anchored_lp = 2.0 * eta / eta_minus_rho
    hybrid = math.inf
    if rho < 1.0 / 3.0 and eta < 3.0 * rho:
        hybrid = math.e + 1.0 + math.log(2.0 * rho / eta_minus_rho)
    centroid_coverage = ceil_ln(1.0 / t)
    return min(RATIO_CAP, anchored_lp, hybrid, centroid_coverage)


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
    main_t_values = {
        1e-5 * 50000.0 ** (row / (MAIN_T_SAMPLES - 1))
        for row in range(MAIN_T_SAMPLES)
    }
    main_t_values.update(math.exp(-level) for level in COVERAGE_EXPONENTIAL_LEVELS)
    main_t_values = sorted(main_t_values)

    main_points = write_mesh(
        OUTPUT_DIR / "tree_approximation_ratio_3d_main.dat",
        lambda row, _rho: main_t_values[row],
        len(main_t_values),
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

    def unit_ratio_t(row: int, rho: float) -> float:
        # Match the 2D plot's threshold+0.0001 start for each fixed rho.
        first_t = 0.5 + 1e-4 / (1.0 - rho)
        last_t = 0.99999
        return first_t + (last_t - first_t) * row / (UNIT_RATIO_T_SAMPLES - 1)

    unit_ratio_points = write_mesh(
        OUTPUT_DIR / "tree_approximation_ratio_3d_direct.dat",
        unit_ratio_t,
        UNIT_RATIO_T_SAMPLES,
        rho_values,
        lambda _rho, _t: 1.0,
    )

    total_points = main_points + cap_points + unit_ratio_points
    print(f"Main-bound mesh: {main_points:,} vertices ({RHO_SAMPLES} x {len(main_t_values)})")
    print(f"Capped boundary strip: {cap_points:,} vertices ({RHO_SAMPLES} x 2)")
    print(f"Centroid unit-ratio region: {unit_ratio_points:,} vertices ({RHO_SAMPLES} x {UNIT_RATIO_T_SAMPLES})")
    print(f"Total: {total_points:,} vertices; {total_points / 312:.2f}x the original 312-point mesh")
    print(f"Wrote coordinate tables to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
