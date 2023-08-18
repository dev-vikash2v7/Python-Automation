import pygame as p,os,sys,random as r
from pygame.locals import*
p.init()


#global variables
fps=30
s_width=280
s_height=512

#game window
SCREEN=p.display.set_mode((s_width,s_height ))
p.display.set_caption('FLAPPY BIRD')


#image variable
img={}
pipe='images/pipe.png'
bird='images/bird.png'
bg='images/bg.png'
base='images/base.png'
mess='images/message.png'

#sound variable
sound={}



def welcome():
	
	#bird pos
	bird_x=int(s_width*0.2)
	bird_y=int((s_height-img['bird'].get_height())/5)
	
	#mess pos
	mess_x=int((s_width-img['mess'].get_width())/2)
	mess_y=int((s_height*0.2)/2)
	
	#base pos
	base_x=0
	base_y=s_height*0.8
	
	while True:
		for event in p.event.get():
			if (event.type==p.QUIT) or (event.type==p.KEYDOWN and event.key==p.K_ESCAPE):
				p.quit()
				sys.exit()
				
			elif event.type==p.KEYDOWN and event.key==p.K_RETURN:
				return
			
			else:
				SCREEN.blit(img['bg'],(0,0))
				SCREEN.blit(img['bird'],(bird_x,bird_y))
				SCREEN.blit(img['mess'],(mess_x,mess_y))
				SCREEN.blit(img['base'],(base_x,base_y))
				p.display.update()
				fpsclock.tick(fps)





def maingame():
	
	bird_h=img['bird'].get_width()
	
	#initial pos
	score=0
	bird_x=s_width/5
	bird_y=s_height/5
	
	base_x=0
	base_y=s_height*0.8

	
	# creatimg 2 pipe 
	n_pipe1=random_pipe()
	n_pipe2=random_pipe()
	
	#low_pipes list
	
	low_pipes=[
	{'x':s_width+200,'y':n_pipe1[1]['y']},
	{'x':s_width+200+(s_width/2), 		
	'y':n_pipe2[1]['y']}]
	
	#upper pipes list 
	
	upp_pipes=[
	{'x':s_width+200,'y':n_pipe1[0]['y']},
	{"x":s_width+200+(s_width/2),   
	'y':n_pipe2[0]['y']}
	]
	
	#creating velocity
	
	pipe_vx=-6
	
	bird_vy=-11
	bird_max_vy=10
	birdy_min_vy=-8
	bird_accy=1
	
	birdflap_vy=-10
	
	birdflaped=False #true when not flap
	
	while True:
		for event in p.event.get():
							if event.type==p.QUIT or (event.type==KEYDOWN and event.key==p.K_ESCAPE):
								p.quit()
								sys.exit()				 
							elif event.type==p.KEYDOWN and event.key==p.K_SPACE:
								if bird_y>0:
									birdflaped=True
									bird_vy=birdflap_vy
									sound['wing'].play()
									
		#check collsion
		crashtext=iscollide(bird_x,bird_y,low_pipes,upp_pipes)
		if crashtext:
		    return
	
		
		#create score
		bird_midpos=bird_x+img['bird'].get_width()/2
		
		for pipe in upp_pipes:
			pipe_midpos=pipe['x']+img['pipe'][0].get_width()/2
			
			if pipe_midpos <= bird_midpos < pipe_midpos + 4:
				score+=1
				sound['point'].play()
		
		if bird_vy<bird_max_vy and not birdflaped:    #brd_vy=-9 & brf max=10
		
		    bird_vy+=bird_accy#inc sped
		    
		if birdflaped:
		    birdflaped = False #to cont flapin
		    
		bird_y+=min(bird_vy,base_y-bird_y-bird_h)#chage pos in y dir
		
		
		#to move pipes in left
		for upperpipe,lowerpipe in zip(upp_pipes,low_pipes):
		    upperpipe['x']+=pipe_vx
		    lowerpipe['x']+=pipe_vx

        #to add pipe        
		if 0<upp_pipes[0]['x']<5:
		          newpipe=random_pipe()
		          upp_pipes.append(newpipe[0])
		          low_pipes.append(newpipe[1])
		

		#to remove pipe
		if upp_pipes[0]['x']< -img['pipe'][0].get_width():
		          upp_pipes.pop(0)
		          low_pipes.pop(0)
		          
		
		#imges in game bliting 
		
		SCREEN.blit(img['bg'],(0,0))

		
		for upperpipe,lowerpipe in zip(upp_pipes,low_pipes):
		    
		    #bliting pipes
		    SCREEN.blit(img['pipe'][0],(upperpipe['x'],upperpipe['y']))
		    
		    SCREEN.blit(img['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
		    
		SCREEN.blit(img['base'],(base_x,base_y))
		SCREEN.blit(img['bird'],(bird_x,bird_y))
		
		    
		  
		 #score bliting   
		digits= [int(x) for x in list(str(score))]
		wid=0
		
		
		for i in digits:		    
		    wid+=img['num'][i].get_width()
		    
		xoffset=(s_width-wid)/2
		
		for i in digits:
		    
		    SCREEN.blit(img['num'][i],(xoffset,s_height*0.12))
		    
		    xoffset+=img['num'][i].get_width()
				
		p.display.update()
		fpsclock.tick(fps)
            
            
    
        
#collididon chec fun
def iscollide(bird_x,bird_y,low_pipes,upp_pipes):
    base_y=0.8*s_height
    
    if bird_y > base_y-35 or bird_y<0:
        sound['hit'].play()
        return True
        
    for pipe in upp_pipes:
        
        pipe_h=img['pipe'][0].get_height()
        pipe_w=img['pipe'][0].get_width()
        
        if (bird_y<pipe_h+pipe['y']) and abs(bird_x-pipe['x']) < pipe_w :
            sound['hit'].play()
            return True
            
    for pipe in low_pipes:
        bird_h=img['bird'].get_height()
        
        if (bird_y + bird_h > pipe['y']) and abs(bird_x - pipe['x']) < pipe_w :
            sound['hit'].play()
            return True
        
    
	
						
						
#randomly pipe generates
def random_pipe():
	
	offset=s_height/3
	pipe_h=img['pipe'][0].get_height()
	pipe_x=s_width+10
	base_h=img['base'].get_height()
	

	#lower pipe pos
	y2=offset+r.randrange(0,int(s_height-base_h-1.6*offset))
	
	#upper pipe pos
	y1=pipe_h-y2+offset
	
	pipe=[{'x':pipe_x,'y':-y1},
	 {'x':pipe_x,'y':y2}]
	
	return pipe




if __name__=="__main__" :
		fpsclock=p.time.Clock()
		
		#score img
		m=[ ]
		for i in range(10):
			a=str(i)
			m.append(p.image.load('images/score/'+a+'.png').convert_alpha())
			
		img['num']=m
		
		#othera img

		img['mess']=p.image.load(mess).convert_alpha()
		
		img['base']=p.image.load(base).convert_alpha()
		
		img['pipe']=(p.transform.rotate(p.image.load(pipe).convert_alpha(),180),p.image.load(pipe).convert_alpha())
		
		img['bg']=p.image.load(bg).convert_alpha()
		
		img['bird']=p.image.load(bird).convert_alpha()
		
		
		#game sound
		for i in ['die','hit','point','wing']:
			sound[i]=p.mixer.Sound('audio/'+i+'.ogg')
		while True:
			    welcome()
			    maingame()
		
		
		
		
			
		
	



