import pygame
from pygame.locals import *


class Paint:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((window_width, window_height))
        self.pen_color = BLACK
        self.pen_width = 1

        # Game loop
        self.create_interface()

    def create_interface(self):
        font = pygame.font.SysFont(None, 24)

        self.surface = pygame.Surface(
            (window_width * 260 / 300, window_height * 170 / 220)
        )
        self.screen.fill(BACKGROUND_PURPLE)

        # dimentions for the width picker thingies
        pen_width_picker_dimentions = [
            window_width * 36 / 300,
            window_height * 80 / 220,
        ]
        self.pen_width_picker_border = pygame.Surface(
            (pen_width_picker_dimentions[0], pen_width_picker_dimentions[1])
        )
        self.pen_width_picker_inner = pygame.Surface(
            (pen_width_picker_dimentions[0] - 2, pen_width_picker_dimentions[1] - 2)
        )
        self.pen_width_picker_inner.fill(BACKGROUND_PURPLE_DARK)

        self.screen.blit(self.pen_width_picker_border, (4, window_height * 100 / 220))
        self.screen.blit(self.pen_width_picker_inner, (5, window_height * 101 / 220))
        pen_width_picker_cell_dimentions = [
            pen_width_picker_dimentions[0] / 2,
            pen_width_picker_dimentions[1] / 4,
        ]

        self.pen_width_picker_cell_1 = pygame.Surface(
            (pen_width_picker_cell_dimentions[0], pen_width_picker_cell_dimentions[1])
        )
        self.pen_width_picker_rect_1 = self.pen_width_picker_cell_1.get_rect(
            topleft=(5, window_height * 101 / 220)
        )
        self.screen.blit(self.pen_width_picker_cell_1, (5, window_height * 101 / 220))

        self.pen_width_picker_cell_2 = pygame.Surface(
            (pen_width_picker_cell_dimentions[0], pen_width_picker_cell_dimentions[1])
        )
        self.pen_width_picker_rect_2 = self.pen_width_picker_cell_2.get_rect(
            topleft=(5 + pen_width_picker_cell_dimentions[0], window_height * 101 / 220)
        )
        self.screen.blit(
            self.pen_width_picker_cell_2,
            (5 + pen_width_picker_cell_dimentions[0], window_height * 101 / 220),
        )

        # penicon and its border
        self.pen_icon = pygame.image.load("images/pen.png").convert()
        self.pen_icon = pygame.transform.scale(self.pen_icon, (30, 30))
        self.pen_icon_rect = self.pen_icon.get_rect(topleft=(10, 30))
        self.screen.blit(self.pen_icon, self.pen_icon_rect.topleft)

        self.eraser_icon = pygame.image.load("images/eraser.png").convert()
        self.eraser_icon = pygame.transform.scale(self.eraser_icon, (30, 30))
        self.eraser_icon_rect = self.eraser_icon.get_rect(topleft=(10 + 30, 30))
        self.screen.blit(self.eraser_icon, self.eraser_icon_rect.topleft)

        # fix this
        self.screen.blit(self.pen_icon, (10, 30))
        label = font.render("textill", 1, BLACK)

        self.screen.blit(label, (10, 5))

        self.surface.fill(WHITE)
        self.screen.blit(self.surface, (window_width * 40 / 300, window_height * 0.06))

        pygame.display.flip()

    def start_painter(self):
        clock = pygame.time.Clock()  # Determine FPS (frames-per-second)
        crashed = False
        surface_offset_x = window_width * 40 / 300
        surface_offset_y = window_height * 0.06

        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pen_icon_rect.collidepoint(pygame.mouse.get_pos()):
                        self.pen_color = BORDER_BLUE
                    if self.eraser_icon_rect.collidepoint(pygame.mouse.get_pos()):
                        self.pen_color = WHITE
                    if self.pen_width_picker_rect_1.collidepoint(
                        pygame.mouse.get_pos()
                    ):
                        self.pen_width = 1

                    # Check for collision with the second button
                    elif self.pen_width_picker_rect_2.collidepoint(
                        pygame.mouse.get_pos()
                    ):
                        self.pen_width = 2
                elif (
                    event.type == pygame.MOUSEMOTION
                ):  # fixing position for meow moew reasons
                    if event.buttons[0]:  # Left mouse button down.
                        # Adjust the mouse position relative to the surface
                        last = (
                            event.pos[0] - event.rel[0] - surface_offset_x,
                            event.pos[1] - event.rel[1] - surface_offset_y,
                        )
                        adjusted_pos = (
                            event.pos[0] - surface_offset_x,
                            event.pos[1] - surface_offset_y,
                        )

                        # Draw on the surface using adjusted coordinates
                        pygame.draw.line(
                            self.surface,
                            self.pen_color,
                            last,
                            adjusted_pos,
                            self.pen_width,
                        )

            # Blit the surface back to the screen after drawing
            self.screen.blit(self.surface, (surface_offset_x, surface_offset_y))

            # Check for key press to quit
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_q]:
                pygame.image.save(self.surface, "meow.png")
                pygame.quit()
            elif pressed[pygame.K_s]:
                self.pen_color = WHITE

            # Update the entire screen
            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    window_height = 500
    window_width = 600
    color_picker = []
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND_PURPLE_DARK = pygame.Color("#bd91da")
    BACKGROUND_PURPLE = pygame.Color("#cea2eb")
    BORDER_BLUE = pygame.Color("#5b61f9")
    painter = Paint()
    painter.start_painter()
