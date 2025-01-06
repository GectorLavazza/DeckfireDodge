from pygame.font import Font


class Text:
    def __init__(self, screen, pos, font_size, color='white', center_align=False, right_align=False):
        self.screen = screen
        self.font = Font('assets/fonts/PixelOperator8.ttf', font_size)
        self.pos = pos
        self.color = color
        self.center_align = center_align
        self.right_align = right_align

        self.render = self.font.render('', True, self.color)
        self.rect = self.render.get_rect()

        self.prev_message = ''

    def update(self, message):
        if self.prev_message != message:

            self.render = self.font.render(str(message), True, self.color)
            self.rect = self.render.get_rect()

        if self.center_align:
            pos = (self.pos[0] - self.render.get_width() // 2,
                   self.pos[1])
        elif self.right_align:
            pos = (self.pos[0] - self.render.get_width(),
                   self.pos[1])
        else:
            pos = self.pos

        self.screen.blit(self.render, pos)


class StaticText:
    def __init__(self, message, surface, pos, font_size, color='white', center_align=False, right_align=False, split=False):
        self.surface = surface
        self.font = Font('assets/fonts/PixelOperator8.ttf', font_size)
        self.pos = pos
        self.color = color
        self.center_align = center_align
        self.right_align = right_align

        if split:
            msg = str(message).split()

        self.render = self.font.render(str(message), True, self.color)
        self.rect = self.render.get_rect()

        if self.center_align:
            self.pos = (pos[0] - self.render.get_width() // 2,
                   pos[1])
        elif self.right_align:
            self.pos = (pos[0] - self.render.get_width(),
                   pos[1])
        else:
            self.pos = pos

        self.surface.blit(self.render, self.pos)
