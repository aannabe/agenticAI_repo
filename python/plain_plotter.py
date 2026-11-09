#!/usr/bin/env python3
"""plain_plotter.py — quick-look plotting tool for tabular data files.

Usage:
    python plain_plotter.py data.csv
    python plain_plotter.py data.tsv -o figure.png

Given a CSV / TSV / whitespace-delimited file, this tool:
  - auto-detects the delimiter and whether the file has a header row
  - plots column 1 as x (or a simple 1..N index if there's only one column)
  - plots every other numeric column as a y-series on the same figure
  - saves the result (default: <input_name>.pdf in the current directory)
  - opens an interactive window, if a display is available

No LaTeX is used anywhere (text.usetex is forced off) so this runs
identically on any machine with just Python + pandas + matplotlib installed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.ticker import MaxNLocator

# ══════════════════════════════════════════════════════════════════
# STYLE CONFIGURATION — edit the constants below to change the look.
# (Everything below this section is logic; you shouldn't need to
# touch it just to restyle the plot.)
# ══════════════════════════════════════════════════════════════════

SHOW_TITLE = False      # set True to display the figure title (defaults to the file name)
GOLDEN_RATIO = 1.61803398875  # width / height ratio for the figure

FIGURE_SIZE = (GOLDEN_RATIO * 4.5, 4.5)    # inches: (width, height)
SAVE_DPI = 200          # resolution used when saving the output file
SCREEN_DPI = 100        # resolution used for the on-screen window

FONT_SIZE = 12
TITLE_SIZE = 16
LABEL_SIZE = 13
TICK_SIZE = 11
LEGEND_SIZE = 11
HANDLE_LENGTH = 4.0       # length of legend lines in inches

LINE_WIDTH = 2.0
GRID_STYLE = ":"        # dotted grid lines
GRID_ALPHA = 0.4        # faint grid

# Distinct, colorblind-friendly line colors (first 8 from the Okabe-Ito
# palette, next 8 from Paul Tol's palettes) so up to 16 series stay
# readable. Columns are colored in this order and it repeats if there
# are more y-series than colors.
COLOR_CYCLE = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # green
    "#CC79A7",  # pink
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black
    "#332288",  # indigo
    "#AA4499",  # purple
    "#44AA99",  # teal
    "#999933",  # olive
    "#882255",  # wine
    "#117733",  # dark green
    "#DDCC77",  # sand
    "#888888",  # grey
]

# Distinct line styles, cycled alongside colors so series stay tellable
# apart even in grayscale or for colorblind viewers. Matplotlib only
# has 4 named styles, so the rest are custom (on, off, on, off, ...)
# dash patterns in points, e.g. (3, 1, 1, 1) = 3pt dash, 1pt gap,
# 1pt dot, 1pt gap, repeating.
LINESTYLE_CYCLE = [
    "-",                      # solid
    "--",                     # dashed
    ":",                      # dotted
    "-.",                     # dash-dot
    (0, (5, 1)),              # densely dashed
    (0, (1, 1)),              # densely dotted
    (0, (3, 1, 1, 1)),        # densely dash-dot
    (0, (3, 5, 1, 5, 1, 5)),  # dash-dot-dot
]

# Distinct marker shapes, cycled alongside color and linestyle. A few
# matplotlib markers are excluded on purpose (e.g. "+", "x", "1"-"4")
# because they're thin lines rather than filled shapes and read poorly
# at a glance next to the others.
MARKER_CYCLE = [
    "o",  # circle
    "s",  # square
    "^",  # triangle up
    "v",  # triangle down
    "D",  # diamond
    "P",  # filled plus
    "X",  # filled x
    "*",  # star
    "p",  # pentagon
    "h",  # hexagon
    "<",  # triangle left
    ">",  # triangle right
    "8",  # octagon
    "d",  # thin diamond
]
MARKER_SIZE = 6
# Roughly how many markers to draw per line, regardless of how many
# data points it has (dense data gets markers spaced out so they don't
# turn into a solid blob).
MARKERS_PER_LINE = 20

# If the x-values are all whole numbers (e.g. 0, 1, 2, ...), force the
# x-axis to only label whole numbers instead of letting matplotlib pick
# fractional ticks like 0.5, 1.5. Has no effect when x is genuinely
# fractional (e.g. 0.1, 0.2, ...).
INTEGER_XTICKS_WHEN_POSSIBLE = True


def apply_style() -> None:
    """Apply the constants above to matplotlib's global settings.

    To change how plots look, edit the constants above this function,
    not the function body itself.
    """
    plt.rcParams.update(
        {
            "figure.figsize": FIGURE_SIZE,
            "figure.dpi": SCREEN_DPI,
            "font.size": FONT_SIZE,
            "axes.titlesize": TITLE_SIZE,
            "axes.labelsize": LABEL_SIZE,
            "xtick.labelsize": TICK_SIZE,
            "ytick.labelsize": TICK_SIZE,
            "legend.fontsize": LEGEND_SIZE,
            "axes.prop_cycle": cycler(color=COLOR_CYCLE),
            # Portability: never depend on a system LaTeX install, and
            # avoid unicode glyphs (e.g. the unicode minus sign) that
            # some fonts lack.
            "text.usetex": False,
            "axes.unicode_minus": False,
        }
    )


# ══════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════


def _read_raw(filepath: Path) -> pd.DataFrame:
    """Read the file into a DataFrame with no assumptions about headers,
    auto-detecting whether it's comma, tab, or whitespace delimited."""
    try:
        df = pd.read_csv(filepath, sep=None, engine="python", header=None)
    except Exception:
        df = pd.read_csv(filepath, sep=r"\s+", engine="python", header=None)

    # pandas' delimiter sniffing can collapse whitespace-separated data
    # into a single column. Detect that and retry with whitespace as
    # the explicit separator.
    if df.shape[1] == 1:
        first_cell = str(df.iloc[0, 0])
        if len(first_cell.split()) > 1:
            df = pd.read_csv(filepath, sep=r"\s+", engine="python", header=None)

    return df


def _row_is_numeric(row: pd.Series) -> bool:
    """True if every value in the row can be parsed as a float."""
    for value in row:
        try:
            float(value)
        except (TypeError, ValueError):
            return False
    return True


def load_data(filepath: Path) -> tuple[np.ndarray, str, dict[str, pd.Series]]:
    """Load a data file and return (x_values, x_label, y_series).

    y_series maps column label -> pandas Series of y values. If the
    file has only one usable numeric column, x is a generated
    1..N index and that column becomes the sole y-series.
    """
    raw = _read_raw(filepath)

    if _row_is_numeric(raw.iloc[0]):
        # No header: first row is already data.
        raw.columns = [f"Column {i + 1}" for i in range(raw.shape[1])]
        data = raw
    else:
        # First row looks like labels: use it as the header.
        headers = [str(value).strip() for value in raw.iloc[0]]
        data = raw.iloc[1:].reset_index(drop=True)
        data.columns = headers

    numeric_columns: dict[str, pd.Series] = {}
    for name in data.columns:
        column = data[name]
        converted = pd.to_numeric(column, errors="coerce")
        failed_to_parse = column.notna() & converted.isna()
        if failed_to_parse.any():
            print(
                f"Warning: skipping column '{name}' (contains non-numeric values).",
                file=sys.stderr,
            )
            continue
        numeric_columns[str(name)] = converted

    if not numeric_columns:
        sys.exit("Error: no numeric columns found to plot.")

    names = list(numeric_columns.keys())

    if len(names) == 1:
        only_series = numeric_columns[names[0]]
        x = np.arange(1, len(only_series) + 1)
        return x, "Index", {names[0]: only_series}

    x_label = names[0]
    x = numeric_columns[x_label].to_numpy()
    y_series = {name: numeric_columns[name] for name in names[1:]}
    return x, x_label, y_series


# ══════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════


def build_figure(
    x: np.ndarray,
    x_label: str,
    y_series: dict[str, pd.Series],
    title: str,
) -> plt.Figure:
    """Build and return a matplotlib Figure with all y-series plotted
    against x on one set of axes."""
    fig, ax = plt.subplots()

    # Space markers out so dense data doesn't turn into a solid blob of
    # symbols; sparse data just gets a marker on every point.
    markevery = max(1, len(x) // MARKERS_PER_LINE)

    for index, (label, y) in enumerate(y_series.items()):
        color = COLOR_CYCLE[index % len(COLOR_CYCLE)]
        linestyle = LINESTYLE_CYCLE[index % len(LINESTYLE_CYCLE)]
        marker = MARKER_CYCLE[index % len(MARKER_CYCLE)]
        ax.plot(
            x,
            y,
            label=label,
            color=color,
            linestyle=linestyle,
            linewidth=LINE_WIDTH,
            marker=marker,
            markersize=MARKER_SIZE,
            markevery=markevery,
        )

    ax.set_xlabel(x_label)
    ax.set_ylabel(next(iter(y_series)) if len(y_series) == 1 else "Value")
    if SHOW_TITLE:
        ax.set_title(title)

    if INTEGER_XTICKS_WHEN_POSSIBLE and np.allclose(x, np.round(x)):
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.grid(True, linestyle=GRID_STYLE, alpha=GRID_ALPHA)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if len(y_series) > 1:
        ax.legend(frameon=False, handlelength=HANDLE_LENGTH)

    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Quickly plot a data file (CSV, TSV, or whitespace-delimited)."
    )
    parser.add_argument("input_file", type=Path, help="Path to the data file to plot.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output image path (default: <input_name>.pdf in the current directory). "
        "Format is inferred from the file extension, e.g. '-o plot.png'.",
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        sys.exit(f"Error: file not found: {args.input_file}")

    apply_style()

    x, x_label, y_series = load_data(args.input_file)
    title = args.input_file.name
    fig = build_figure(x, x_label, y_series, title)

    output_path = args.output or Path.cwd() / f"{args.input_file.stem}.pdf"
    fig.savefig(output_path, dpi=SAVE_DPI, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")

    try:
        plt.show()
    except Exception:
        print("Note: no display available; skipping interactive window.", file=sys.stderr)


if __name__ == "__main__":
    main()
