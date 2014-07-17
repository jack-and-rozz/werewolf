import random

def sum(a,b):
    sum = 0;
    for i in range(a,b):
        sum += i
    return sum


def sumlist(l):
    sum = 0;
    for i in l:
        sum+= i;
    return sum

def my_range(a, b):
    l = [];
    if a==b:
        return []
    else:
        l = my_range(a+1,b)
        l.insert(0,a)
        return l
    

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def norm2(self):
        return self.x * self.x + self.y*self.y

#print sumlist([2,4,6]);
#print my_range(2,5)
#p = Point(2,3)
#print p.norm2()


class ClosedShape:
    def __init__(self):
        self.fill = ""
        self.stroke = ""
    def set_fill(self,color):
        self.fill = color
    def set_stroke(self,color):
        self.stroke = color
 


class Circle(ClosedShape):
    def __init__(self,cx,cy,r):
        ClosedShape.__init__(self)
        self.cx = cx
        self.cy = cy
        self.r = r
    def to_svg(self): 
        return  ' <circle cx="%d" cy="%d" r="%d" stroke="%s" fill="%s"/>' % (self.cx,self.cy,self.r,self.stroke,self.fill)


class Rect(ClosedShape):
    def __init__(self,x,y,w,h):
        ClosedShape.__init__(self)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    def to_svg(self): 
        return  '<rect x="%d" y="%d" width="%d" height="%d" stroke="%s" fill="%s"/>' % (self.x,self.y,self.width,self.height,self.stroke,self.fill)
 

"""
c = Circle(30,20,10)
c.set_stroke("red")
c.set_fill("red")
c.set_fill("yellow")
print c.to_svg()
"""




def swap(l,i,j):
    tmp = l[i]
    l[i] = l[j]
    l[j] = tmp
    return l


def partition(l,a,b):
    pivot = l[(a+b)/2]
    if len(l) <= 1:
       return l
    while(1):
        while(l[a] < pivot ):
            a+=1
        while(l[b] > pivot) :
            b-=1
        if a >= b:
            break
        if l[a] == l[b]:
            a+=1
        swap(l,a,b)
    return a



def qs(l):
    if len(l) > 1:
        p = partition(l,0,len(l)-1)
        lcpy = qs(l[0:p])+[l[p]] + qs(l[p+1:len(l)])
        for i in range(0,len(l)):
            l[i] = lcpy[i]
        return l
    elif len(l) == 1:
        return l
    else:
        return []

import random

def random_ints(maxint,n):
    l = []
    for i in range(n):
        l.append(random.randint(0,maxint-1))
    return l



def check_sorted(l):
    for i in range(0,len(l)-1):
        if l[i] > l[i+1]:
            return 0
    return 1
    

def test_qs(n):
    l = random_ints(n,n)
    return check_sorted(qs(l))

import time

def measure_qs(n):
    l = random_ints(n,n)
    t1 = time.clock()
    qs(l)
    t2 = time.clock()
    if  check_sorted(l)== 1:
        print "OK %d elems in %f sec" % (n,t2-t1)
    else : 
        print "NG sort failed"

measure_qs(100000)
#print test_qs(1000)







