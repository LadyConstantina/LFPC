# -*- coding: utf-8 -*-
"""LFPC4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ke8bGJxx4VZ7JTG5V5kv6b03KulzZrCJ
"""

import string

cases_binary=[]

#Returns the list of non-Terminals that -> ε
def empties(G):
    empty_nonT = []
    for key in G:
      for value in G[key]:
        if value == "_":
          empty_nonT.append(key)
    return empty_nonT


#Returns the derivations for non_terminal -> ε
def substrings(char,Str):
    #Case: If S->A and A->ε then S->ε
    if Str == char :
      return ['_']
    sub = []
    S1 = Str
    S1 = S1.replace(char,'',1)
    sub.append(S1) #Case; AaAb turns in aAb
    if S1.find(char) != -1:
      pos = S1.find(char)+1
      S1 = Str[:pos] + Str[pos+1:]
      sub.append(S1) #Case; AaAb turns in Aab
      S1=Str.replace(char,'',2)
      sub.append(S1) #Case; AaAb turns in ab
    return sub

#Returns list with tuples where key->value is unitary production
def unitaries(G):
    unit_prod = []
    for key in G:
      for value in G[key]:
        if len(value)==1 and ord('A') <= ord(value) <= ord('Z'):
          unit_prod.append((key,value))
    
    return unit_prod

def reached(list):
    rec=[]
    for value in list:
      for i in range(0,len(value)):
        if ord('A') <= ord(value[i]) <= ord('Z') and value[i] not in rec:
          rec.append(value[i])
    return rec

def new_val(val,Y):
  l=len(val)
  if l==1:
    return val,Y
  elif l==2:
    if val not in Y:
      Y.append(val)
    i=Y.index(val)
    val='Y'+str(i+1)
    return val,Y
  elif l>2:
    val1=val[:l//2]
    val2=val[(l//2):]
    val1,Y = new_val(val1,Y)
    val2,Y = new_val(val2,Y)
    val=val1+val2
    return val,Y

def new_val2(val,let,M):
  l=len(val)
  if l==2:
    return val,M
  elif l==4:
    if val not in M:
      M.append(val)
    i=M.index(val)
    val2=let+str(i+1)
    return val2,M
  elif l>4:
    val1=val[:(l//4)+3]
    val2=val[(l//4)+3:]
    val1,M = new_val2(val1,let,M)
    val2,M = new_val2(val2,let,M)
    val=val1+val2
    return val,M

class Chomsky():

    #Initialization function
    def __init__(self,file):
      with open(file) as f:
          input_lines = f.read().split('\n')

      #Defining variables
      self.non_terminal = list(input_lines[0].split())
      self.terminal = list(input_lines[1].split())

      self.available_letters=list(string.ascii_uppercase)
      for char in self.non_terminal:
        self.available_letters.remove(char)
      
      self.P = {}
      self.new_value = False

      #Reading the Grammar
      for line in input_lines[2 : ]:
          key, value = line.split()

          #See if we need S1 -> S
          if value.find('S') >= 0 :
              self.new_value = True

          if key in self.P:
              self.P[key].append(value)
          else:
              self.P[key] = [ value ]
      
      #Chomsky Normal Form transformations
    def Chomsky_normal(self):
      print('Initial state:')
      self.print()
      print('After Step 1:')
      self.Step1()
      self.print()
      print('After Step 2:')
      self.Step2()
      self.print()
      print('After Step 3:')
      self.Step3()
      self.print()
      print('After Step 4:')
      self.Step4()
      self.print()
      print('After Step 5:')
      self.Step5()
      self.print()

      #Add S1 -> S if needed    
      #if self.new_value :
      #  self.P['S1'] = ['S']

    #Printing the Grammar
    def print(self):
        print('P={')
        for key in self.P:
          print(key,'-> ',end='')
          i=0
          for value in self.P[key]:

            if i>=1:
              print('|',end='')

            #Replacing _ with ε symbol
            if value == '_':
                print('ε',end='')
                i+=1
            else:
                print(value+'',end='')
                i+=1

          print()
        print('}')

    #Step 1: Eliminating empty strings
    def Step1(self):

        #Getting the list of non-Terminals that -> ε
        e_list = empties(self.P)

        for char in e_list:
          self.P[char].remove("_") #Removing the -> ε
          for key in self.P:
            new_str=[]
            for value in self.P[key]:
              if value.find(char) != -1:
                #Adding the derivations for non-Terminal -> ε to a list
                new_str.extend(substrings(char,value))
            
            self.P[key].extend(new_str) #Adding the list to grammar
            self.P[key]=list(set(self.P[key])) #Eliminating copies
        
        #If we have new empties, we recall Step 1
        if len(empties(self.P)) > 0 :
          self.Step1()
    
    #Step 2: Eliminating unitary productions
    def Step2(self):

      #Getting the list of tuples where key->value is unitary production
      un_list=unitaries(self.P)

      for key1,key2 in un_list:
        #Remove the unitary production
        self.P[key1].remove(key2)
        #Add all the productions of the unit eliminated
        self.P[key1].extend(self.P[key2]) 
        #Eliminate copies
        self.P[key1]=list(set(self.P[key1]))

      #If we have new unitary productions, we recall Step 2
      if len(unitaries(self.P)) > 0 :
          self.Step2()
    
    #Step 3: Remove unreachable non-Terminals
    def Step3(self):
      
      #We start with S so S is reachable
      reachable=['S']

      for key in self.non_terminal:
          #For each non-T we get the list of keys we can reach 
          #and add them to reachable
          reachable.extend(reached(self.P[key]))
      
      #Eliminate the copies
      reachable=list(set(reachable))

      #Remove the keys that are not in reachable list
      for key in self.non_terminal:
        if key not in reachable:
          del self.P[key]
          self.non_terminal.remove(key)

    #Step 4: Remove unproductive non-Terminals
    def Step4(self):
      
      productive=['S']
      non_productive =list(self.P.keys())
      non_productive.remove('S')
      
      #Case non-terminal -> terminal => productive
      for key in non_productive:
        for value in self.P[key]:
          if len(value) == 1 and value in self.terminal:
            productive.append(key)
            non_productive.remove(key)
            break

      #Case non-terminal -> productive non-terminal [+ terminal] => productive
      prod = False
      for key in non_productive:
        for value in self.P[key]:
          for i in range(0,len(value)):
            if value[i] == key:
              prod=False
              break
            elif value[i] in productive:
              prod=True
          if prod:
            productive.append(key)
            non_productive.remove(key)
            break
        else:
          break
  
      #Elimination of non-productive
      for key in non_productive:
        del self.P[key]
        for key2 in productive:
          for value in self.P[key2]:
            if value.find(key) != -1:
              self.P[key2].remove(value)

    #Step 5: Chomsky normal form 
    def Step5(self):
      self.X = self.terminal
      self.Y = []
      for key in self.P:
        j=0
        for value in self.P[key]:
          if len(value) > 2:
            value, self.Y = new_val(value,self.Y)
          self.P[key][j]=value
          j=j+1
      
      for i in range(0,len(self.Y)):
        self.P['Y'+str(i+1)] = [self.Y[i]]

      j=0
      for key in self.P:
        j=0
        for value in self.P[key]:
          if len(value) > 1:
            value2=value
            k=0
            for i in range(0,len(value)):
              if value[i] in self.X:
                value2=value2[:i+k]+'X'+str(self.X.index(value[i])+1)+value2[i+k+1:]
                k+=1
            self.P[key][j]=value2
          j+=1

      for i in range(0,len(self.X)):
        self.P['X'+str(i+1)] = [self.X[i]]

      need_step_2=False
      for key in self.P:
        for value in self.P[key]:
          if len(value)>4:
            need_step_2=True
            break

      if need_step_2:
        self.available_letters.remove('X')
        self.available_letters.remove('Y')
        self.Step5_2()
    
    #Step 5 part 2
    def Step5_2(self):
      lr=self.available_letters[0]
      self.available_letters.remove(lr)
      self.extra=[]
      for key in self.P:
        j=0
        for value in self.P[key]:
          if len(value) > 4:
            value,self.extra = new_val2(value,lr,self.extra)
          self.P[key][j]=value
          j=j+1
      
      for i in range(0,len(self.extra)):
        self.P[lr+str(i+1)] = [self.extra[i]]

      need_step_2=False
      for key in self.P:
        for value in self.P[key]:
          if len(value)>4:
            need_step_2=True
            break

      if need_step_2:
        self.Step5_2()

G = Chomsky('grammar.txt')
G.Chomsky_normal()