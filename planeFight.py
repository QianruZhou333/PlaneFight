# 飞机大战
import pygame, sys
import random

pygame.init()
screen_surface = pygame.display.set_mode((480, 600))

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/plane.png')
        self.rect = self.image.get_rect()
        self.rect.center = (screen_surface.get_width()/2, screen_surface.get_height() - 20)
        
    def update(self):
        #获取键盘事件，如果按下，返回True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.rect = self.rect.move(-10, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < screen_surface.get_width():
            self.rect = self.rect.move(10,0)
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect = self.rect.move(0,-10)
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_surface.get_height():
            self.rect = self.rect.move(0,10)
        
        #在屏幕上放飞机，在rect位置
        screen_surface.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/bt.png')
        self.rect = self.image.get_rect()
        #设置初始位置，初始位置要在飞机处，由外部传入
        self.rect.center = center
        
    def update(self):
        #获取键盘事件，如果按下，返回True
        self.rect = self.rect.move(0,-10)
        screen_surface.blit(self.image, self.rect)
        #如果出屏幕了，就终止，删除子弹
        if self.rect.top < 0:
            self.kill()
            
class Enemy_plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/e_plane.png')
        self.rect = self.image.get_rect()
        # 设置初始位置
        x = random.randint(0, screen_surface.get_width())
        y = 0
        self.rect.center = (x,y)
    
    def update(self):
        self.rect = self.rect.move((0,5))
        if self.rect.y > screen_surface.get_height():
            x = random.randint(0, screen_surface.get_width())
            y = 0
            self.rect.center = (x,y)
        #屏幕上放飞机，在rect位置上
        screen_surface.blit(self.image, self.rect)
        
#创建一架飞机
plane_surface = Plane()
# 创建一个子弹 精灵组（用于存放所有的精灵对象）
bullet_sprite = pygame.sprite.Group()
#创建敌机
enemy_plane_surface = Enemy_plane()

#存储得分
score = 0

#背景音乐
music_bg = pygame.mixer.Sound('mp3/背景音乐.mp3')
music_bg.play(loops=-1) #播放音乐（loops=-1循环播放）
#发射音效
music_shoot = pygame.mixer.Sound('mp3/shoot.mp3') 
#得分音效
music_score = pygame.mixer.Sound('mp3/score.mp3')

clock = pygame.time.Clock()

#游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #按下一个空格，创建一个子弹对象
                bullet_surface = Bullet(plane_surface.rect.center)
                bullet_sprite.add(bullet_surface)
                music_shoot.play()
       
    #重新绘制背景
    screen_surface.fill((0,0,0))
    #飞机修改数据 更新画面
    plane_surface.update()
    #子弹更新数据 更新画面
    bullet_sprite.update()
    #敌机更新数据 更新画面
    enemy_plane_surface.update()
    
    #判断子弹是否和敌机碰撞
    a=pygame.sprite.spritecollide(enemy_plane_surface, bullet_sprite, True, collided = pygame.sprite.collide_mask)
    if a:
        music_score.play()
        score += 10
        x = random.randint(0, screen_surface.get_width())
        y = 0
        enemy_plane_surface.rect.center = (x,y)
        
    # 判断敌机是否和战斗机相撞
    b = pygame.sprite.collide_mask(enemy_plane_surface, plane_surface)
    if b:
        break
        
    # 记录得分
    font_name = pygame.font.match_font("黑体")
    font = pygame.font.Font(font_name, 20)
    # 绘制内容
    font_surface = font.render(str(score), True, 'white')
    screen_surface.blit(font_surface, (screen_surface.get_width()/2, 10))
    
    #界面更新
    pygame.display.flip()
    clock.tick(25)