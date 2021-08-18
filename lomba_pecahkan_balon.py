# 1 - Import Library ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame
import math
from random import randint #(random integer) untuk membuat bilangan acak
from pygame.locals import *

# 2 - Initialize the Game ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pygame.init()
width, height = 800, 480
screen = pygame.display.set_mode((width, height))
health_point = 194 # default health point for castle
countdown_timer = 60000 # 60 detik

# Key mapping
keys = {
    "top": False, 
    "bottom": False,
    "left": False,
    "right": False 
}

running = True

playerpos = [100, 100] # letak anak pertama kali diletakkan

exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1
score = 0 
arrows = [] # list of arrows

balon_timer = 100 # waktu kemunculan
balons = [[width, 100]] # list yang menampung koordinat balon

# 3 - Load Game Assets ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3.1 - Load Images
player = pygame.image.load("resources/images/anak.png")
background = pygame.image.load("resources/images/background.png")
kaktus = pygame.image.load("resources/images/kaktus.png")
arrow = pygame.image.load("resources/images/bullet.png")
balon_img = pygame.image.load("resources/images/balon.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
balon_hit_sound = pygame.mixer.Sound("resources/audio/Balloon_popping.mp3")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
balon_hit_sound.set_volume(0.05)
shoot_sound.set_volume(0.05)

# background music
pygame.mixer.music.load("resources/audio/hari_merdeka.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

## 4 - The Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while(running):
    
    # 5 - Membuat tampilan hitam sebelum dimasukan semuanya
    screen.fill(0)
    
    # 6 - Draw the game object ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # draw the background
    screen.blit(background, (0, 0))

    #6.1 - Draw arrows
    for bullet in arrows:
        arrow_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1
        # draw the arrow
        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))

    # 6.2 - Draw Balon
    # waktu balon akan muncul
    balon_timer -= 1
    if balon_timer == 0:
        # buat balon baru
        balons.append([width, randint(50, height-32)])
        # reset balon timer to random time
        balon_timer = randint(1, 100)

    index = 0
    for balon in balons:
        # balon bergerak dengan kecepatan 5 pixel ke kiri
        balon[0] -= 5
        # hapus balon saat mencapai batas layar sebelah kiri
        if balon[0] < -64:
            balons.pop(index)

    # 6.2.1 collision between balon and kaktus 
        balon_rect = pygame.Rect(balon_img.get_rect())
        balon_rect.top = balon[1] # ambil titik y 
        balon_rect.left = balon[0] # ambil titik x
        # benturan musuh dengan markas kelinci
        if balon_rect.left < 40:
            balons.pop(index)
            health_point -= randint(5,20)
            hit_sound.play()
            print("Oh Tidak Balonnya Lewat!!")
        
        # 6.2.2 Check for collisions between enemies and arrows
        index_arrow = 0
        for bullet in arrows:
            bullet_rect = pygame.Rect(arrow.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            # benturan anak panah dengan musuh
            if balon_rect.colliderect(bullet_rect):
                score += 1
                balons.pop(index)
                arrows.pop(index_arrow)
                balon_hit_sound.play()
                print("Boom! Balonnya Pecah")
                print("Score: {}".format(score))
            index_arrow += 1
        index += 1

    # gambar balon ke layar
    for balon in balons:
        screen.blit(balon_img, balon)

    # 6.3 - Draw Health bar
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    # 6.4 - Draw clock
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 itu sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [795, 5]
    screen.blit(clock, textRect)
    #-----------------------------------------------------------   

    # draw the kaktus
    screen.blit(kaktus, (0, 25))
    screen.blit(kaktus, (0, 105))
    screen.blit(kaktus, (0, 205))
    screen.blit(kaktus, (0, 305))
    screen.blit(kaktus, (0, 400))
                
    # draw the player
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 28.66)
    new_playerpos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos)
    #screen.blit(player, playerpos)
           
    # 7 - Update the sceeen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pygame.display.flip()

    # 8 - Event Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Mengecek event apa saja yang terjadi di dalam game,
    # contoh keyboard ditekan, dll
    for event in pygame.event.get():
        # event saat tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # PECAHKAAAAAN BALOON!!
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])
            shoot_sound.play()
            
        # chek the keydown and keyup
        if event.type == pygame.KEYDOWN: #Event KEYDOWN artinya saat kita menekan tombol di keyboard
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pygame.KEYUP: #KEYUP saat kita melepas keyboad
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False
    # - End of event loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # 9. Move the player ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if keys["top"]:
        playerpos[1] -= 5 # kurangi nilai y
    elif keys["bottom"]:
        playerpos[1] += 5 # tambah nilai y 
    if keys["left"]:
        playerpos[0] -= 5 # kurangi nilai x
    elif keys["right"]:
        playerpos[0] += 5 # tambah nilai x

    # 10 - Win/Lose check ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

    # - End of Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # - End of Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # 11 - Win/lose display ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if exitcode == EXIT_CODE_GAME_OVER:
            screen.blit(gameover, (0, 0))
        else:
            screen.blit(youwin, (0, 0))

        # Tampilkan score
        text = font.render("Score: {}".format(score), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(text, textRect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            pygame.display.flip()
