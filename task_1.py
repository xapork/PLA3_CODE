import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

np.set_printoptions(precision=2, suppress=True)

# Cube with side 6, centered at the origin. Each COLUMN is a vertex (x, y, z, 1).
vertices_cube = np.array([
    [-3, -3, -3, 1],   # 0
    [ 3, -3, -3, 1],   # 1
    [ 3,  3, -3, 1],   # 2
    [-3,  3, -3, 1],   # 3
    [-3, -3,  3, 1],   # 4
    [ 3, -3,  3, 1],   # 5
    [ 3,  3,  3, 1],   # 6
    [-3,  3,  3, 1],   # 7
], dtype=float).T

# Each face is a list of vertex indices
faces_cube = [
    [0, 1, 2, 3], [4, 5, 6, 7],
    [0, 1, 5, 4], [2, 3, 7, 6],
    [1, 2, 6, 5], [0, 3, 7, 4],
]

# Another figure: square pyramid (base 6x6, height 6)
vertices_pyramid = np.array([
    [-3, -3, 0, 1],
    [ 3, -3, 0, 1],
    [ 3,  3, 0, 1],
    [-3,  3, 0, 1],
    [ 0,  0, 6, 1],
], dtype=float).T

faces_pyramid = [
    [0, 1, 2, 3],
    [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
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


print("Cube vertices (columns):\n", vertices_cube)
print("Pyramid vertices (columns):\n", vertices_pyramid)

plot([(vertices_cube, faces_cube, "tab:blue", "cube 6x6x6")],
     "Task 1: cube", "fig1_cube.png")
plot([(vertices_pyramid, faces_pyramid, "tab:orange", "pyramid")],
     "Task 1: pyramid", "fig1_pyramid.png")