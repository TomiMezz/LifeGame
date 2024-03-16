import pygame
import numpy as np
import time

pygame.init()

width, height = 500,500
screen = pygame.display.set_mode((height,width))

bg = 25, 25, 25
screen.fill(bg) 

nxC,nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

# Estados de las celdas. Vivas = 1, Muertas = 0
gameState = np.zeros((nxC, nyC))


# Automata palo:
gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1
gameState[5,6] = 1
gameState[6,7] = 1
gameState[6,8] = 1

gameState[15,3] = 1
gameState[15,4] = 1
gameState[15,5] = 1
gameState[15,6] = 1
gameState[15,7] = 1
gameState[15,9] = 1

# Control del estado del juego.
pauseExect = False

#Bucle de ejecucion-
while True:

    
 
    newGameState = np.copy(gameState)
    
    screen.fill(bg)
    time.sleep(0.1)
    
    # Registro de usos del teclado y el mouse.
    ev = pygame.event.get()
    
    for event in ev:
              
        # Detectamos si se presiona el mouse    
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX,celY] = 1
    
    for y in range(0,nxC):
        for x in range(0,nyC):
            
            if not pauseExect:
                
                
                # Calculamos el numero de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x)   % nxC, (y-1) % nyC] + \
                          gameState[(x+1) % nxC, (y-1) % nyC] + \
                          gameState[(x-1) % nxC, (y)   % nyC] + \
                          gameState[(x+1) % nxC, (y)   % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[(x)   % nxC, (y+1) % nyC] + \
                          gameState[(x+1) % nxC, (y+1) % nyC]
                          
                          
      # Regla 1: Unca celula muerta con exactamente 3 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1
                
      # Regla 2: Unca celula viva con menos de 2 o mas de 3 vecinas vivas, "muere"     
                elif   gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0
                
                # Creamos el poligono de cada celda a dibujar
                poly = [((x)*dimCW, y*dimCH ),
                        ((x+1)*dimCW, y*dimCH),
                        ((x+1)*dimCW, (y+1)*dimCH),
                        ((x)*dimCW, (y+1)*dimCH)]
                
                # Dibujamos la celda para cada par de X e Y
                if newGameState[x,y] == 0:
                    pygame.draw.polygon(screen,(128,128,128),poly,1)
                else:
                    pygame.draw.polygon(screen,(255,255,255),poly,0)
                
     # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)            
            
     # Actualizamos la pantalla
    pygame.display.flip()       
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            