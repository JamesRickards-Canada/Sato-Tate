import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons

def shifthist(j):
		v=[0, 0, 0, 1, 1, 2, 3, 3, 4, 6, 7, 9, 13, 16, 22, 29, 37, 51, 66, 88, 116, 159, 212, 287, 387, 518, 709, 958, 1304, 1765, 2408, 3284, 4487, 6156, 8401, 11527, 15821, 21731, 29858, 41072, 56538, 77831, 107364, 148010, 204349, 282251, 389869, 539107, 745724, 1032043, 1428850, 1979315]
		return(v[j-1]-v[2*j-1])

#Used to save the histograms for good.
def savetohists():
	primespi=np.loadtxt('primepilist.txt',dtype='int')
	newprimespi=[1, 2, 5, 8, 15, 26, 45, 78, 142, 255, 458, 840, 1537, 2841, 5258, 9799, 18345, 34472, 65048, 122977, 233390, 443883, 846074, 1616634, 3095334, 5936302]
	file,name,minp,maxp=('rk0CMoverCMlist.txt','e6/',8,26)
	x=np.loadtxt(file,dtype='float')
	for n in range(minp,maxp+1):
		lim=newprimespi[n-1]
		nbins=math.floor(2*math.pow(lim,1/3))
		hist,bins=np.histogram(x[0:lim],bins=nbins)
		hist[0]=hist[0]+shifthist(n)
		np.save(name+str(n)+'hist',hist)
		np.save(name+str(n)+'bins',bins)
	'''
	for c in range(1,7):
		if c==1:
			file,name,minp,maxp=('rk0CMlist.txt','e1/',8,26)
		elif c==2:
			file,name,minp,maxp=('rk0noCMlist.txt','e2/',8,26)
		elif c==3:
			file,name,minp,maxp=('rk1noCMlist.txt','e3/',8,26)
		elif c==4:
			file,name,minp,maxp=('rk4noCMlist.txt','e4/',8,26)
		elif c==5:
			file,name,minp,maxp=('rk14noCMlist.txt','e5/',8,26)
		elif c==6:
			file,name,minp,maxp=('rk0CMoverCMlist.txt','e6/',8,26)
		x=np.loadtxt(file,dtype='float')
		for n in range(minp,maxp+1):
			lim=primespi[n-1]
			nbins=math.floor(2*math.pow(lim,1/3))
			hist,bins=np.histogram(x[0:lim],bins=nbins)
			np.save(name+str(n)+'hist',hist)
			np.save(name+str(n)+'bins',bins)
	'''	
	
class Index(object):
	def __init__(self,p):
		self.radiodict={'Rk 0, CM': 0, 'Rk 0, no CM': 1, 'Rk 1, no CM': 2,'Rk 4, no CM': 3,'Rk 14, no CM': 4,'Rk 0, CM over CM': 5,'Rk 1, CM over CM': 6}
		self.radiodict2={'Show expected': True, 'Hide expected':False}
	
	def next(self, event):
		p.update(-1,1,-1)

	def prev(self, event):
		p.update(-1,-1,-1)
		
	def radiocurve(self,label):
		p.update(self.radiodict[label],0,-1)
		
	def curveshow(self,label):
		p.update(-1,0,self.radiodict2[label])
	
class plotmaker(object):
	def __init__(self):
		#Initializing figure and position
		self.fig=plt.figure(figsize=(10,7.1))
		self.ax=self.fig.add_subplot(111)
		self.ax.set_position([0.06,0.285,0.9,0.6])
		#Loading primepi(2^n) for 0<=n<=34
		self.primespi=np.loadtxt('primepilist.txt',dtype='int')
		#Initializeing the histograms and the maximum values of y for the display of the histograms
		self.hists=[[0 for j in range(maxp-minp+1)] for i in range(ncurves)]
		self.ymaxs=[0 for i in range(ncurves)]
		self.tstarts=['Elliptic curve '+r'$y^2=x^3-x$'+' over '+r'$\mathbb{Q}$'+'\n Rank 0, CM for ', 'Elliptic curve '+r'$y^2+y=x^3-x^2$'+' over '+r'$\mathbb{Q}$'+'\n Rank 0, no CM for ', 'Elliptic curve '+r'$y^2+y=x^3-x$'+' over '+r'$\mathbb{Q}$'+'\n Rank 1, no CM for ', 'Elliptic curve '+r'$y^2+xy=x^3-x^2-79x+289$'+' over '+r'$\mathbb{Q}$'+'\n Rank 4, no CM for ','Elliptic curve '+r'$y^2+y=x^3-2248232106757x+1329472091379662406$'+' over '+r'$\mathbb{Q}$'+'\n Rank 14, no CM for ','Elliptic curve '+r'$y^2=x^3-x$'+' over '+r'$\mathbb{Q}[i]$'+'\n Rank 0, CM by '+r'$\mathbb{Z}[i]$ for ', 'Elliptic curve '+r'$y^2+y=x^3+1$'+' over '+r'$\mathbb{Q}[\sqrt{-3}]$'+'\n Rank 1, CM by '+r'$\mathbb{Z}[\frac{1+\sqrt{-3}}{2}]$ for ']
		for i in range(1,ncurves+1):
			fstart='e'+str(i)+'/'
			for j in range(minp,maxp+1):
				#Remaking the histograms from the saved np.histogram data
				bins=np.load(fstart+str(j)+'bins.npy')
				hist=np.load(fstart+str(j)+'hist.npy')
				width=bins[1]-bins[0]
				center=(bins[:-1]+bins[1:])/2
				scaledhist=hist/(width*sum(hist))
				self.hists[i-1][j-8]=self.ax.bar(center,scaledhist,width=width, visible=False,facecolor='g')
				#self.ymaxs[i-1]=max(self.ymaxs[i-1],max(scaledhist)*1.05)
				if j==maxp:
					self.ymaxs[i-1]=max(scaledhist)*1.2
		self.ymaxs[0]=2
		self.ymaxs[5]=2
		self.ymaxs[6]=2
		#Setting the initial histogram to be visible
		for i in self.hists[0][0]:
			i.set_visible(True)
		self.curhist=[0,0] #[ecurve,prime]
		#Initializing the Sato-Tate distribution curves
		#No CM, CM over CM, CM over Q main part
		self.plotdict=[2, 0, 0, 0, 0, 1,1]
		self.stplot=[0,0,0]
		
		self.stx=np.arange(-2.001,2.001,0.001)
		self.stnoCM=(1/(2*np.pi))*np.power(np.abs((4-np.power(self.stx,2))),1/2)
		self.stnoCM[0]=0
		self.stnoCM[-1]=0
		self.stx1=np.arange(-1.9999,1.9999,0.0001)
		self.stCMCM=(1/(np.pi))*np.power(np.abs((4-np.power(self.stx1,2))),-1/2)
		
		self.stplot[0]=self.ax.plot(self.stx,self.stnoCM,visible=False,color='r')[0]
		self.stplot[1]=self.ax.plot(self.stx1,self.stCMCM,visible=False,color='r')[0]
		self.stplot[2]=self.ax.plot(self.stx1,self.stCMCM/2,visible=False,color='r')[0]
		
		self.showexpected=False
		self.ax.set_ylim(bottom=0,top=self.ymaxs[self.curhist[0]])
		self.ax.set_title(self.tstarts[0]+r' $p\leq 2^{%d}$'%(minp)+' with %d primes'%(self.primespi[minp-1]))
	
	def update(self,ecup,pup,expected):
		#ecup is elliptic curve update, pup is prime update. ecup=-1 means no update, expected is the expected sato-tate curve update; -1 means no update	
		if expected!=-1:
			self.showexpected=expected
		for i in self.hists[self.curhist[0]][self.curhist[1]]:
			i.set_visible(False)
		if ecup!=-1:
			self.curhist[0]=ecup			
		self.curhist[1]=(self.curhist[1]+pup)%(maxp-minp+1)
		for i in self.hists[self.curhist[0]][self.curhist[1]]:
			i.set_visible(True)
		self.ax.set_ylim(bottom=0,top=self.ymaxs[self.curhist[0]])
		for i in self.stplot:
			i.set_visible(False)
		self.stplot[self.plotdict[self.curhist[0]]].set_visible(self.showexpected)
		self.ax.set_title(self.tstarts[self.curhist[0]]+r'$p\leq 2^{%d}$'%(self.curhist[1]+8)+' with %d primes'%(self.primespi[self.curhist[1]+7]))
		plt.draw()

if __name__=='__main__':
	minp=8
	maxp=26
	ncurves=7
	p=plotmaker()
	callback = Index(p)
	axprev = plt.axes([0.22, 0.02, 0.07, 0.075])
	axnext = plt.axes([0.30, 0.02, 0.07, 0.075])
	bnext = Button(axnext, 'Next')
	bnext.on_clicked(callback.next)
	bprev = Button(axprev, 'Previous')
	bprev.on_clicked(callback.prev)
	axcolor = 'lightgoldenrodyellow'
	rax = plt.axes([0.01, 0.02, 0.20, 0.22], facecolor=axcolor)
	radio = RadioButtons(rax, ('Rk 0, CM', 'Rk 0, no CM', 'Rk 1, no CM','Rk 4, no CM','Rk 14, no CM','Rk 0, CM over CM','Rk 1, CM over CM'))
	radio.on_clicked(callback.radiocurve)
	rax2 = plt.axes([0.22,0.11,0.15,0.13], facecolor=axcolor)
	radio2 = RadioButtons(rax2, ('Show expected', 'Hide expected'))
	radio2.set_active(1)
	radio2.on_clicked(callback.curveshow)
	plt.show()