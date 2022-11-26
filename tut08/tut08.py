

from datetime import datetime
start_time = datetime.now()
import pandas as pd
import sys
from csv import writer
start_time = datetime.now()

#Help
def scorecard():
	pass
	score= open('tut08\Scorecard.txt','a')   
	#opening scorecard as score
 
	pak_ins=open('tut08\pak_inns1.txt','r').read() 
	# pak batting is opened as pak_ins
	
	splitefile=[]  # this is used to score splited file 
	for p in pak_ins.split('\n\n'):
		splitefile.append(p)           	#spliting to get batsmen and bowlers name
	line=[]
	for p in range(len(splitefile)):
		line.append(splitefile[p].split(','))
	lx=len(splitefile)
	
	pak_batsman=[]
	ind_bowlers=[]
	pak_inns_ball=[]
	for i in range(len(line)):
		pak_bat= line[i][0].split('to')      # storing pak batsmen name 
		india_bowl=pak_bat[0].split(' ')	#storing indbowler  name
		
		pak_batsman.append(pak_bat[1])     
		stin=''
		for j in range(len(india_bowl)-1):
			if j!=0:
				stin=stin+india_bowl[j]+" "       #here we are attcahing the india bowler to aur data  frame
			else:
				continue
		pak_inns_ball.append(india_bowl[0])
		ind_bowlers.append(stin)
		
	
	
	current_bowler=pd.DataFrame()                         #making data frame to store bowlers name
	bowlers_ind_play= list(dict.fromkeys(ind_bowlers))  # making a list out of dictionary of ind bowlers
	current_bowler['BOWLER']=bowlers_ind_play
	current_bowler['O']=current_bowler['M']=current_bowler['R']=current_bowler['W']=current_bowler['NB']=current_bowler['WD']=current_bowler['EC']=current_bowler['B']=0
	batman_pak_play= list(dict.fromkeys(pak_batsman))
	current_batsman=pd.DataFrame()     # making a list out of dictionary of pak batsmen
	current_batsman['BATTER']=batman_pak_play
	current_batsman['status']='Not Out'
	current_batsman['R']=current_batsman['B']=current_batsman['4s']=current_batsman['6s']=current_batsman['SR']=0



	# print(bowlers)
	fall_wicket=[]     
	ext=wide=score=wickets=NoBall=b=lb=0
	for i in range(len(line)):    #ere we are increasing the no of played by batsmen and bowl bowled by bowler and also counting the  no. of widers byes legbyesetc
		line[i][1]=line[i][1].lower()
		ind_present_bowler=ind_bowlers[i]
		pak_present_batsmen=pak_batsman[i]
		ball_no=pak_inns_ball[i]
		row_pak_2=0
		row_pak_1=0
		for k in range(len(batman_pak_play)):
			if batman_pak_play[k]==pak_batsman[i]:
				row_pak_2=k
				break
			
		for k in range(len(bowlers_ind_play)):
			if bowlers_ind_play[k]==ind_bowlers[i]:
				row_pak_1=k
				break

		
		
		if line[i][1]==' wide':
			
			
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+1
			score=score+1
			current_bowler.at[row_pak_1,'WD']=current_bowler.at[row_pak_1,'WD']+1
			
			wide=wide+1
		elif line[i][1]==' 2 wides':
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+2
			score=score+2
			current_bowler.at[row_pak_1,'WD']=current_bowler.at[row_pak_1,'WD']+2
			
			wide=wide+2
		elif line[i][1]==' 3 wides':
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+3
			score=score+3
			current_bowler.at[row_pak_1,'WD']=current_bowler.at[row_pak_1,'WD']+3
			
			wide=wide+3
		elif line[i][1]==' byes':
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			
			if line[i][2]==' 1 run':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+1
				score=score+1

			elif line[i][2]==' 2 runs':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+2
				score=score+2
			elif line[i][2]==' 3 runs':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+3
				score=score+3
			elif line[i][2]==' 4 run' or line[i][2]==' FOUR':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+4
				score=score+4

		elif line[i][1]==' no run':
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1

			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1

		elif line[i][1]==' 1 run':
			score=score+1
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+1
			
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+1
			
			
			

		elif line[i][1]==' 2 runs':
			
			score=score+2
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+2
			
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+2
			
		
		elif line[i][1]==' 3 runs':
			score=score+3
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+3
			
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+3
			
			
		
		elif line[i][1]==' four':
			score=score+4
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_batsman.loc[row_pak_2,'4s']=current_batsman.loc[row_pak_2,'4s']+1
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+4
			
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+4
			
			

		elif line[i][1]==' six':
			score=score+6
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			
			current_batsman.loc[row_pak_2,'6s']=current_batsman.loc[row_pak_2,'6s']+1
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+6

			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+6
			
			
		elif line[i][1]==' leg byes':
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
   
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			
			lg=lg+1
			if line[i][2]==' 1 run':
				score=score+1
			elif line[i][2]==' 2 runs':
				score=score+2
			elif line[i][2]==' 3 runs':
				score=score+3
			elif line[i][2]==' 4 runs' or line[i][2]==' FOUR':
				score=score+4
		elif line[i][1]==' no ball':
			NoBall=NoBall+1
			score=score+1
			
			current_bowler.loc[row_pak_1,'R']=current_bowler.loc[row_pak_1,'R']+1
			current_bowler.loc[row_pak_1,'NB']=current_bowler.loc[row_pak_1,'NB']+1
		
		

		else:
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
   
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			
			add_fall_wicket= str(score)+'-'+str(wickets)+'('+ pak_present_batsmen +','+ball_no+')'
			fall_wicket.append(add_fall_wicket)
			if len(fall_wicket)%5==0:   # doing line scane of scorecard if wicket line is greater than 5
				fall_wicket.append('\n') 

			wicket_count=line[i][1].split('!')   #using split function getting the type of wicket from commentry
			if wicket_count[0]==' out lbw':
				current_batsman.loc[row_pak_2,'status']='lbw b '+ind_present_bowler
				current_bowler.at[row_pak_1,'W']=current_bowler.at[row_pak_1,'W']+1
				wickets=wickets+1
			else:	
				
				if wicket_count[0]==' run out':
					current_batsman.loc[row_pak_2,'status']='run out'
					wickets=wickets+1
				elif wicket_count[0]==' out bowled':
					current_batsman.loc[row_pak_2,'status']='b'+ind_present_bowler
					current_bowler.at[row_pak_1,'W']=current_bowler.at[row_pak_1,'W']+1
					wickets=wickets+1
				else:
					content2=wicket_count[0].split('by')
					current_batsman.loc[row_pak_2,'status']='c'+content2[1]+' b '+ind_present_bowler
					current_bowler.at[row_pak_1,'W']=current_bowler.at[row_pak_1,'W']+1
					wickets=wickets+1
	for i in range (len(current_bowler)):
		rem=(current_bowler.at[i,'B']%6)/10	
		val=int(current_bowler.at[i,'B']/6)	
		current_bowler.at[i,'O']=round(val+rem,1)
		current_bowler.at[i,'EC']=round(current_bowler.at[i,'R']/current_bowler.at[i,'O'],2)

	for i in range (len(current_batsman)):
		
		current_batsman.loc[i,'SR']=round((current_batsman.loc[i,'R']/current_batsman.loc[i,'B'])*100,2)	

	
	del current_bowler['B']
	
	ext=wide+NoBall+lb+b
	current_batsman.loc[len(current_batsman)+1,'BATTER']=''
	current_batsman.loc[len(current_batsman)+1,'BATTER']=('Extras\t\t'+str(ext)+'(b '+str(b)+', lb '+str(lb)+', w '+str(wide)+', nb '+str(NoBall)+')')
	current_batsman.loc[len(current_batsman)+1,'BATTER']=('\nTotal\t\t'+str(score)+' ('+str(wickets)+' wkts, '+ str(current_bowler['O'].sum())+' Ov)')
	
	current_batsman.to_csv('tut08\Scorecard.txt')
	with open('tut08\Scorecard.txt','a') as f:
		writer_object=writer(f)
		writer_object.writerow(fall_wicket)
	current_bowler.loc[len(current_bowler)+1,'BATTER']=''
	current_bowler.loc[len(current_bowler)+1,'BATTER']=''
	current_bowler.loc[len(current_bowler)+1,'BATTER']='Pakistan innings over\n'
	current_bowler.loc[len(current_bowler)+1,'BATTER']=''
	current_bowler.loc[len(current_bowler)+1,'BATTER']=''
	current_bowler.loc[len(current_bowler)+1,'BATTER']='India inning started\n'
	current_bowler.to_csv('tut08\Scorecard.txt',mode='a')

	

	pak_ins=open('tut08\india_inns2.txt','r').read()
	
	splitefile=[]
	for i in pak_ins.split('\n\n'):
		splitefile.append(i)
	line=[]
	for i in range(len(splitefile)):
		line.append(splitefile[i].split(','))
	lx=len(splitefile)
	
	pak_batsman=[]
	ind_bowlers=[]
	pak_inns_ball=[]
	for i in range(len(line)):
		pak_bat= line[i][0].split('to')
		india_bowl=pak_bat[0].split(' ')
		
		pak_batsman.append(pak_bat[1])
		stin=''
		for j in range(len(india_bowl)-1):
			if j==0:
				continue
			else:
				stin=stin+india_bowl[j]+" "
		ind_bowlers.append(stin)
		pak_inns_ball.append(india_bowl[0])
	
	batman_pak_play= list(dict.fromkeys(pak_batsman))
	bowlers_ind_play= list(dict.fromkeys(ind_bowlers))
	current_batsman=pd.DataFrame()
	current_batsman['BATTER']=batman_pak_play
	current_batsman['status']='Not Out'
	current_batsman['R']=current_batsman['B']=current_batsman['4s']=current_batsman['6s']=current_batsman['SR']=0

	current_bowler=pd.DataFrame()
	current_bowler['BOWLER']=bowlers_ind_play
	current_bowler['O']=current_bowler['M']=current_bowler['R']=current_bowler['W']=current_bowler['NB']=current_bowler['WD']=current_bowler['EC']=current_bowler['B']=0
	
	# print(bowlers)
	ext=wide=score=wickets=NoBall=b=lb=0
	fall_wicket=[]
	for i in range(len(line)):
		line[i][1]=line[i][1].lower()
		ind_present_bowler=ind_bowlers[i]
		pak_present_batsmen=pak_batsman[i]
		ball_no=pak_inns_ball[i]
		row_pak_1=0
		row_pak_2=0

		for k in range(len(bowlers_ind_play)):
			if bowlers_ind_play[k]==ind_bowlers[i]:
				row_pak_1=k
				break

		for k in range(len(batman_pak_play)):
			if batman_pak_play[k]==pak_batsman[i]:
				row_pak_2=k
				break
		
		if line[i][1]==' wide':
			wide=wide+1
			score=score+1
			current_bowler.at[row_pak_1,'WD']=current_bowler.at[row_pak_1,'WD']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+1

		elif line[i][1]==' no run':
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1

		elif line[i][1]==' 2 wides':
			wide=wide+2
			score=score+2
			current_bowler.at[row_pak_1,'WD']=current_bowler.at[row_pak_1,'WD']+2
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+2

		elif line[i][1]==' 3 wides':
			wide=wide+3
			score=score+3
			current_bowler.at[row_pak_1,'WD']=current_bowler.at[row_pak_1,'WD']+3
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+3

		elif line[i][1]==' no ball':
			NoBall=NoBall+1
			score=score+1
			
			current_bowler.loc[row_pak_1,'R']=current_bowler.loc[row_pak_1,'R']+1
			current_bowler.loc[row_pak_1,'NB']=current_bowler.loc[row_pak_1,'NB']+1
		
		elif line[i][1]==' four':
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+4
			current_batsman.loc[row_pak_2,'4s']=current_batsman.loc[row_pak_2,'4s']+1
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+4
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			score=score+4

		elif line[i][1]==' six':
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+6
			current_batsman.loc[row_pak_2,'6s']=current_batsman.loc[row_pak_2,'6s']+1
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+6
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			score=score+6

		elif line[i][1]==' 1 run':
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+1
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+1
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			score=score+1

		elif line[i][1]==' 2 runs':
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+2
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+2
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			score=score+2
		
		elif line[i][1]==' 3 runs':
			current_batsman.loc[row_pak_2,'R']=current_batsman.loc[row_pak_2,'R']+3
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+3
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			score=score+3

		
		elif line[i][1]==' byes':
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			if line[i][2]==' 1 run':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+1
				score=score+1

			elif line[i][2]==' 2 runs':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+2
				score=score+2
			elif line[i][2]==' 3 runs':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+3
				score=score+3
			elif line[i][2]==' 4 run' or line[i][2]==' FOUR':
				current_bowler.at[row_pak_1,'R']=current_bowler.at[row_pak_1,'R']+4
				score=score+4

		elif line[i][1]==' leg byes':
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			lb=lb+1
			if line[i][2]==' 1 run':
				score=score+1
			elif line[i][2]==' 2 runs':
				score=score+2
			elif line[i][2]==' 3 runs':
				score=score+3
			elif line[i][2]==' 4 runs' or line[i][2]==' FOUR':
				score=score+4

		

		else:
			current_batsman.loc[row_pak_2,'B']=current_batsman.loc[row_pak_2,'B']+1
			current_bowler.at[row_pak_1,'B']=current_bowler.at[row_pak_1,'B']+1
			add_fall_wicket= str(score)+'-'+str(wickets)+'('+ pak_present_batsmen +','+ball_no+')'
			fall_wicket.append(add_fall_wicket)
			if len(fall_wicket)%4==0:
				fall_wicket.append('\n') 

			wicket_count=line[i][1].split('!')
			if wicket_count[0]==' out lbw':
				current_batsman.loc[row_pak_2,'status']='lbw b '+ind_present_bowler
				current_bowler.at[row_pak_1,'W']=current_bowler.at[row_pak_1,'W']+1
				wickets=wickets+1
			else:	
				if wicket_count[0]==' out bowled':
					current_batsman.loc[row_pak_2,'status']='b'+ind_present_bowler
					current_bowler.at[row_pak_1,'W']=current_bowler.at[row_pak_1,'W']+1
					wickets=wickets+1
				elif wicket_count[0]==' run out':
					current_batsman.loc[row_pak_2,'status']='run out'
					wickets=wickets+1
				else:
					content2=wicket_count[0].split('by')
					current_batsman.loc[row_pak_2,'status']='c'+content2[1]+' b '+ind_present_bowler
					current_bowler.at[row_pak_1,'W']=current_bowler.at[row_pak_1,'W']+1
					wickets=wickets+1

	for i in range (len(current_batsman)):
		
		current_batsman.loc[i,'SR']=round((current_batsman.loc[i,'R']/current_batsman.loc[i,'B'])*100,2)	

	for i in range (len(current_bowler)):
		rem=(current_bowler.at[i,'B']%6)/10	
		val=int(current_bowler.at[i,'B']/6)	
		current_bowler.at[i,'O']=round(val+rem,1)
		current_bowler.at[i,'EC']=round(current_bowler.at[i,'R']/current_bowler.at[i,'O'],2)
	del current_bowler['B']
	
	ext=wide+NoBall+lb+b
	current_batsman.loc[len(current_batsman)+1,'BATTER']=''
	current_batsman.loc[len(current_batsman)+1,'BATTER']=('Extras\t\t'+str(ext)+'(b '+str(b)+', lb '+str(lb)+', w '+str(wide)+', nb '+str(NoBall)+')')
	current_batsman.loc[len(current_batsman)+1,'BATTER']=('\nTotal\t\t'+str(score)+' ('+str(wickets)+' wkts, '+ str(current_bowler['O'].sum())+' Ov)')
	
	current_batsman.to_csv('tut08\Scorecard.txt',mode='a')
	with open('tut08\Scorecard.txt','a') as f:
		writer_object=writer(f)
		writer_object.writerow(fall_wicket)
	# print(25*"A")
	current_bowler.to_csv('tut08\Scorecard.txt',mode='a')
	# del MyBowlers['B']
	
#final code submission

###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

scorecard()
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))

