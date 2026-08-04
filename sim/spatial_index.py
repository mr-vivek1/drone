"""
Uniform spatial hash grid for 3D neighbor queries.

This implementation maps 3D space into cubic grid cells of size `cell_size`.
Each inserted object (drone) is stored in the cell computed by flooring
its position divided by the cell size. Neighbor queries within a radius
only examine the cells that overlap the query sphere, reducing the number
of narrow-phase distance checks compared to O(N^2) scans.

API:
  insert(obj)       - insert object (must have `.position` with x,y,z)
  remove(obj)       - remove object
  update(obj)       - update object's cell membership after it moved
  query_radius(pos, r) - return iterable of objects within radius r of pos
  clear()           - clear the grid

Notes:
- Objects stored are the drone instances themselves. The grid stores a
  mapping from integer cell coords (ix,iy,iz) to a set of objects.
- The cell size should be chosen according to typical interaction radius
  (e.g., SAFE_DISTANCE) to balance per-cell candidate counts vs number
  of cells to check.
"""

from math import floor
from collections import defaultdict
from config import *


def _cell_coords_for_pos(pos, cell_size):
    """Return integer 3-tuple cell coordinates for a position-like object."""
    return (
        int(floor(pos.x / cell_size)),
        int(floor(pos.y / cell_size)),
        int(floor(pos.z / cell_size)),
    )


class SpatialHashGrid:
    def __init__(self, cell_size=GRID_CELL_SIZE):
        self.cell_size = float(cell_size)
        # cell -> set(objects)
        self._cells = defaultdict(set)
        # object -> cell coords
        self._obj_cell = {}

    def insert(self, obj):
        """Insert obj into the grid. obj must have `.position` with x,y,z.

        We record the object's current cell so subsequent `update` calls can
        efficiently move it when it crosses cell boundaries.
        """
        cell = _cell_coords_for_pos(obj.position, self.cell_size)
        self._cells[cell].add(obj)
        self._obj_cell[obj] = cell

    def remove(self, obj):
        cell = self._obj_cell.get(obj)
        if cell is None:
            return
        bucket = self._cells.get(cell)
        if bucket and obj in bucket:
            bucket.remove(obj)
            if not bucket:
                del self._cells[cell]
        del self._obj_cell[obj]

    def update(self, obj):
        """Update object's cell membership based on its current position."""
        old = self._obj_cell.get(obj)
        new = _cell_coords_for_pos(obj.position, self.cell_size)
        if old == new:
            return
        # remove from old
        if old is not None:
            bucket = self._cells.get(old)
            if bucket and obj in bucket:
                bucket.remove(obj)
                if not bucket:
                    del self._cells[old]
        # add to new
        self._cells[new].add(obj)
        self._obj_cell[obj] = new

    def query_radius(self, pos, radius):
        """Return list of objects whose positions are within `radius` of `pos`.

        The function computes the AABB of the sphere and iterates the cells
        overlapping that box. For each candidate object we perform the
        accurate distance check.
        """
        cx_min = int(floor((pos.x - radius) / self.cell_size))
        cy_min = int(floor((pos.y - radius) / self.cell_size))
        cz_min = int(floor((pos.z - radius) / self.cell_size))

        cx_max = int(floor((pos.x + radius) / self.cell_size))
        cy_max = int(floor((pos.y + radius) / self.cell_size))
        cz_max = int(floor((pos.z + radius) / self.cell_size))

        found = []
        r2 = radius * radius
        for ix in range(cx_min, cx_max + 1):
            for iy in range(cy_min, cy_max + 1):
                for iz in range(cz_min, cz_max + 1):
                    cell = (ix, iy, iz)
                    bucket = self._cells.get(cell)
                    if not bucket:
                        continue
                    for obj in bucket:
                        # Assume obj.position is Vec3-like
                        dx = obj.position.x - pos.x
                        dy = obj.position.y - pos.y
                        dz = obj.position.z - pos.z
                        if dx * dx + dy * dy + dz * dz <= r2:
                            found.append(obj)

        return found

    def clear(self):
        self._cells.clear()
        self._obj_cell.clear()
