import pygame, sys, os
from pygame.locals import *


class Paint:
    def __init__(self, image=None):
        pygame.init()

        self.screen = pygame.display.set_mode((window_width, window_height))
        self.pen_color = BLACK
        self.pen_width = 1

        # Game loop
        self.image = image
        if self.image:
            self.image = self.image.convert()
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
        width = 1
        for i in range(4):
            pen_width_picker_cell_1 = pygame.Surface(
                (
                    pen_width_picker_cell_dimentions[0],
                    pen_width_picker_cell_dimentions[1],
                )
            )
            pen_width_picker_cell_1_size = pygame.Surface((width, width))
            pen_width_picker_cell_1_size.fill(BLACK)
            self.screen.blit(
                pen_width_picker_cell_1_size,
                (10, 229 + pen_width_picker_cell_dimentions[1] * i),
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
            width += 3
            pen_width_picker_cell_2_size = pygame.Surface((width, width))
            pen_width_picker_cell_2_size.fill(BLACK)
            self.screen.blit(
                pen_width_picker_cell_2_size,
                (
                    10 + pen_width_picker_cell_dimentions[0],
                    229 + pen_width_picker_cell_dimentions[1] * i,
                ),
            )
            width += 3
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
                    color1.get_rect(topleft=(80 + (40 * i), window_height - 65)),
                    COLOR_PALLET[i],
                ]
            )
            self.screen.blit(color1, (80 + (40 * i), window_height - 65))
            color2 = pygame.Surface((20, 20))
            color2.fill(pygame.Color(COLOR_PALLET[i + 1]))
            self.collor_pallet_array.append(
                [
                    color2.get_rect(topleft=(80 + (40 * i), window_height - 25)),
                    COLOR_PALLET[i + 1],
                ]
            )
            self.screen.blit(color2, (80 + (40 * i), window_height - 25))

    def create_interface(self):
        self.surface_position = [80, 30]
        self.surface_shape = [520, 340]  # Default surface shape

        # Adjust surface size if there's an image
        if self.image:
            self.surface_shape = [self.image.get_width(), self.image.get_height()]

        self.surface = pygame.Surface((self.surface_shape[0], self.surface_shape[1]))
        self.surface = self.surface.convert()

        if self.image:
            self.surface.blit(self.image, (0, 0))

        self.screen.fill(BACKGROUND_PURPLE)

        # Border around the drawing surface
        self.surface_border = pygame.Surface(
            (self.surface_shape[0] + 4, self.surface_shape[1] + 4)
        )
        self.surface_border.fill(BORDER_BLUE)
        self.screen.blit(
            self.surface_border,
            (self.surface_position[0] - 2, self.surface_position[1] - 2),
        )

        # Now blit the drawing surface (either the image or an empty surface)
        self.screen.blit(
            self.surface, (self.surface_position[0], self.surface_position[1])
        )

        self.width_picker()
        self.color_pallet()

        # Draw the pen and eraser icons
        self.pen_icon = pygame.image.load("images/pen.png").convert()
        self.pen_icon = pygame.transform.scale(self.pen_icon, (30, 30))
        self.pen_icon_rect = self.pen_icon.get_rect(topleft=(10, 30))
        self.screen.blit(self.pen_icon, self.pen_icon_rect.topleft)

        self.eraser_icon = pygame.image.load("images/eraser.png").convert()
        self.eraser_icon = pygame.transform.scale(self.eraser_icon, (30, 30))
        self.eraser_icon_rect = self.eraser_icon.get_rect(topleft=(40, 30))
        self.screen.blit(self.eraser_icon, self.eraser_icon_rect.topleft)

        font = pygame.font.SysFont(None, 24)
        label = font.render("textill", 1, BLACK)
        self.screen.blit(label, (10, 5))

        pygame.display.flip()

    def start_painter(self):
        clock = pygame.time.Clock()  # Determine FPS (frames-per-second)
        crashed = False
        input_image = None
        surface_offset_x = 0
        surface_offset_y = 0
        surface_offset_x = self.surface_position[0]
        surface_offset_y = self.surface_position[1]

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
                pygame.image.save(self.surface, "image.png")
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
    window_height = 450
    window_width = 600
    image = None
    if len(sys.argv) > 1 and sys.argv[1]:
        # fix this
        image = pygame.image.load(os.path.abspath(sys.argv[1]))
        window_height = image.get_height() + 110  # 30+height+80 ( top gap + bottom gap
        window_width = image.get_width() + 80  # 80+width
    color_picker = []
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND_PURPLE_DARK = pygame.Color("#bd91da")
    BACKGROUND_PURPLE = pygame.Color("#cea2eb")
    BORDER_BLUE = pygame.Color("#5b61f9")
    painter = Paint(image)
    painter.start_painter()
