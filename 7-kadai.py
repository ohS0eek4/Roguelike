import csv
import time
import random
flag=int(1)
mapraw=[]
map=[]
startMes=""
clearMes=""
gameoverMes=""
enenum=int
itemnum=int
npcnum=int

filename=input("読み込むMAP: ")
#filename="map1.csv"#デバッグ用
entitys=[] #[[y,x],HP,AP,added-AP] 0:pl 1:bos 2-:ene
items=[] #[[y,x],addAP]
npcs=[]
class entity():
 yx=[0,0]
 HP=0
 AP=0
 equipment=-1
 name=""
 def set(self,id):
  self.yx=[int(mapraw[mapraw[0][0]+1+id][0]),int(mapraw[mapraw[0][0]+1+id][1])]
  self.HP=int(mapraw[mapraw[0][0]+1+id][2])
  self.AP=int(mapraw[mapraw[0][0]+1+id][3])
  self.name=mapraw[mapraw[0][0]+1+id][4]
  #print(self.name) #デバッグ
class item():
 yx=[0,0]
 addAP=0
 name=""
 def set(self,id):
  self.yx=[int(mapraw[mapraw[0][0]+1+id][0]),int(mapraw[mapraw[0][0]+1+id][1])]
  self.addAP=int(mapraw[mapraw[0][0]+1+id][2])
  self.name=mapraw[mapraw[0][0]+1+id][3]
class npc():
 yx=[0,0]
 serif=""
 name=""
 def set(self,id):
  self.yx=[int(mapraw[mapraw[0][0]+1+id][0]),int(mapraw[mapraw[0][0]+1+id][1])]
  self.serif=mapraw[mapraw[0][0]+1+id][2]
  self.name=mapraw[mapraw[0][0]+1+id][3]

def loadmap():
 f = open(filename, "r",encoding='utf-8')
 reader = csv.reader(f)
 for row in reader:
  mapraw.append(row)
 f.close()
 mapraw[0][0]=int(mapraw[0][0]) #high
 mapraw[0][1]=int(mapraw[0][1]) #weight
 global enenum
 global itemnum
 global npcnum
 global clearMes
 global startMes
 global gameoverMes
 enenum=int(mapraw[0][2])
 itemnum=int(mapraw[0][3])
 npcnum=int(mapraw[0][4])
 startMes=mapraw[0][5]
 clearMes=mapraw[0][6]
 gameoverMes=mapraw[0][7]
 #print(mapraw)　#デバッグ
 for i in range(mapraw[0][0]):
  map.append([])
  for j in range(mapraw[0][1]):
   mapraw[i+1][j]=int(mapraw[i+1][j])
   #print(mapraw[i+1][j]) #デバッグ
   for c in range(10):
    if mapraw[i+1][j]%2==0:
     map[i].append(" ")
    else:
     map[i].append("#")
    mapraw[i+1][j]=int(mapraw[i+1][j]/2)
 for i in range(2+enenum):
  entitys.append(entity())
  entitys[i].set(i)
 for i in range(itemnum):
  items.append(item())
  items[i].set(i+2+enenum)
 for i in range(npcnum):
  npcs.append(npc())
  npcs[i].set(i+2+enenum+itemnum)

def printmap():
 if entitys[0].equipment!=-1:
  print("\033[2K\n%s(プレイヤー)[HP:%d 攻撃力:%d 装備品:%s(追加攻撃力:%d)]"%(entitys[0].name,entitys[0].HP,entitys[0].AP,items[entitys[0].equipment].name,items[entitys[0].equipment].addAP))
 else:
  print("\033[2K\n%s(プレイヤー)[HP:%d 攻撃力:%d 装備品:なし]"%(entitys[0].name,entitys[0].HP,entitys[0].AP))
 for y in range(mapraw[0][0]):
  for x in range(mapraw[0][1]*10):
   print(map[y][x],end="")
   if [y,x]==entitys[1].yx :
    print("\033[D\033[35mB\033[39m",end="")
   for i in range(itemnum):
    if [y,x]==items[i].yx :
     print("\033[D\033[33mI\033[39m",end="")
   for i in range(npcnum):
    if [y,x]==npcs[i].yx :
     print("\033[DN",end="")
   for i in range(enenum):
    if [y,x]==entitys[i+2].yx :
     print("\033[D\033[36mE\033[39m",end="")
   if [y,x]==entitys[0].yx :
    print("\033[D\033[32m@\033[39m",end="")
  if y!=mapraw[0][0]-1:
   print("")
 if flag>0:
  print("\033[%dF" %(mapraw[0][0]+1),end="")
 
def move(changey,changex):
  entitys[0].yx[0]+=changey
  entitys[0].yx[1]+=changex
  printmap()
  time.sleep(0.1)
  if(map[entitys[0].yx[0]][entitys[0].yx[1]]=="#"):
   print("\033[2K目の前は壁だった！")
   entitys[0].yx[0]-=changey
   entitys[0].yx[1]-=changex
  if(entitys[0].yx==entitys[1].yx):
   chacha=entitys[1].HP
   if entitys[0].equipment!=-1:
    entitys[1].HP-=(entitys[0].AP+items[entitys[0].equipment].addAP)
   else:
    entitys[1].HP-=entitys[0].AP
   print("\033[2K%s に攻撃した！ %s の残りHP：%d -> %d"%(entitys[1].name,entitys[1].name,chacha,entitys[1].HP))
   if entitys[1].HP<=0:
    print("\033[2K%s を倒した！"%(entitys[1].name))
    entitys[1].yx=[-1,-1]
    global flag
    flag=0
   else:
    entitys[0].yx[0]-=changey
    entitys[0].yx[1]-=changex
  if entitys[1].yx!=[-1,-1]:
   movebos()
  for i in range(enenum):
   if(entitys[0].yx==entitys[i+2].yx):
    chacha=entitys[i+2].HP
    if entitys[0].equipment!=-1:
     entitys[i+2].HP-=(entitys[0].AP+items[entitys[0].equipment].addAP)
    else:
     entitys[i+2].HP-=entitys[0].AP
    print("\033[2K%s に攻撃した！ %s の残りHP：%d -> %d"%(entitys[i+2].name,entitys[i+2].name,chacha,entitys[i+2].HP))
    if entitys[i+2].HP<=0:
     print("\033[2K%s を倒した！"%(entitys[i+2].name))
     entitys[i+2].yx=[-1,-1]
    else:
     entitys[0].yx[0]-=changey
     entitys[0].yx[1]-=changex
   if entitys[i+2].yx!=[-1,-1]:
    moveene(i)
  for i in range(itemnum):
   if(entitys[0].yx==items[i].yx):
    asdfg=0
    while asdfg==0:
     anscha=input("\033[2K%s(追加攻撃力:%d) を拾った！ 装備しますか?[Y/n]"%(items[i].name,items[i].addAP))
     if anscha=="Y" or anscha=="y" or anscha=="":
      if entitys[0].equipment!=-1:
       cache=items[entitys[0].equipment].addAP
      else:
       cache=0
      entitys[0].equipment=i
      print("\033[2K装備ダメージ変化！　"+str(cache)+"->"+str(items[entitys[0].equipment].addAP))
      asdfg=1
     elif anscha=="N" or anscha=="n":
      print("\033[2K処分した")
      asdfg=1
     else:
      print("\033[2K入力が不正です")
      printmap()
    items[i].yx=[-1,-1]
  for i in range(npcnum):
   if(entitys[0].yx==npcs[i].yx):
    print("\033[2K%s に話しかけた！"%(npcs[i].name))
    entitys[0].yx[0]-=changey
    entitys[0].yx[1]-=changex
    print("\033[2K"+npcs[i].name+": "+npcs[i].serif,sep="")

def moveene(id):
 if (entitys[id+2].yx[0]==entitys[0].yx[0] and (entitys[id+2].yx[1]-1==entitys[0].yx[1] or entitys[id+2].yx[1]+1==entitys[0].yx[1])) or (entitys[id+2].yx[1]==entitys[0].yx[1] and (entitys[id+2].yx[0]-1==entitys[0].yx[0] or entitys[id+2].yx[0]+1==entitys[0].yx[0])):
  kyashu=entitys[0].HP
  entitys[0].HP-=entitys[id+2].AP
  print("\033[2K%s に攻撃された！ %s の残りHP:%d -> %d"%(entitys[id+2].name,entitys[0].name,kyashu,entitys[0].HP))
 else:
  houkou=random.randint(0,3)
  if(houkou==0):
   movee=[-1,0]
  elif(houkou==1):
   movee=[0,-1]
  elif(houkou==2):
   movee=[1,0]
  else:
   movee=[0,1]
  entitys[id+2].yx[0]+=movee[0]
  entitys[id+2].yx[1]+=movee[1]
  if map[entitys[id+2].yx[0]][entitys[id+2].yx[1]]=="#" or entitys[id+2].yx==entitys[1].yx:
   entitys[id+2].yx[0]-=movee[0]
   entitys[id+2].yx[1]-=movee[1]
def movebos():
 if (entitys[1].yx[0]==entitys[0].yx[0] and (entitys[1].yx[1]-1==entitys[0].yx[1] or entitys[1].yx[1]+1==entitys[0].yx[1])) or (entitys[1].yx[1]==entitys[0].yx[1] and (entitys[1].yx[0]-1==entitys[0].yx[0] or entitys[1].yx[0]+1==entitys[0].yx[0])):
  kyashu=entitys[0].HP
  entitys[0].HP-=entitys[1].AP
  print("\033[2K%s に攻撃された！ %s の残りHP:%d -> %d"%(entitys[1].name,entitys[0].name,kyashu,entitys[0].HP))

print("")
loadmap()
print("\033[1m%s\033[0m\n\033[32m@\033[39m:プレイヤー　#:壁　\033[33mI\033[39m:アイテム　\033[36mE\033[39m:エネミー　\033[35mB\033[39m:ボス　N:NCP\n移動:wasd　終了:q　強制終了:Q"%startMes)
printmap()
print("マップ読み込み完了")
printmap()
while flag>0:
 key=input("\033[2K行動：")
 print("\033[1F\033[2K",end="")
 if key=="w":
  move(-1,0)
 if key=="a":
  move(0,-1)
 if key=="s":
  move(1,0)
 if key=="d":
  move(0,1)
 if key=="q":
  key=input("\033[2Kゲームを強制終了しますか？(Y/n)")
  if key=="Y" or key=="y":
   flag=-1
  else:
   print("\033[2Kキャンセルしました")
 if key=="Q":
  flag=-1

 #print(entitys[0].yx) #デバッグ
 if entitys[0].HP<=0:
  flag=-1
  print("\033[2K\033[1mGAME OVER: %s\033[0m"%gameoverMes)
 if flag==0:
  print("\033[2K\033[1mGameClear!: %s\033[0m"%clearMes)

 printmap()



















#隠小話：制作時間七時間、お陰で他の課題が無事昇天。