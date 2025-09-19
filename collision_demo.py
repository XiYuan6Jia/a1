import pygame as pg
import random
import math
import maps
from sprites import tank, bullet, wall

class CollisionDemo:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.target_fps = 30
        
        # 创建精灵组
        self.tank = tank()
        self.tank_group = pg.sprite.Group(self.tank)
        self.bullet_group = pg.sprite.Group()
        
        # 创建墙壁
        self.wall_group = pg.sprite.Group()
        for wall_info in maps.map1:
            self.wall_group.add(wall(wall_info['pos'], wall_info['size']))
        
        # 碰撞检测调试标志
        self.debug_collision = True
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                if event.key == pg.K_SPACE:  # 发射子弹
                    barrel_length = 35
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
        # 坦克与墙壁碰撞
        tank_wall_collisions = pg.sprite.spritecollide(
            self.tank, self.wall_group, False)
        if tank_wall_collisions and self.debug_collision:
            print("坦克撞墙!")
        
        # 子弹与墙壁碰撞
        bullet_wall_collisions = pg.sprite.groupcollide(
            self.bullet_group, self.wall_group, True, False)
        if bullet_wall_collisions and self.debug_collision:
            print("子弹击中墙壁!")
        
        # 子弹与坦克碰撞
        bullet_tank_collisions = pg.sprite.spritecollide(
            self.tank, self.bullet_group, True)
        if bullet_tank_collisions and self.debug_collision:
            print("坦克被子弹击中!")
    
    def update(self):
        # 移除屏幕外的子弹
        for b in self.bullet_group:
            if (b.rect.right < 0 or b.rect.left > 1280 or 
                b.rect.bottom < 0 or b.rect.top > 720):
                self.bullet_group.remove(b)
        
        self.bullet_group.update()
    
    def render(self):
        self.window.fill((255, 255, 255))
        self.wall_group.draw(self.window)
        self.tank_group.draw(self.window)
        self.bullet_group.draw(self.window)
        pg.display.update()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.check_collisions()
            self.update()
            self.render()
            self.clock.tick(self.target_fps)
        
        pg.quit()

if __name__ == "__main__":
    demo = CollisionDemo()
    demo.run()
