import pygame 
player1_image = pygame.image.load("player1.png")
player2_image = pygame.image.load("player2.png")
ball_image = pygame.image.load("ball.png")

player1_image = pygame.transform.scale(player1_image, PLAYER_SIZE)
player2_image = pygame.transform.scale(player2_image, PLAYER_SIZE)
ball_image = pygame.transform.scale(ball_image, BALL_SIZE)

pygame.screen.blit(player1_image, player1.topleft)
pygame.screen.blit(player2_image, player2.topleft)
pygame.screen.blit(ball_image, ball.topleft)
