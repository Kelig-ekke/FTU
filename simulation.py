import json
import pygame
import math
from planet import Planet

class SolarSystemSimulation:
    def __init__(self, settings_file='settings.json'):
        self.load_settings(settings_file)
        self.planets = []
        self.time_scale = 1.0
        self.zoom_scale = 1.0
        self.scale = 1.0
        self.base_sun_radius = self.sun_radius  # Сохраняем базовый радиус Солнца
        self.is_paused = False
        self.camera_x = self.window_width // 2
        self.camera_y = self.window_height // 2
        self.follow_planet = None
        
        # Для плавного масштабирования
        self.target_scale = 1.0
        self.scale_speed = 0.05
        
        self.setup_planets()
        self.setup_ui()
    
    def load_settings(self, settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        
        self.window_width = settings['window_width']
        self.window_height = settings['window_height']
        self.bg_color = tuple(settings['background_color'])
        self.sun_radius = settings['sun_radius']
        self.planet_data = settings['planets']
    
    def setup_planets(self):
        # Настраиваем относительные размеры планет (для лучшей визуализации)
        # В реальности соотношения размеров гораздо больше
        planet_sizes = {
            "Mercury": 4,
            "Venus": 10,
            "Earth": 11,
            "Mars": 6,
            "Jupiter": 24,
            "Saturn": 20,
            "Uranus": 18,
            "Neptune": 17
        }
        
        # Настраиваем относительные скорости (чем дальше - тем медленнее)
        for data in self.planet_data:
            # Корректируем размер планеты
            if data['name'] in planet_sizes:
                data['size'] = planet_sizes[data['name']]
            
            # Делаем скорости более реалистичными (закон Кеплера)
            # Скорость обратно пропорциональна квадратному корню из радиуса орбиты
            base_speed = 0.01
            kepler_speed = base_speed * math.sqrt(170 / data['orbit_radius'])  # 170 - радиус Земли
            
            planet = Planet(
                name=data['name'],
                orbit_radius=data['orbit_radius'],
                orbit_speed=kepler_speed,
                size=data['size'],
                color=tuple(data['color']),
                show_orbit=True
            )
            
            # Начальные углы для красивого расположения
            planet.angle = len(self.planets) * (2 * math.pi / len(self.planet_data))
            
            self.planets.append(planet)
    
    def setup_ui(self):
        # Создаем поверхности для кнопок
        self.buttons = {
            'start_pause': {'rect': pygame.Rect(10, 10, 100, 40), 'text': 'Pause'},
            'slow_down': {'rect': pygame.Rect(120, 10, 40, 40), 'text': '<<'},
            'speed_up': {'rect': pygame.Rect(170, 10, 40, 40), 'text': '>>'},
            'zoom_in': {'rect': pygame.Rect(220, 10, 40, 40), 'text': '+'},
            'zoom_out': {'rect': pygame.Rect(270, 10, 40, 40), 'text': '-'},
            'reset': {'rect': pygame.Rect(320, 10, 100, 40), 'text': 'Reset View'},
            'follow_earth': {'rect': pygame.Rect(430, 10, 100, 40), 'text': 'Follow Earth'}
        }
    
    def update(self, delta_time):
        # Плавное масштабирование
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * self.scale_speed
        else:
            self.scale = self.target_scale
        
        if not self.is_paused:
            for planet in self.planets:
                planet.update(delta_time, self.time_scale)
        
        # Если следим за планетой, центрируем камеру на ней (работает и при паузе)
        if self.follow_planet is not None:
            planet = self.planets[self.follow_planet]
            x, y = planet.get_position()
            self.camera_x = self.window_width // 2 - x * self.scale
            self.camera_y = self.window_height // 2 - y * self.scale
    
    def draw(self, screen):
        # Очищаем экран
        screen.fill(self.bg_color)
        
        # Рисуем звезды на фоне
        self.draw_stars(screen)
        
        # Рисуем орбиты планет
        for planet in self.planets:
            planet.draw(screen, self.camera_x, self.camera_y, self.scale)
        
        # Рисуем Солнце с масштабированием
        self.draw_sun(screen)
        
        # Отображаем информацию
        self.draw_info(screen)
        
        # Рисуем кнопки
        self.draw_buttons(screen)
    
    def draw_stars(self, screen):
        # Рисуем звездочки на фоне
        import random
        random.seed(42)  # Для постоянного расположения звезд
        
        for i in range(100):
            x = random.randint(0, self.window_width)
            y = random.randint(0, self.window_height)
            brightness = random.randint(100, 255)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, (brightness, brightness, brightness), 
                             (x, y), size)
    
    def draw_sun(self, screen):
        # Солнце находится в начале координат (0, 0)
        sun_x = self.camera_x
        sun_y = self.camera_y
        
        # Масштабируем Солнце вместе с общим масштабом
        current_sun_radius = self.base_sun_radius * self.scale
        
        # Рисуем свечение Солнца
        for i in range(3, 0, -1):
            glow_radius = current_sun_radius * (1 + i * 0.1)
            alpha = 50 - i * 10
            glow_surface = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, 
                             (255, 255, 100, alpha), 
                             (int(glow_radius), int(glow_radius)), 
                             int(glow_radius))
            screen.blit(glow_surface, 
                       (sun_x - glow_radius, sun_y - glow_radius))
        
        # Рисуем само Солнце
        pygame.draw.circle(screen, (255, 255, 0), 
                          (int(sun_x), int(sun_y)), 
                          int(current_sun_radius))
        
        # Добавляем текстуру Солнцу (пятна)
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            distance = current_sun_radius * 0.7
            spot_x = sun_x + math.cos(angle) * distance
            spot_y = sun_y + math.sin(angle) * distance
            spot_radius = current_sun_radius * 0.1
            pygame.draw.circle(screen, (255, 200, 0), 
                             (int(spot_x), int(spot_y)), 
                             int(spot_radius))
    
    def draw_info(self, screen):
        font = pygame.font.Font(None, 24)
        
        # Информация о скорости и масштабе
        speed_text = f"Speed: {self.time_scale:.1f}x"
        scale_text = f"Scale: {self.scale:.2f}"
        status_text = "Paused" if self.is_paused else "Running"
        
        # Информация о слежении
        follow_text = "Free view"
        if self.follow_planet is not None:
            follow_text = f"Following: {self.planets[self.follow_planet].name}"
        
        texts = [
            speed_text,
            scale_text,
            status_text,
            follow_text
        ]
        
        for i, text in enumerate(texts):
            rendered = font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (10, 60 + i * 30))
    
    def draw_buttons(self, screen):
        font = pygame.font.Font(None, 28)
        
        for name, button in self.buttons.items():
            # Рисуем прямоугольник кнопки
            pygame.draw.rect(screen, (50, 50, 100), button['rect'])
            pygame.draw.rect(screen, (100, 100, 200), button['rect'], 2)
            
            # Рисуем текст кнопки
            text = font.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
    
    def handle_click(self, pos):
        for name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                self.handle_button_click(name)
                return True
        return False
    
    def handle_button_click(self, button_name):
        if button_name == 'start_pause':
            self.is_paused = not self.is_paused
            self.buttons['start_pause']['text'] = 'Start' if self.is_paused else 'Pause'
        
        elif button_name == 'slow_down':
            self.change_speed(up=False)
        
        elif button_name == 'speed_up':
            self.change_speed(up=True)
        
        elif button_name == 'zoom_in':
            self.change_zoom(plus=True)
        
        elif button_name == 'zoom_out':
            self.change_zoom(plus=False)
        
        elif button_name == 'reset':
            self.camera_x = self.window_width // 2
            self.camera_y = self.window_height // 2
            self.target_scale = 1.0
            self.follow_planet = None
        
        elif button_name == 'follow_earth':
            # Ищем Землю
            earth_index = None
            for i, planet in enumerate(self.planets):
                if planet.name == "Earth":
                    earth_index = i
                    break
            
            if earth_index is not None:
                if self.follow_planet == earth_index:
                    # Если уже следим за Землей, отключаем фокус
                    self.camera_x = self.window_width // 2
                    self.camera_y = self.window_height // 2
                    self.target_scale = 1.0
                    self.follow_planet = None
                else:
                    # Иначе включаем фокус на Землю
                    self.follow_planet = earth_index
                    self.target_scale = 2.0

    
    def handle_keypress(self, key):
        # Управление с клавиатуры
        if key == pygame.K_SPACE:
            self.is_paused = not self.is_paused
            self.buttons['start_pause']['text'] = 'Start' if self.is_paused else 'Pause'
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.change_zoom(plus=True)
        elif key == pygame.K_MINUS:
            self.change_zoom(plus=False)
        elif key == pygame.K_UP:
            self.change_speed(up=True)
        elif key == pygame.K_DOWN:
            self.change_speed(up=False)
        elif key == pygame.K_r:
            self.camera_x = self.window_width // 2
            self.camera_y = self.window_height // 2
            self.target_scale = 1.0
            self.follow_planet = None
        elif key == pygame.K_e:
            # Следить за Землей или отключить фокус при повторном нажатии
            earth_index = None
            for i, planet in enumerate(self.planets):
                if planet.name == "Earth":
                    earth_index = i
                    break
            
            if earth_index is not None:
                if self.follow_planet == earth_index:
                    # Если уже следим за Землей, отключаем фокус
                    self.camera_x = self.window_width // 2
                    self.camera_y = self.window_height // 2
                    self.target_scale = 1.0
                    self.follow_planet = None
                else:
                    # Иначе включаем фокус на Землю
                    self.follow_planet = earth_index
                    self.target_scale = 2.0


    def change_speed(self, up=True):
        speed_levels = [0.1, 0.5, 1, 2, 5, 10, 20, 30, 40, 50]
        
        if up:
            # Находим следующую скорость в списке
            for speed in speed_levels:
                if speed > self.time_scale:
                    self.time_scale = speed
                    return
            # Если уже на максимуме, остаемся на месте
            if self.time_scale < speed_levels[-1]:
                self.time_scale = speed_levels[-1]
        else:
            # Находим предыдущую скорость в списке
            for speed in reversed(speed_levels):
                if speed < self.time_scale:
                    self.time_scale = speed
                    return
            # Если уже на минимуме, остаемся на месте
            if self.time_scale > speed_levels[0]:
                self.time_scale = speed_levels[0]

    def change_zoom(self, plus=True):
        zoom_levels = [0.5, 1, 2, 5, 8]

        if plus:
            for zoom in zoom_levels:
                if zoom > self.target_scale:
                    self.target_scale = zoom
                    return
            # Если уже на максимуме, остаемся на месте
            if self.target_scale < zoom_levels[-1]:
                self.target_scale = zoom_levels[-1]
        else:
            for zoom in reversed(zoom_levels):
                if zoom < self.target_scale:
                    self.target_scale = zoom
                    return
            # Если уже на минимуме, остаемся на месте
            if self.target_scale > zoom_levels[0]:
                self.target_scale = zoom_levels[0]