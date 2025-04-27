import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing

# A class for modeling the game grid
class GameGrid:
   # A constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles locked on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # Add next tetromino property
      self.next_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      self.score = 0

      # set the color used for the empty grid cells
      self.empty_cell_color = Color(42, 69, 99)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(0, 100, 200)
      self.boundary_color = Color(0, 100, 200)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness

   # A method for displaying the game grid
   def display(self):
    # 1. Arka planı temizle
    stddraw.clear(self.empty_cell_color)

    # 2. Oyun gridini çiz
    self.draw_grid()

    # 3. Tetromino varsa onu çiz
    if self.current_tetromino is not None:
        self.current_tetromino.draw()

    # 4. Gridin kenar kutusunu çiz
    self.draw_boundaries()

    # 5. Skor yazısı ve başlığı
    stddraw.setFontSize(20)
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.text(self.grid_width + 1, self.grid_height - 1, "SCORE")

    stddraw.setFontSize(16)
    stddraw.text(self.grid_width + 1, self.grid_height - 2, f"{self.score}")
    
    # 6. Sonraki tetromino başlığı ve gösterimi
    stddraw.setFontSize(20)
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.text(self.grid_width + 1, self.grid_height - 4, "NEXT")
    
    # Sonraki tetromino'yu çiz
    if self.next_tetromino is not None:
        self.draw_next_tetromino()

    # 7. Her şeyi göster
    stddraw.show(250)

   # Sonraki tetromino'yu çizme metodu
   def draw_next_tetromino(self):
      if self.next_tetromino is None:
         return
         
      # Sonraki tetromino'nun matrisini al
      tile_matrix = self.next_tetromino.tile_matrix
      n = len(tile_matrix)  # Matris boyutu
      
      # Çizim konumunu güncelle - y pozisyonunu düşür
      center_x = self.grid_width + 1
      center_y = self.grid_height - 7  # 6'dan 7'ye değiştirdik
      
      # Her bir hücreyi çiz
      for row in range(n):
         for col in range(n):
            if tile_matrix[row][col] is not None:
               # Tetromino'nun ortasını referans alarak konum hesapla
               pos_x = center_x + (col - n/2 + 0.5)
               pos_y = center_y - (row - n/2 + 0.5)
               
               # Bu konumda tile'ı çiz
               tile_matrix[row][col].draw(Point(pos_x, pos_y))


   def clear_full_rows(self):
    rows_cleared = 0
    for row in range(self.grid_height):
        full = True
        row_sum = 0
        for col in range(self.grid_width):
            tile = self.tile_matrix[row][col]
            if tile is None:
                full = False
                break
            else:
                row_sum += tile.number

        if full:
            # 1. Skora ekle
            self.score += row_sum
            rows_cleared += 1

            # 2. Satırı temizle
            for col in range(self.grid_width):
                self.tile_matrix[row][col] = None

            # 3. Üst satırları aşağı kaydır
            for r in range(row, self.grid_height - 1):
                for c in range(self.grid_width):
                    self.tile_matrix[r][c] = self.tile_matrix[r + 1][c]

            # 4. En üst satırı boş yap
            for c in range(self.grid_width):
                self.tile_matrix[self.grid_height - 1][c] = None

            # 5. Aynı satırı tekrar kontrol et
            row -= 1
    return rows_cleared
   
 
   def merge_tiles(self):
    for col in range(self.grid_width):
      merged_flags = [False for _ in range(self.grid_height)]
      for row in range(self.grid_height - 1):
        current_tile = self.tile_matrix[row][col]
        tile_above = self.tile_matrix[row + 1][col]

        if current_tile and tile_above and current_tile.number == tile_above.number:
            if not merged_flags[row] and not merged_flags[row + 1]:
                self.tile_matrix[row][col].number *= 2
                self.tile_matrix[row + 1][col] = None
                merged_flags[row] = True
                self.score += self.tile_matrix[row][col].number


    self.drop_floating_tiles()
   def drop_floating_tiles(self):
    for col in range(self.grid_width):
        for row in range(1, self.grid_height):
            if self.tile_matrix[row][col] is not None and self.tile_matrix[row - 1][col] is None:
                current_row = row
                while current_row > 0 and self.tile_matrix[current_row - 1][col] is None:
                    self.tile_matrix[current_row - 1][col] = self.tile_matrix[current_row][col]
                    self.tile_matrix[current_row][col] = None
                    current_row -= 1

   # A method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # if the current grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               # draw this tile
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the game grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method used checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # A method that locks the tiles of a landed tetromino on the grid checking
   # if the game is over due to having any tile above the topmost grid row.
   # (This method returns True when the game is over and False otherwise.)
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the grid
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each tile (occupied cell) onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # return the value of the game_over flag
      self.merge_tiles()
      self.clear_full_rows()

      # Mevcut tetromino'yu sonraki tetromino ile değiştir
      if self.next_tetromino is not None:
          self.current_tetromino = self.next_tetromino
          self.next_tetromino = None
 
      return self.game_over
   def has_empty_cells(self):
    for row in range(self.grid_height):
        for col in range(self.grid_width):
            if self.tile_matrix[row][col] is None:
                return True
    return False
   def check_win_condition(self):
    # Grid'deki tüm hücreleri kontrol et
    for row in range(self.grid_height):
        for col in range(self.grid_width):
            # Eğer bir tile varsa ve değeri 2048 veya üstüyse
            if (self.tile_matrix[row][col] is not None and 
                self.tile_matrix[row][col].number >= 2048):
                return True
    return False