import pygame as pg
import math
import json
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

        #加载字体
        try:
            self.font = pg.font.Font("C:/Windows/Fonts/simhei.ttf", 36)  # 使用黑体
        except:
            try:
                self.font = pg.font.Font("C:/Windows/Fonts/msyh.ttc", 36)  # 使用微软雅黑
            except:
                self.font = pg.font.SysFont("simsun", 36)  # 使用宋体
        
        # 创建精灵组
        self.tank = tank()
        self.tank_group = pg.sprite.Group(self.tank)
        self.bullet_group = pg.sprite.Group()
        self.tank.alive = True

        #二号玩家
        self.tank2 = tank()
        self.tank2.rect.center = (200, 200)
        self.tank_group.add(self.tank2)
        self.tank2.alive = True
        self.bullet_group2 = pg.sprite.Group()

        # 创建墙壁
        with open('maps.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.wall_group = pg.sprite.Group()
        for wall_info in data['map1']:
            self.wall_group.add(wall(wall_info['pos'], wall_info['size'], wall_info['type']))

        # 碰撞检测调试标志
        self.debug_collision = True            

    def remember(self):
        self.tank.remember()
    
    def handle_events(self):
        """处理所有游戏事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                if event.key == pg.K_SPACE:  # 发射子弹
                    if self.tank.alive and len(self.bullet_group) < 5:
                        barrel_length = 45
                        rad_angle = math.radians(self.tank.angle)
                        bullet_start_pos = (
                            self.tank.rect.centerx + barrel_length * math.cos(rad_angle),
                            self.tank.rect.centery - barrel_length * math.sin(rad_angle)
                        )
                        print("发射子弹")
                        self.bullet_group.add(bullet(bullet_start_pos, self.tank.angle))
                if event.key == pg.K_KP_ENTER:  # 二号玩家发射子弹
                    if self.tank2.alive and len(self.bullet_group2) < 5:
                        barrel_length = 45
                        rad_angle = math.radians(self.tank2.angle)
                        bullet_start_pos = (
                            self.tank2.rect.centerx + barrel_length * math.cos(rad_angle),
                            self.tank2.rect.centery - barrel_length * math.sin(rad_angle)
                        )
                        print("二号玩家发射子弹")
                        self.bullet_group2.add(bullet(bullet_start_pos, self.tank2.angle))
        
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.tank.rotate(5)
        if keys[pg.K_d]:
            self.tank.rotate(-5)
        if keys[pg.K_w]:
            self.tank.move_forward(5)
        if keys[pg.K_s]:
            self.tank.move_backward(3)
        if keys[pg.K_LEFT]:
            self.tank2.rotate(5)
        if keys[pg.K_RIGHT]:
            self.tank2.rotate(-5)
        if keys[pg.K_UP]:
            self.tank2.move_forward(5)
        if keys[pg.K_DOWN]:
            self.tank2.move_backward(3)

        return True

    def check_collisions(self):
        '''碰撞检测和响应'''
        # 坦克与墙壁碰撞
        for tank in self.tank_group:
            for wall in self.wall_group:
                if pg.sprite.collide_mask(tank, wall):
                    if self.debug_collision:
                        print("坦克撞墙了!")
                    tank.rewind()  # 碰撞后回退

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
        
        for bullet in self.bullet_group2:
            for wall in self.wall_group:
                if pg.sprite.collide_mask(bullet, wall):
                    if self.debug_collision:
                        print("二号玩家子弹撞墙")
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
                        tank.kill()
                        game.gameover()
        
        for bullet in self.bullet_group2:
            for tank in self.tank_group:
                if pg.sprite.collide_mask(bullet, tank):
                    if self.debug_collision:
                        print("二号玩家子弹击中坦克")
                        self.bullet_group2.remove(bullet)
                        tank.kill()
                        game.gameover()

    def update(self):
        """更新游戏逻辑"""
        # 移除屏幕外的子弹
        for b in self.bullet_group:
            if (b.rect.right < 0 or b.rect.left > 1280 or 
                b.rect.bottom < 0 or b.rect.top > 720):
                self.bullet_group.remove(b)
        
        for b in self.bullet_group2:
            if (b.rect.right < 0 or b.rect.left > 1280 or 
                b.rect.bottom < 0 or b.rect.top > 720):
                self.bullet_group2.remove(b)

        #子弹运动
        self.bullet_group.update()
        self.bullet_group2.update()

        pass

    def restart(self):
        """重置游戏状态"""
        self.tank_group.empty()
        self.bullet_group.empty()
        self.tank = tank()
        self.tank_group.add(self.tank)
        self.tank.alive = True

        self.tank2 = tank()
        self.tank2.rect.center = (200, 200)
        self.tank_group.add(self.tank2)
        self.tank2.alive = True
        self.bullet_group2.empty()

    def gameover(self):
        """处理游戏结束逻辑"""
        if self.tank.alive:
            winner = "一号"
        else:
            winner = "二号"
        image = self.font.render(f"{winner}玩家胜利，游戏结束，按下R重新开始", True, (255, 0, 0))
        rect = image.get_rect(center=(self.WINDOW_SIZE[0]//2, self.WINDOW_SIZE[1]//2))
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        return
                    if event.key == pg.K_r:
                        self.restart()
                        return
            self.window.blit(image, rect)
            pg.display.update()

        pass
    
    def render(self):
        """渲染游戏画面"""
        self.window.fill((255, 255, 255))
        self.wall_group.draw(self.window)
        self.tank_group.draw(self.window)
        self.bullet_group.draw(self.window)
        self.bullet_group2.draw(self.window)
        pg.display.update()
    
    def run(self):
        """主游戏循环"""
        running = True
        while running:
            self.remember()
            running = self.handle_events()
            self.update()
            self.check_collisions()
            self.render()
            
            self.clock.tick(self.FPS)
        
        pg.quit()
        print("游戏已退出")

if __name__ == "__main__":
    game = Game()
    game.run()
