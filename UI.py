from pygame import Rect, draw
import pygame
pygame.init()

FONT = pygame.font.Font(None, 20)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:
    def __init__(self, window_size, pixel_size, text, n):
        self.pos = window_size[0] * pixel_size + 200, 40 * n
        self.rect = Rect(self.pos[0], self.pos[1], 80, 20)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, window_size, pixel_size, text, n):
        self.pos = window_size[0] * pixel_size + 30, 40 * n
        self.rect = Rect(self.pos[0], self.pos[1], 150, 20)

        font = pygame.font.Font(None, 20)
        self.text = font.render(text, True, (0, 0, 0))

    def drawing(self, surface):
        draw.rect(surface, (200, 200, 200), self.rect)
        surface.blit(self.text, self.rect)
