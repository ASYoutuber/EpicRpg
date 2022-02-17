import pygame
import os
import random
import button

pygame.init()

bottom_panel = 150
window_width = 800
window_height = 400 + 150

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Battle")
icon = pygame.image.load(os.path.join("Assets/icons/sword.png"))
pygame.display.set_icon(icon)

background_img = pygame.image.load(os.path.join("Assets/Background/background.png"))
panel_img = pygame.image.load(os.path.join("Assets/Icons/panel.png"))
sword_img = pygame.image.load(os.path.join("Assets/Icons/sword.png"))
potion_img = pygame.image.load(os.path.join("Assets/Icons/potion.png"))
victory_img = pygame.image.load(os.path.join("Assets/Icons/victory.png"))
defeat_img = pygame.image.load(os.path.join("Assets/Icons/defeat.png"))
restart_img = pygame.image.load(os.path.join("Assets/Icons/restart.png"))

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
potion_effect = 15
attack = False
potion = False
clicked = False
game_over = 0

font = pygame.font.SysFont("Times New Roman", 26)

red = (255, 0, 0)
green = (0, 255, 0)

def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    window.blit(image, (x, y))

def draw_bg():
    window.blit(background_img, (0, 0))

def draw_panel():
    window.blit(panel_img, (0, window_height - bottom_panel))
    draw_text(f"{knight.name} HP: {knight.health}", font, red, 100, window_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        draw_text(f"{i.name} HP: {i.health}", font, red, 550, (window_height - bottom_panel + 10) + count * 60)

class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_health = max_hp
        self.health = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(8):
            image = pygame.image.load(os.path.join(f"Assets/{self.name}/Idle/{i}.png"))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(8):
            image = pygame.image.load(os.path.join(f"Assets/{self.name}/Attack/{i}.png"))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(3):
            image = pygame.image.load(os.path.join(f"Assets/{self.name}/Hurt/{i}.png"))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(10):
            image = pygame.image.load(os.path.join(f"Assets/{self.name}/Death/{i}.png"))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.health -= damage
        target.hurt()
        if (target.health < 1):
            target.health = 0
            target.alive = False
            target.death()
        damage_text = Damagetext(target.rect.centerx, target.rect.y, str(damage), red)
        damagetext_group.add(damage_text)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.health = self.max_health
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if (pygame.time.get_ticks() - self.update_time > animation_cooldown):
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if (self.frame_index >= len(self.animation_list[self.action])):
            if (self.action == 3):
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def draw(self):
        window.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.health = hp
        self.max_health = max_hp
    
    def draw(self, hp):
        self.health = hp
        ratio = self.health / self.max_health

        pygame.draw.rect(window, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(window, green, (self.x, self.y, 150 * ratio, 20))

class Damagetext(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        
        if (self.counter > 30):
            self.kill()

damagetext_group = pygame.sprite.Group()

knight = Fighter(200, 260, "Knight", 35, 11, 3)
bandit_1 = Fighter(550, 270, "Bandit", 20, 7, 1)
bandit_2 = Fighter(700, 270, "Bandit", 20, 7, 1)

bandit_list = []
bandit_list.append(bandit_1)
bandit_list.append(bandit_2)

knight_healthbar = HealthBar(100, window_height - bottom_panel + 40, knight.health, knight.max_health)
bandit1_healthbar = HealthBar(550, window_height - bottom_panel + 40, bandit_1.health, bandit_1.max_health)
bandit2_healthbar = HealthBar(550, window_height - bottom_panel + 100, bandit_2.health, bandit_2.max_health)

potion_button = button.Button(window, 100, window_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(window, 330, 120, restart_img, 120, 30)

clock = pygame.time.Clock()
fps = 60

run = True
while run:
    clock.tick(fps)

    draw_bg()
    draw_panel()

    knight.update()
    knight.draw()

    knight_healthbar.draw(knight.health)
    
    bandit1_healthbar.draw(bandit_1.health)
    bandit2_healthbar.draw(bandit_2.health)

    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    damagetext_group.update()
    damagetext_group.draw(window)

    attack = False
    potion = False
    target = None
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if (bandit.rect.collidepoint(pos)):
            pygame.mouse.set_visible(False)
            window.blit(sword_img, pos)
            if (clicked and bandit.alive):
                attack = True
                target = bandit_list[count]
    if (potion_button.draw()):
        potion = True
    draw_text(str(knight.potions), font, red, 150, window_height - bottom_panel + 70)

    if (game_over == 0):
        if (knight.alive):
            if (current_fighter == 1):
                action_cooldown += 1
                if (action_cooldown >= action_wait_time):
                    if (attack and target != None):
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0

                    if (potion):
                        if (knight.potions > 0):
                            if (knight.max_health - knight.health > potion_effect):
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_health - knight.health
                            knight.health += heal_amount
                            knight.potions -= 1
                            damage_text = Damagetext(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damagetext_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        for count, bandit in enumerate(bandit_list):
            if (current_fighter == 2 + count):
                if (bandit.alive):
                    action_cooldown += 1
                    if (action_cooldown >= action_wait_time):
                        if ((bandit.health / bandit.max_health) < 0.5 and bandit.potions > 0):
                            if (bandit.max_health - bandit.health > potion_effect):
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_health - bandit.health
                            bandit.health += heal_amount
                            bandit.potions -= 1
                            damage_text = Damagetext(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damagetext_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        else:  
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1
        
        if (current_fighter > total_fighters):
            current_fighter = 1

    alive_bandits = 0
    for bandit in bandit_list:
        if (bandit.alive):
            alive_bandits += 1
    
    if (alive_bandits == 0):
        game_over = 1

    if (game_over != 0):
        if (game_over == 1):
            window.blit(victory_img, (250, 50))
        if (game_over == -1):
            window.blit(defeat_img, (290, 50))
        if (restart_button.draw()):
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
        
        if (event.type == pygame.K_ESCAPE):
            run = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            clicked = True
        else:
            clicked = False
        

    pygame.display.update()
pygame.quit()