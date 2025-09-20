import pygame as pg
import math
import maps
from sprites import tank, bullet, wall

class Game:
    def __init__(self):
        # 游戏配置常量
        self.WINDOW_SIZE = (1280, 720)
        self.TITLE = "Tank Trouble"
        self.FPS = 30
        
        # 初始化pygame
        pg.init()
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode(self.WINDOW_SIZE)
        pg.display.set_caption(self.TITLE)
        
        # 创建精灵组
        self.tank = tank()
        self.tank_group = pg.sprite.Group(self.tank)
        self.bullet_group = pg.sprite.Group()

        # 创建墙壁
        self.wall_group = pg.sprite.Group()
        for wall_info in maps.map1:
            self.wall_group.add(wall(wall_info['pos'], wall_info['size'], wall_info['type']))
            
        # 碰撞检测调试标志
        self.debug_collision = True            
    
    def handle_events(self):
        """处理所有游戏事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                if event.key == pg.K_SPACE:  # 发射子弹
                    if self.tank.alive:
                        barrel_length = 40
                        rad_angle = math.radians(self.tank.angle)
                        bullet_start_pos = (
                            self.tank.rect.centerx + barrel_length * math.cos(rad_angle),
                            self.tank.rect.centery - barrel_length * math.sin(rad_angle)
                        )
                        self.bullet_group.add(bullet(bullet_start_pos, self.tank.angle))
        
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.tank.rotate(5)
        if keys[pg.K_d]:
            self.tank.rotate(-5)
        if keys[pg.K_w]:
            self.tank.move_forward(5)
        if keys[pg.K_s]:
            self.tank.move_backward(3)
        
        return True

    def check_collisions(self):
        '''碰撞检测和响应'''
        # 坦克与墙壁碰撞
        for tank in self.tank_group:
            for wall in self.wall_group:
                if pg.sprite.collide_mask(tank, wall):
                    if self.debug_collision:
                        print("坦克撞墙了!")
                    # 简单处理：将坦克移回上一位置
                    tank.rewind_move()

        # 子弹与墙壁碰撞
        for bullet in self.bullet_group:
            for wall in self.wall_group:
                if pg.sprite.collide_mask(bullet, wall):
                    if self.debug_collision:
                        print("子弹撞墙")
                        if wall.type == 'horizontal':
                            bullet.y_speed = -1 * bullet.y_speed
                        elif wall.type == 'vertical':
                            bullet.x_speed = -1 * bullet.x_speed
        
        # 子弹与坦克碰撞
        for bullet in self.bullet_group:
            for tank in self.tank_group:
                if pg.sprite.collide_mask(bullet, tank):
                    if self.debug_collision:
                        print("子弹击中坦克")
                        self.bullet_group.remove(bullet)
                        #self.tank_group.remove(tank)
                        tank.kill()

    def update(self):
        """更新游戏逻辑"""
        # 移除屏幕外的子弹
        for b in self.bullet_group:
            if (b.rect.right < 0 or b.rect.left > 1280 or 
                b.rect.bottom < 0 or b.rect.top > 720):
                self.bullet_group.remove(b)
        #子弹运动
        self.bullet_group.update()

        pass
    
    def render(self):
        """渲染游戏画面"""
        self.window.fill((255, 255, 255))
        self.wall_group.draw(self.window)
        self.tank_group.draw(self.window)
        self.bullet_group.draw(self.window)
        pg.display.update()
    
    def run(self):
        """主游戏循环"""
        running = True
        while running:
            running = self.handle_events()
            self.check_collisions()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pg.quit()
        print("游戏已退出")

if __name__ == "__main__":
    game = Game()
    game.run()
