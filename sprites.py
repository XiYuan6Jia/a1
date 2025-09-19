import pygame as pg
import random
import math
import maps

test_border = 1  # 是否显示边框用于调试
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
        barrel_length = 35
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
     
    def rotate(self, angle_change):
        """旋转坦克"""
        self.angle = (self.angle + angle_change) % 360
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if test_border:
            self.show_image_border()  # 调试用，显示边框

    def move_forward(self, distance):
        """向前移动坦克"""
        rad_angle = math.radians(self.angle)
        self.rect.x += distance * math.cos(rad_angle)
        self.rect.y -= distance * math.sin(rad_angle)
        if test_border:
            self.show_image_border()  # 调试用，显示边框

    def move_backward(self, distance):
        """向后移动坦克"""
        rad_angle = math.radians(self.angle)
        self.rect.x -= distance * math.cos(rad_angle)
        self.rect.y += distance * math.sin(rad_angle)
        if test_border:
            self.show_image_border()  # 调试用，显示边框
            
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

    def update(self):
        rad_angle = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(rad_angle)
        self.rect.y -= self.speed * math.sin(rad_angle)

class wall(pg.sprite.Sprite):#墙壁
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill((0, 0, 0)) # 黑色墙壁
        self.rect = self.image.get_rect(topleft=pos)

if __name__ == "__main__":
    ##############################################################################
    #帧率
    clock = pg.time.Clock()
    targeted_fps = 30

    #坦克组
    tank1 = tank()
    tank_group = pg.sprite.Group()
    #子弹组
    bullet_group = pg.sprite.Group()
    #墙壁组
    wall_group = pg.sprite.Group()
    for wall_info in maps.map1:
        new_wall = wall(wall_info['pos'], wall_info['size'])
        wall_group.add(new_wall)


    #初始化pygame
    pg.init()

    window = pg.display.set_mode((1280, 720))


    rn=True
    ###########################################################################     #循环进程
    while rn:
        ##########################################################################      #事件处理
        for ev in pg.event.get():
            #如果点击关闭窗口按钮
            if ev.type == pg.QUIT:
                #退出循环
                rn=False
                break
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    rn = False
                    break
                if ev.key == pg.K_SPACE:#发射子弹
                    barrel_length = 35
                    rad_angle = math.radians(tank1.angle)
                    bullet_start_pos = (
                        tank1.rect.centerx + barrel_length * math.cos(rad_angle),
                        tank1.rect.centery - barrel_length * math.sin(rad_angle)
                    )
                    new_bullet = bullet(bullet_start_pos, tank1.angle)
                    bullet_group.add(new_bullet)
                    print("发射子弹")

        #按住键盘
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            tank1.rotate(5)
        if keys[pg.K_d]:
            tank1.rotate(-5)
        tank_group.add(tank1)
        if keys[pg.K_w]:
            tank1.move_forward(5)
        if keys[pg.K_s]:
            tank1.move_backward(3)



    ##############################################################################              # 逻辑处理区

        #超出屏幕的子弹删除
        for b in bullet_group:
            if (b.rect.right < 0 or b.rect.left > 1280 or 
                b.rect.bottom < 0 or b.rect.top > 720):
                bullet_group.remove(b)

        bullet_group.update() #更新子弹位置

    ################################################################################         #背景   文字渲染区
        window.fill((255,255,255)) #填充白色背景
        



    ###################################################################################     #图形渲染区
        wall_group.draw(window) #绘制墙壁
        tank_group.draw(window) #绘制坦克
        bullet_group.draw(window) #绘制子弹


        



    #########################################
        #更新窗口内容    
        pg.display.update()
        #tick帧率
        clock.tick(targeted_fps)
        
    print("退出循环")


    pg.quit()
