"""Make docs/overview.png, the figure at the top of the README.

Run from the repository root:  python scripts/make_overview.py
"""

from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from skimage import data  # noqa: E402

out = Path(__file__).resolve().parents[1] / "docs" / "overview.png"
out.parent.mkdir(exist_ok=True)

moon = data.moon()
camera = data.camera()
coins = data.coins()

# salt and pepper noise, same as notebook 05
rng = np.random.default_rng(0)
noisy = camera.copy()
mask = rng.random(camera.shape)
noisy[mask < 0.025] = 0
noisy[mask > 0.975] = 255

_, otsu = cv2.threshold(coins, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
edges = cv2.Canny(cv2.GaussianBlur(camera, (5, 5), 1.4), 50, 150, L2gradient=True)

pairs = [
    (moon, "moon", cv2.equalizeHist(moon), "histogram equalization"),
    (camera, "camera", edges, "Canny edges"),
    (coins, "coins", otsu, "Otsu threshold"),
    (noisy[60:220, 160:320], "salt and pepper noise", cv2.medianBlur(noisy, 5)[60:220, 160:320], "median filter"),
]

fig, ax = plt.subplots(2, 4, figsize=(16, 8.4))
for col, (before, t1, after, t2) in enumerate(pairs):
    ax[0, col].imshow(before, cmap="gray", vmin=0, vmax=255)
    ax[0, col].set_title(t1)
    ax[1, col].imshow(after, cmap="gray", vmin=0, vmax=255)
    ax[1, col].set_title(t2)
for a in ax.ravel():
    a.axis("off")
fig.tight_layout()
fig.savefig(out, dpi=110, bbox_inches="tight")
print("wrote", out)
