import time
import pygame
import numpy as np

#Color Constants
COLOR_BACKGROUND = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE = (217, 0, 255)
COLOR_ALIVE = (255, 255, 255)

def main():
    #initialize game field
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    updateLife(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    #Uses input to start/stop game and turn cells alive
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    updateLife(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                updateLife(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = updateLife(screen, cells, 10, withProgress=True)
            pygame.display.update()

        time.sleep(0.001)

#Updates cell colors to correspond with the rules of life
def updateLife(screen, cells, size, withProgress=False):
    #Grid starts with no life
    updatedCells = np.zeros((cells.shape[0], cells.shape[1]))

    #Iterate through all cells to determine life
    for row, col in np.ndindex(cells.shape):
        #Determine number of alive neighbor cells for each cell
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        
        #Determine if cell is displayed as alive or dead
        if cells[row, col] == 0:
            color = COLOR_BACKGROUND
        else:
            color = COLOR_ALIVE

        #Apply game rules to each cell
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if withProgress:
                    color = COLOR_DIE
            elif 2 <= alive <= 3:
                updatedCells[row, col] = 1
                if withProgress:
                    color = COLOR_ALIVE
        else: 
            if alive == 3:
                updatedCells[row, col] = 1
                if withProgress:
                    color = COLOR_ALIVE

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    
    return updatedCells

if __name__ == '__main__':
    main()