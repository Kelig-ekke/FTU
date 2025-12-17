import math
import pygame

class Planet:
    def __init__(self, name, orbit_radius, orbit_speed, size, color, show_orbit=False):
        self.name = name
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.size = size
        self.color = color
        self.angle = 0
        self.show_orbit = show_orbit
        self.orbit_points = []
        
    def update(self, delta_time, time_scale):
        # Обновляем угол вращения
        self.angle += self.orbit_speed * delta_time * time_scale
        
        # Сохраняем точки орбиты для отрисовки
        if self.show_orbit:
            x = math.cos(self.angle) * self.orbit_radius
            y = math.sin(self.angle) * self.orbit_radius
            self.orbit_points.append((x, y))
            if len(self.orbit_points) > 1000:  # Ограничиваем длину следа
                self.orbit_points.pop(0)
    
    def get_position(self):
        # Вычисляем координаты планеты
        x = math.cos(self.angle) * self.orbit_radius
        y = math.sin(self.angle) * self.orbit_radius
        return x, y
    
    def draw(self, screen, center_x, center_y, scale):
        # Рисуем орбиту (если включено)
        if self.show_orbit and len(self.orbit_points) > 1:
            points = []
            for x, y in self.orbit_points:
                screen_x = center_x + x * scale
                screen_y = center_y + y * scale
                points.append((screen_x, screen_y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, (100, 100, 100), False, points, 1)
        
        # Рисуем планету
        x, y = self.get_position()
        screen_x = center_x + x * scale
        screen_y = center_y + y * scale
        
        pygame.draw.circle(screen, self.color, 
                          (int(screen_x), int(screen_y)), 
                          max(2, int(self.size * scale)))
        
        # Отображаем имя планеты
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (screen_x + 10, screen_y - 10))