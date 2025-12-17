import pygame
import sys
from simulation import SolarSystemSimulation

def main():
    # Инициализация PyGame
    pygame.init()
    
    # Создание симуляции
    simulation = SolarSystemSimulation()
    
    # Создание окна
    screen = pygame.display.set_mode((simulation.window_width, simulation.window_height))
    pygame.display.set_caption("Solar System Simulator")
    
    # Часы для контроля FPS
    clock = pygame.time.Clock()
    
    # Основной цикл
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Время в секундах
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    simulation.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                simulation.handle_keypress(event.key)
            elif event.type == pygame.MOUSEWHEEL:
                # Масштабирование колесиком мыши
                if event.y > 0:
                    simulation.scale = min(simulation.scale * 1.1, 5.0)
                else:
                    simulation.scale = max(simulation.scale / 1.1, 0.1)
        
        # Обновление симуляции
        simulation.update(delta_time)
        
        # Отрисовка
        simulation.draw(screen)
        
        # Обновление экрана
        pygame.display.flip()
    
    # Завершение работы
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()