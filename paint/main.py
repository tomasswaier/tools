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

    def width_picker(self):

        pen_width_picker_dimentions = [
            70,
            160,
        ]
        self.pen_width_picker_border = pygame.Surface(
            (pen_width_picker_dimentions[0], pen_width_picker_dimentions[1])
        )
        self.pen_width_picker_inner = pygame.Surface(
            (pen_width_picker_dimentions[0] - 2, pen_width_picker_dimentions[1] - 2)
        )
        self.pen_width_picker_inner.fill(BACKGROUND_PURPLE_DARK)

        self.screen.blit(self.pen_width_picker_border, (4, 210))
        self.screen.blit(self.pen_width_picker_inner, (5, 211))
        pen_width_picker_cell_dimentions = [
            pen_width_picker_dimentions[0] / 2,
            pen_width_picker_dimentions[1] / 4,
        ]
        self.width_picker_cells = []
        # todo : finish adding shit
        for i in range(4):
            pen_width_picker_cell_1 = pygame.Surface(
                (
                    pen_width_picker_cell_dimentions[0],
                    pen_width_picker_cell_dimentions[1],
                )
            )
            self.width_picker_cells.append(
                pen_width_picker_cell_1.get_rect(
                    topleft=(5, 220 + pen_width_picker_cell_dimentions[1] * i)
                )
            )

            pen_width_picker_cell_2 = pygame.Surface(
                (
                    pen_width_picker_cell_dimentions[0],
                    pen_width_picker_cell_dimentions[1],
                )
            )
            self.width_picker_cells.append(
                pen_width_picker_cell_2.get_rect(
                    topleft=(
                        5 + pen_width_picker_cell_dimentions[0],
                        220 + pen_width_picker_cell_dimentions[1] * i,
                    )
                )
            )

    def color_pallet(self):
        self.collor_pallet_array = []
        for i in range(int(len(COLOR_PALLET) / 2)):
            color1 = pygame.Surface((20, 20))
            color1.fill(pygame.Color(COLOR_PALLET[i]))
            self.collor_pallet_array.append(
                [
                    color1.get_rect(topleft=(80 + (40 * i), window_height - 60)),
                    COLOR_PALLET[i],
                ]
            )
            self.screen.blit(color1, (80 + (40 * i), window_height - 60))
            color2 = pygame.Surface((20, 20))
            color2.fill(pygame.Color(COLOR_PALLET[i + 1]))
            self.collor_pallet_array.append(
                [
                    color2.get_rect(topleft=(80 + (40 * i), window_height - 20)),
                    COLOR_PALLET[i + 1],
                ]
            )
            self.screen.blit(color2, (80 + (40 * i), window_height - 20))

    def create_interface(self):

        font = pygame.font.SysFont(None, 24)
        self.surface = pygame.Surface(
            (window_width * 260 / 300, window_height * 170 / 220)
        )
        self.screen.blit(self.surface, (window_width * 40 / 300, window_height * 0.06))

        self.screen.fill(BACKGROUND_PURPLE)
        self.surface_border = pygame.Surface(
            ((window_width * 260 / 300) + 4, (window_height * 170 / 220) + 4)
        )
        self.surface_border.fill(BORDER_BLUE)
        self.screen.blit(
            self.surface_border,
            ((window_width * 40 / 300) - 2, (window_height * 0.06) - 2),
        )
        # add width picker
        self.width_picker()
        self.color_pallet()

        # dimentions for the width picker thingies

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
                        self.pen_color = BLACK
                    if self.eraser_icon_rect.collidepoint(pygame.mouse.get_pos()):
                        self.pen_color = WHITE
                    for i in range(8):  # None

                        if self.width_picker_cells[i].collidepoint(
                            pygame.mouse.get_pos()
                        ):
                            self.pen_width = (i + 1) ** 2
                    for i in range(int(len(COLOR_PALLET))):

                        if self.collor_pallet_array[i][0].collidepoint(
                            pygame.mouse.get_pos()
                        ):
                            self.pen_color = pygame.Color(
                                self.collor_pallet_array[i][1]
                            )
                    # Check for collision with the second button
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
    COLOR_PALLET = [
        "#ffe9df",
        "#3c3772",
        "#2d96c5",
        "#355af5",
        "#4adeb5",
        "#9985f3",
        "#e2b267",
        "#2f62d4",
        "#e94cb6",
        "#de5ce8",
    ]
    window_height = 950
    window_width = 1600
    color_picker = []
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND_PURPLE_DARK = pygame.Color("#bd91da")
    BACKGROUND_PURPLE = pygame.Color("#cea2eb")
    BORDER_BLUE = pygame.Color("#5b61f9")
    painter = Paint()
    painter.start_painter()
