
import pygame
import sys
import random


pygame.init()
ANCHO, ALTO = 800, 500
COLOR_FONDO = (25, 25, 25)
FPS = 60


class Jugador:
    def __init__(self, x, y, color=(0, 255, 0), velocidad=6):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.color = color
        self.velocidad = velocidad

    def mover(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        
        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTO - self.rect.height))

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)


class Obstaculo:
    def __init__(self, x, y, ancho, alto, color=(255, 80, 80)):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        
        self.vel_x = random.choice([-4, -3, -2, 2, 3, 4])
        self.vel_y = random.choice([-4, -3, -2, 2, 3, 4])

    def mover(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.vel_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.vel_y *= -1

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)



def menu_principal(pantalla, fuente):
    while True:
        pantalla.fill((0, 0, 0))
        titulo = fuente.render("ESQUIVA LOS OBSTÁCULOS ", True, (255, 255, 255))
        jugar = fuente.render("Presiona ENTER para Jugar", True, (0, 255, 0))
        salir = fuente.render("Presiona ESC para Salir", True, (255, 0, 0))

        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))
        pantalla.blit(jugar, (ANCHO // 2 - jugar.get_width() // 2, 230))
        pantalla.blit(salir, (ANCHO // 2 - salir.get_width() // 2, 270))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def pantalla_perdida(pantalla, fuente, puntaje):
    while True:
        pantalla.fill((0, 0, 0))
        texto = fuente.render("💀 ¡HAS PERDIDO! 💀", True, (255, 0, 0))
        score = fuente.render(f"Tiempo sobrevivido: {puntaje:.2f} segundos", True, (255, 255, 255))
        reiniciar = fuente.render("Presiona ENTER para volver a iniciar", True, (0, 255, 0))
        salir = fuente.render("Presiona ESC para salir", True, (255, 255, 255))

        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 150))
        pantalla.blit(score, (ANCHO // 2 - score.get_width() // 2, 200))
        pantalla.blit(reiniciar, (ANCHO // 2 - reiniciar.get_width() // 2, 250))
        pantalla.blit(salir, (ANCHO // 2 - salir.get_width() // 2, 290))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True  # Reinicia
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def bucle_juego(pantalla, fuente):
    jugador = Jugador(ANCHO // 2, ALTO - 50)
   
    obstaculos = [Obstaculo(random.randint(0, ANCHO - 50),
                             random.randint(0, ALTO - 50),
                             random.randint(30, 60),
                             random.randint(20, 40))
                  for _ in range(8)]

    reloj = pygame.time.Clock()
    inicio = pygame.time.get_ticks()  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        jugador.mover(keys)

      
        for obs in obstaculos:
            obs.mover()

       
        for obs in obstaculos:
            if jugador.rect.colliderect(obs.rect):
               
                tiempo_total = (pygame.time.get_ticks() - inicio) / 1000
                return pantalla_perdida(pantalla, fuente, tiempo_total)

       
        pantalla.fill(COLOR_FONDO)
        jugador.dibujar(pantalla)
        for obs in obstaculos:
            obs.dibujar(pantalla)

        
        tiempo_actual = (pygame.time.get_ticks() - inicio) / 1000
        texto_tiempo = fuente.render(f"Tiempo: {tiempo_actual:.2f}s", True, (255, 255, 255))
        pantalla.blit(texto_tiempo, (10, 10))

        pygame.display.flip()
        reloj.tick(FPS)


 
def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Modo Difícil - Esquiva los Obstáculos")
    fuente = pygame.font.SysFont("Arial", 24)

    while True:
        if menu_principal(pantalla, fuente):
            bucle_juego(pantalla, fuente)


if __name__ == "__main__":
    main()