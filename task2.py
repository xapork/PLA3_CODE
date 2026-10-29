import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

np.set_printoptions(precision=2, suppress=True)

# Cube with side 6, centered at the origin. Each COLUMN is a vertex (x, y, z, 1).
vertices_cube = np.array([
    [-3, -3, -3, 1],
    [ 3, -3, -3, 1],
    [ 3,  3, -3, 1],
    [-3,  3, -3, 1],
    [-3, -3,  3, 1],
    [ 3, -3,  3, 1],
    [ 3,  3,  3, 1],
    [-3,  3,  3, 1],
], dtype=float).T

faces_cube = [
    [0, 1, 2, 3], [4, 5, 6, 7],
    [0, 1, 5, 4], [2, 3, 7, 6],
    [1, 2, 6, 5], [0, 3, 7, 4],
]


def plot(items, title, fname):
    """items: list of (vertices 4xN, faces, color, label)."""
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    handles = []
    for V, F, color, label in items:
        polys = [V[:3, f].T for f in F]
        ax.add_collection3d(Poly3DCollection(
            polys, facecolors=color, edgecolors="k", alpha=0.45))
        handles.append(Patch(facecolor=color, edgecolor="k", label=label))

    pts = np.hstack([V[:3] for V, _, _, _ in items])
    c = (pts.max(axis=1) + pts.min(axis=1)) / 2
    r = (pts.max(axis=1) - pts.min(axis=1)).max() / 2 * 1.1
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.set_title(title)
    ax.legend(handles=handles, loc="upper left")
    fig.tight_layout()
    fig.savefig(fname, dpi=200)
    plt.close(fig)
    print("saved", fname)


def scale(sx, sy, sz):
    return np.diag([sx, sy, sz, 1.0])


def apply(M, V):
    return M @ V          # vertices are columns -> M * V


ORIG = (vertices_cube, faces_cube, "lightgray", "original")

# ---------- Scaling matrices ----------
S1 = scale(2, 1, 1)
S2 = scale(1, 1.5, 0.5)
S = S2 @ S1                      # combined: first S1, then S2
print("S1 =\n", S1, "\nS2 =\n", S2, "\nS = S2*S1 =\n", S)
print("S1*S2 == S2*S1 ?", np.allclose(S1 @ S2, S2 @ S1))

for M, name, label in [(S1, "fig2_S1.png", "S1"),
                       (S2, "fig2_S2.png", "S2"),
                       (S,  "fig2_S.png",  "S = S2*S1")]:
    V = apply(M, vertices_cube)
    size = V[:3].max(axis=1) - V[:3].min(axis=1)
    print("\n" + label, "vertices:\n", V)
    print(label, "size (x, y, z):", size)
    plot([ORIG, (V, faces_cube, "tab:red", label)],
         f"Task 2: scaling {label}", name)