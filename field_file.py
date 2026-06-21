class Field:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._grid = self._empty_grid()
    
    def _empty_grid(self):
        return[[0] * self._width for _ in range (self._height)]
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    def cell(self, x, y):
        return self._grid[y][x]
    
    def set_cell(self,x , y, value):
        self._grid[y][x] = value

    def freeze (self, figure):

        for block in figure.blocks:
            if 0 <= block.y < self._height:
                self._grid[block.y][block.x]=figure.color

    def clear_lines(self):
        kept_rows = [row for row in self._grid if any(cell == 0 for cell in row)]
        cleared = self._height - len(kept_rows)
        self._grid = [[0] * self._width for _ in range(cleared)] + kept_rows
        return cleared
    
    def top_row_occupied(self):
        return any(self._grid[0])
    
    def reset(self):
        self._grid = self._empty_grid()

    def __iter__(self):
        return iter(self._grid)