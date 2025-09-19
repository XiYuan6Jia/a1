import pygame as pg

class Game:
    def __init__(self):
        # 游戏配置常量
        self.WINDOW_SIZE = (1280, 720)
        self.TITLE = "Tank Trouble"
        self.FPS = 30
        
        # 初始化pygame
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.WINDOW_SIZE)
        pg.display.set_caption(self.TITLE)
        
        # 游戏状态
        self.running = True
    
    def handle_events(self):
        """处理所有游戏事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    def update(self):
        """更新游戏逻辑"""
        pass
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill((255, 255, 255))
        pg.display.update()
    
    def run(self):
        """主游戏循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pg.quit()
        print("游戏已退出")

if __name__ == "__main__":
    game = Game()
    game.run()
