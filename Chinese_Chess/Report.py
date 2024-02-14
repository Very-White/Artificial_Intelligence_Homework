import pygame

pygame.init()


class Report():
    """
    主要有三个成员变量：存储历史的message，存储游戏屏幕的screen，还有存储图像的image(图像参数的rect)
    """
    __title_font = pygame.font.SysFont('Futura', 45, bold=True)
    __text_font = pygame.font.SysFont('Futura', 30, bold=False)

    def __init__(self, screen, message: list = []):
        self.screen = screen
        self.messages = message  # 用一个列表来存储消息，默认初始化为空
        self.image = pygame.image.load('images/rep.webp')
        self.image = pygame.transform.scale(self.image, (800, 900))
        self.rect = self.image.get_rect()
        self.rect.topleft = (750, 0)

    def append(self, message: str):
        self.messages.append(message)

    def pop(self):
        return self.messages.pop()

    def show(self):
        self.__image_show()
        self.__message_show()

    def clear(self):
        self.messages.clear()
    def __image_show(self):
        self.screen.blit(self.image, self.rect.topleft)

    def __message_show(self):
        title_pos = (self.rect.topleft[0] + 25, self.rect.topleft[1] + 25)
        self.screen.blit(self.__title_font.render('history', True, [0, 0, 0]), title_pos)
        message_length = len(self.messages)
        first_message_pos = title_pos[1] + 75
        for line in self.messages[max(message_length - 9, 0):message_length]:
            self.screen.blit(self.__text_font.render(line, True, [0, 0, 0]), [title_pos[0] + 50, first_message_pos])
            first_message_pos += 75
