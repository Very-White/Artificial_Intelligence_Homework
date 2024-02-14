import pygame


class Chess(pygame.sprite.Sprite):
    """
    棋子类
    """

    def __init__(self, screen, chess_name, row, col):
        super().__init__()
        self.screen = screen
        # self.name = chess_name
        self.team = chess_name[0]  # 队伍（红方 r、黑方b）
        self.name = chess_name[2]  # 名字（炮p、马m等）
        self.image = pygame.image.load("images/" + chess_name + ".png")
        self.rect = self.image.get_rect()  # 得到rect参数
        self.rect.topleft = (50 + col * 57, 50 + row * 57)  # 设置图片显示的位置
        self.row, self.col = row, col

    def show(self):
        self.screen.blit(self.image, self.rect)  # 显示棋子

    @staticmethod
    def get_clicked_chess(player, chessboard):
        """
        获取被点击的棋子
        """
        for chess in chessboard.get_chess():
            if pygame.mouse.get_pressed()[0] and chess.rect.collidepoint(pygame.mouse.get_pos()):
                """
                        pygame.mouse.get_pressed()[0]：这是检查鼠标左键是否被按下。pygame.mouse.get_pressed()返回一个包含三个布尔值的元组，
                    分别表示左、中、右键是否被按下。[0]获取这个元组的第一个值，即左键的状态。
                        chess.rect.collidepoint(pygame.mouse.get_pos())：这是检查当前遍历到的棋子（chess）的矩形区域是否与鼠标的当前位置碰撞。
                    如果鼠标在棋子的矩形区域内，这个方法将返回True。
                """
                if player == chess.team:  # 这行代码检查当前遍历到的棋子（chess）的队伍（team）是否与传入的玩家（player）相同。这意味着我们只关心与玩家同队的棋子是否被点击。
                    print(chess.name + "被点击了")
                    return chess

    def update_position(self, new_row, new_col):
        """
        更新要显示的图片的坐标
        """
        self.row = new_row
        self.col = new_col
        self.rect.topleft = (50 + new_col * 57, 50 + new_row * 57)
