import pygame as pg
import random
import math
import maps

test_border = 0  # 是否显示边框用于调试
test_hitbox = 0  # 是否启用碰撞检测用于调试

class tank(pg.sprite.Sprite):#坦克
    def __init__(self):
        super().__init__()
        # 设置坦克尺寸
        self.width = 80
        self.height = 30
        self.angle = 0  # 初始角度
        self.original_image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        
        # 生成随机颜色边框
        border_color = (
            random.randint(0, 255),
            random.randint(0, 255), 
            random.randint(0, 255)
        )
        
        # 绘制坦克主体
        pg.draw.rect(self.original_image, border_color, (15, 0, self.width-30, self.height), 2)
        
        # 绘制炮管(从中心向前延伸)
        barrel_length = 34
        pg.draw.line(
            self.original_image, 
            border_color,
            (self.width//2, self.height//2),
            (self.width//2 + barrel_length, self.height//2),
            3
        )

        #绘制驾驶舱
        pg.draw.circle(self.original_image, border_color, (self.width//2, self.height//2), 10, 2)
        
        # 设置旋转后的图像和位置
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(640, 360))
        self.mask = pg.mask.from_surface(self.image)  # 用于像素级碰撞检测

        self.alive = True  # 坦克存活状态
     
    def rotate(self, angle_change):
        """旋转坦克"""
        self.remember_angle()  # 记住当前角度
        self.angle = (self.angle + angle_change) % 360
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)  # 更新碰撞掩码

        if test_border:
            self.show_image_border()  # 调试用，显示边框

    def move_forward(self, distance):
        """向前移动坦克"""
        self.remember_position()  # 记住当前位置
        rad_angle = math.radians(self.angle)
        self.rect.x += distance * math.cos(rad_angle)
        self.rect.y -= distance * math.sin(rad_angle)
        self.mask = pg.mask.from_surface(self.image)  # 更新碰撞掩码
        if test_border:
            self.show_image_border()  # 调试用，显示边框

    def move_backward(self, distance):
        """向后移动坦克"""
        self.remember_position()  # 记住当前位置
        rad_angle = math.radians(self.angle)
        self.rect.x -= distance * math.cos(rad_angle)
        self.rect.y += distance * math.sin(rad_angle)
        self.mask = pg.mask.from_surface(self.image)  # 更新碰撞掩码
        if test_border:
            self.show_image_border()  # 调试用，显示边框

    def remember_position(self):
        """记住当前位置（用于碰撞后回退）"""
        self.last_position = self.rect.topleft

    def remember_angle(self):
        """记住当前角度（用于碰撞后回退）"""
        self.last_angle = self.angle

    def rewind_move(self):
        """将坦克移回上一位置（简单碰撞处理）"""
        self.rect.topleft = self.last_position
        self.angle = self.last_angle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)  # 更新碰撞掩码
            
    def show_image_border(self):
        """显示坦克边框（调试用）"""
        pg.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), 1)

class bullet(pg.sprite.Sprite):#子弹
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        pg.draw.circle(self.image, (0, 0, 0), (2.5, 2.5), 2.5)
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        self.speed = 10
        rad_angle = math.radians(self.angle)
        self.x_speed = self.speed * math.cos(rad_angle)
        self.y_speed = self.speed * math.sin(rad_angle)
        self.mask = pg.mask.from_surface(self.image)  # 用于像素级碰撞检测
        self.time_lived = 0  # 子弹存在的时间


    def update(self):
        self.rect.x += self.x_speed
        self.rect.y -= self.y_speed
        self.time_lived += 1
        if self.time_lived > 500:  # 子弹存在时间超过100帧则消失
            self.kill()

    def kill(self):
        super().kill()
        self.alive = False

class wall(pg.sprite.Sprite):#墙壁
    def __init__(self, pos, size, type):
        super().__init__()
        self.type = type
        self.image = pg.Surface(size)
        self.image.fill((0, 0, 0)) # 黑色墙壁
        self.rect = self.image.get_rect(topleft=pos)
