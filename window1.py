#窗口1
import pygame as pg

# 多行文本处理函数
def render_multiline_text(text, font, color, max_width):
    """将长文本分割成多行"""
    words = text
    lines = []
    current_line = ""
    
    for char in words:
        test_line = current_line + char
        # 检查当前行宽度是否超过最大宽度
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    return lines

# 初始化pygame
pg.init()

#################################################################################################################     #资源加载
#设置窗口尺寸
size = (window_w,window_h) = (1280,720)
#窗口标题
title1 = "欣然赴死"
#帧率
clock = pg.time.Clock()
targeted_fps = 30
#创建窗口
window1 = pg.display.set_mode(size)
#设置窗口标题
pg.display.set_caption(title1)

#填充白色背景
window1.fill((255,255,255)) 

##############################################################################      #图片
img1 = pg.image.load(r'assets\image\b2.png')
draw_img = pg.Surface((100,100),pg.SRCALPHA)    #创建一个支持透明的画布
#img2 = pg.transform.scale(img1,(100,100))       #缩放图片
img2 = pg.transform.rotate(img1,60)         #旋转图片
#初始化字体 - 使用系统字体支持中文
try:
    # 尝试使用常见的中文字体
    font = pg.font.Font("C:/Windows/Fonts/simhei.ttf", 36)  # 使用黑体
except:
    try:
        # 如果黑体不存在，尝试使用其他中文字体
        font = pg.font.Font("C:/Windows/Fonts/msyh.ttc", 36)  # 使用微软雅黑
    except:
        # 如果都没有，使用系统字体
        font = pg.font.SysFont("simsun", 36)  # 使用宋体

# 要显示的多行文本
long_text = "请输入文本"
max_line_width = 800  # 最大行宽

##############################################################################      #音频
pg.mixer.music.load(r'assets\audio\Toby Fox - sans_.wav')
volume = pg.mixer.music.get_volume()
pg.mixer.music.set_volume(0.1)
#pg.mixer.music.play()



############################################################################        #参数
#方框位置和尺寸
rect_x=0
rect_y=0
rect_w=pg.Surface.get_width(img2)
rect_h=pg.Surface.get_height(img2)
#速度矢量
a=6
b=6
v=3
#转动
rotate=60

#循环标志
rn=True

###########################################################################     #循环进程

#主循环
while rn:
    ##########################################################################      #事件处理
    
    for ev in pg.event.get():
        #如果点击关闭窗口按钮
        if ev.type == pg.QUIT:
            #退出循环
            rn=False
            break
        #按下按键
        elif ev.type == pg.KEYDOWN:
            '''if ev.key == pg.K_ESCAPE:
                rn = False
                break'''
            if ev.key == pg.K_KP_6:
                a+=3
            if ev.key == pg.K_KP_4:
                a-=3
            if ev.key == pg.K_KP_2:
                b+=3
            if ev.key == pg.K_KP_8:
                b-=3
            if ev.key == pg.K_PAGEDOWN:
                v-=1
                if v<1:
                    v=1
            if ev.key == pg.K_PAGEUP:
                v+=1
                if v>10:
                    v=10
            continue
    #按住按键
    Keys = pg.key.get_pressed()
    if Keys[pg.K_w]:
        rect_y-=v
    if Keys[pg.K_s]:
        rect_y+=v
    if Keys[pg.K_d]:
        rect_x+=v
    if Keys[pg.K_a]:
        rect_x-=v
##############################################################################              # 逻辑处理区
    # 多行文本
    long_text = f"横向速度{a},纵向速度{b},坐标（{rect_x},{rect_y}），音量{volume}"

    #运动
    rect_x+=a
    rect_y+=b

    #反弹检测
    if rect_x>window_w-rect_w:
        a*= -1
    if rect_x<0:
        a*= -1
    if rect_y>window_h-rect_h:
        b*= -1
    if rect_y<0:
        b*= -1

    #主体边界检测
    if rect_x>window_w-rect_w:
        rect_x=window_w-rect_w
    if rect_x<0:
        rect_x=0
    if rect_y>window_h-rect_h:
        rect_y=window_h-rect_h
    if rect_y<0:
        rect_y=0

    #旋转
    img2 = pg.transform.rotate(img1,rotate)
    rotate+=6
    if rotate>=360:
        rotate=0

    #音量
    volume = pg.mixer.music.get_volume()

################################################################################         #背景   文字渲染区
    window1.fill((255,255,255)) #填充白色背景
    

    # 渲染多行文本
    text_lines = render_multiline_text(long_text, font, (0, 0, 0), max_line_width)
    text_surfaces = [font.render(line, True, (0, 0, 0)) for line in text_lines]
    y_offset = 200  # 文本起始Y坐标
    for i, text_surface in enumerate(text_surfaces):
        text_rect = text_surface.get_rect(center=(size[0]//2, y_offset + i * 40))
        window1.blit(text_surface, text_rect)

###################################################################################     #图形渲染区
    
#    pg.draw.rect(window1,(0,0,255),(rect_x,rect_y,rect_w,rect_h),1)#边框
    window1.blit(img2,(rect_x,rect_y),None,0) #绘制图片

    



#########################################
    #更新窗口内容    
    pg.display.update()
    #tick帧率
    clock.tick(targeted_fps)
    
print("退出循环")

#推出pygame
pg.quit()
