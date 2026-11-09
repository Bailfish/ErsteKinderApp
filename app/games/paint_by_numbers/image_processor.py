"""Image processor converting uploaded user images into Paint-by-Numbers templates.

Supports configurable color granularity (`num_colors` between 2 and 16) and grid resolution.
"""

from collections import deque
import io
from typing import Any
import numpy as np
from PIL import Image


class ImageProcessor:
    """Quantizes uploaded images and segments them into clickable numbered SVG regions."""

    MIN_COLORS = 2
    MAX_COLORS = 16
    VIEW_WIDTH = 600
    VIEW_HEIGHT = 450

    @classmethod
    def process_uploaded_image(
        cls,
        image_bytes: bytes,
        num_colors: int = 6,
        grid_cols: int = 20,
        grid_rows: int = 15,
        title: str = "Eigenes Bild",
    ) -> dict[str, Any]:
        """Convert raw image bytes into a Paint-by-Numbers template dictionary."""
        if not image_bytes:
            raise ValueError("Empty image upload.")
        clamped_colors = max(cls.MIN_COLORS, min(cls.MAX_COLORS, int(num_colors)))
        cols = max(6, min(36, int(grid_cols)))
        rows = max(6, min(28, int(grid_rows)))

        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                rgb_img = img.convert("RGB")
        except Exception as exc:
            raise ValueError(f"Invalid image file: {exc}") from exc

        # Resize to grid dimensions using nearest/bilinear sampling
        small_img = rgb_img.resize((cols, rows), Image.Resampling.BILINEAR)
        quantized = small_img.quantize(
            colors=clamped_colors, method=Image.Quantize.MEDIANCUT
        )
        quant_rgb = quantized.convert("RGB")
        pixels = np.array(quant_rgb, dtype=np.uint8)  # shape (rows, cols, 3)

        # Extract unique RGB colors present and assign numbers 1..K
        flat_colors = pixels.reshape(-1, 3)
        unique_colors, inverse_indices = np.unique(
            flat_colors, axis=0, return_inverse=True
        )
        color_grid = (inverse_indices.reshape(rows, cols) + 1).astype(int)

        palette: list[dict[str, Any]] = []
        for idx, rgb in enumerate(unique_colors, start=1):
            r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
            hex_code = f"#{r:02X}{g:02X}{b:02X}"
            palette.append(
                {
                    "number": idx,
                    "name": f"Farbe {idx}",
                    "hex": hex_code,
                }
            )

        # Segment connected components of identical color numbers
        regions = cls._segment_connected_regions(color_grid, cols, rows)

        return {
            "id": "custom_upload",
            "title": title,
            "icon": "📷🎨",
            "view_box": f"0 0 {cls.VIEW_WIDTH} {cls.VIEW_HEIGHT}",
            "granularity": len(palette),
            "palette": palette,
            "regions": regions,
        }

    @classmethod
    def _segment_connected_regions(
        cls, color_grid: np.ndarray, cols: int, rows: int
    ) -> list[dict[str, Any]]:
        """Group adjacent cells of the same color number into clickable SVG regions."""
        visited = np.zeros((rows, cols), dtype=bool)
        cell_w = cls.VIEW_WIDTH / cols
        cell_h = cls.VIEW_HEIGHT / rows
        regions: list[dict[str, Any]] = []
        region_counter = 0

        for r in range(rows):
            for c in range(cols):
                if visited[r, c]:
                    continue
                color_num = int(color_grid[r, c])
                cells: list[tuple[int, int]] = []
                queue: deque[tuple[int, int]] = deque([(r, c)])
                visited[r, c] = True

                while queue:
                    cr, cc = queue.popleft()
                    cells.append((cr, cc))
                    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        nr, nc = cr + dr, cc + dc
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and not visited[nr, nc]
                            and int(color_grid[nr, nc]) == color_num
                        ):
                            visited[nr, nc] = True
                            queue.append((nr, nc))

                region_counter += 1
                # Build compound SVG path for all cells in this region
                path_parts = [
                    f"M {cc * cell_w:.1f} {cr * cell_h:.1f} "
                    f"h {cell_w:.1f} v {cell_h:.1f} h {-cell_w:.1f} Z"
                    for cr, cc in cells
                ]
                # Choose the cell closest to the component centroid for placing the number label
                avg_r = sum(pt[0] for pt in cells) / len(cells)
                avg_c = sum(pt[1] for pt in cells) / len(cells)
                best_cell = min(
                    cells, key=lambda pt: (pt[0] - avg_r) ** 2 + (pt[1] - avg_c) ** 2
                )
                label_x = round((best_cell[1] + 0.5) * cell_w, 1)
                label_y = round((best_cell[0] + 0.5) * cell_h, 1)

                regions.append(
                    {
                        "id": f"reg_{region_counter}",
                        "number": color_num,
                        "label_x": label_x,
                        "label_y": label_y,
                        "path_d": " ".join(path_parts),
                    }
                )

        return regions
