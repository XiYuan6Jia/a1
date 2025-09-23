import pygame
import json
from pygame.locals import *

# 初始化pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 1480
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("地图编辑器")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# 元素类型
ELEMENT_TYPES = ["horizontal", "vertical", "wall", "spawn", "goal"]

# 加载地图数据
def load_map(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {"map1": []}

# 保存地图数据
def save_map(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# 主循环
def main():
    clock = pygame.time.Clock()
    map_data = load_map("maps.json")
    current_map = "map1"
    selected_item = None
    dragging = False
    
    running = True
    while running:
        screen.fill(WHITE)
        
        # 绘制地图元素
        for item in map_data[current_map]:
            rect = pygame.Rect(item["pos"][0], item["pos"][1], 
                             item["size"][0], item["size"][1])
            pygame.draw.rect(screen, BLUE, rect, 2)
            
            # 显示类型文字
            font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 20)
            text = font.render(item["type"], True, BLACK)
            screen.blit(text, (item["pos"][0] + 5, item["pos"][1] + 5))
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    save_map("maps.json", map_data)
                    print("地图已保存")
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    mouse_pos = pygame.mouse.get_pos()
                    for i, item in enumerate(map_data[current_map]):
                        rect = pygame.Rect(item["pos"][0], item["pos"][1], 
                                         item["size"][0], item["size"][1])
                        if rect.collidepoint(mouse_pos):
                            selected_item = i
                            dragging = True
                            break
                    else:
                        # 添加新元素
                        new_item = {
                            "pos": [mouse_pos[0], mouse_pos[1]],
                            "size": [100, 20],
                            "type": ELEMENT_TYPES[0]  # 默认第一个类型
                        }
                        map_data[current_map].append(new_item)
                        selected_item = len(map_data[current_map]) - 1
                        dragging = True
                
                elif event.button == 3:  # 右键切换类型或删除元素
                    mouse_pos = pygame.mouse.get_pos()
                    for i, item in enumerate(map_data[current_map]):
                        rect = pygame.Rect(item["pos"][0], item["pos"][1], 
                                         item["size"][0], item["size"][1])
                        if rect.collidepoint(mouse_pos):
                            keys = pygame.key.get_mods()
                            if keys & KMOD_SHIFT:  # 按住Shift删除元素
                                del map_data[current_map][i]
                                if selected_item == i:  # 如果删除的是当前选中项
                                    selected_item = None
                                elif selected_item is not None and selected_item > i:  # 如果删除项在选中项前面
                                    selected_item -= 1  # 调整选中项索引
                                break
                            else:  # 不按Shift切换类型
                                current_type = item["type"]
                                current_index = ELEMENT_TYPES.index(current_type)
                                next_index = (current_index + 1) % len(ELEMENT_TYPES)
                                item["type"] = ELEMENT_TYPES[next_index]
                            break
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # 左键
                    dragging = False
            
            elif event.type == KEYDOWN:
                if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                    save_map("maps.json", map_data)
                    print("地图已保存")
                elif selected_item is not None:  # 只有选中元素时才处理大小调整
                    if event.key == K_LEFT:
                        map_data[current_map][selected_item]["size"][0] = max(10, map_data[current_map][selected_item]["size"][0] - 5)
                    elif event.key == K_RIGHT:
                        map_data[current_map][selected_item]["size"][0] += 5
                    elif event.key == K_UP:
                        map_data[current_map][selected_item]["size"][1] = max(10, map_data[current_map][selected_item]["size"][1] - 5)
                    elif event.key == K_DOWN:
                        map_data[current_map][selected_item]["size"][1] += 5
                    else:
                        return
                else:
                    print("请先选中一个元素再切换类型")
            
            elif event.type == MOUSEMOTION and dragging:
                if selected_item is not None:
                    keys = pygame.key.get_mods()
                    if keys & KMOD_SHIFT:  # 按住Shift只调整宽度
                        map_data[current_map][selected_item]["size"][0] = max(10, event.pos[0] - map_data[current_map][selected_item]["pos"][0])
                    elif keys & KMOD_CTRL:  # 按住Ctrl只调整高度
                        map_data[current_map][selected_item]["size"][1] = max(10, event.pos[1] - map_data[current_map][selected_item]["pos"][1])
                    else:  # 正常拖动调整位置
                        map_data[current_map][selected_item]["pos"] = [
                            event.pos[0] - map_data[current_map][selected_item]["size"][0] // 2,
                            event.pos[1] - map_data[current_map][selected_item]["size"][1] // 2
                        ]
                    
                    # 取消自动判断类型
                
        # 绘制元素类型选择
        font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)
        for i, elem_type in enumerate(ELEMENT_TYPES):
            color = GREEN if (selected_item is not None and 
                            selected_item < len(map_data[current_map]) and 
                            map_data[current_map][selected_item]["type"] == elem_type) else BLACK
            text = font.render(f"{i+1}. {elem_type}", True, color)
            screen.blit(text, (SCREEN_WIDTH - 190, 10 + i * 30))
        
        # 绘制帮助文本
        help_text = [
            "左键: 添加/移动元素",
            "右键: 删除元素", 
            "方向键: 调整大小",
            "Shift+拖动: 调整宽度",
            "Ctrl+拖动: 调整高度", 
            "Ctrl+S: 保存地图",
            "右键: 切换元素类型",
            "Shift+右键: 删除元素"
        ]
        for i, text in enumerate(help_text):
            screen.blit(font.render(text, True, BLACK), (SCREEN_WIDTH - 190, 200 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
