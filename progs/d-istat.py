import sys
import argparse
import numpy as np
from scipy.stats import t
pop={"Lombardia": 10103969,"Lazio": 5865544,"Campania": 5785861,"Sicilia": 4968410, \
    "Veneto": 4907704,"Emilia-Romagna": 4467118,"Piemonte": 4341375,"Puglia": 4008296, \
    "Toscana": 3722729,"Calabria": 1924701,"Sardegna": 1630474,"Liguria": 1543127, \
    "Marche": 1518400,"Abruzzo": 1305770,"Friuli-Venezia Giulia": 1211357, \
    "Trentino-Alto Adige": 1074819,"Umbria": 880285,"Basilicata": 556934,"Molise": 302265, \
    "Valle d'Aosta": 125501,"Italy": 60244639}
month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


def cound_istat(filename, ypos, region, months, years, ages, pr=2, pa=7, pd=8):
	d={}
	sp=years[0]
	tp=years[1]
	tm=months[1]-months[0]+1
	ty=years[1]-years[0]+1
	if region=='Italy': d['Italy']=np.zeros((12,ty))
	lines=open(filename).readlines()[1:]
	for line in lines:
		v=line.rstrip().split(',')
		r=v[pr].split('/')[0]
		ac=int(v[pa])
		if ac<ages[0] or ac>ages[1]: continue
		if region!='Italy' and r!=region: continue
		m=int(v[pd][:2])
		d[r]=d.get(r,np.zeros((12,ty)))
		if len(v)<tp: 
			print >> sys.stderr,'ERROR',line.rstrip()
			continue
		for j in range(sp,tp):
			if v[j]=='n.d.': continue
			d[r][m-1][j-sp]+=int(v[j])
			if region=='Italy': d['Italy'][m-1][j-sp]+=int(v[j])
		if v[ypos]=='n.d.': continue
		d[r][m-1][-1]+=int(v[ypos])
		if region=='Italy': d['Italy'][m-1][-1]+=int(v[ypos])
	return d



def print_stat(d,months,ty,ry=0,start=2011):
	tm=months[1]-months[0]+1
	hy='\t'.join([str(start+i) for i in range(ty)])+'\tNEW'
	print 'Regione\tMese\t'+hy+'\tDELTA\tMAX\tDMAX\tPROB\tPERCENT'
	regs=d.keys()
	if 'Italy' in regs:
		regs.remove('Italy')
		regs.append('Italy')
	for preg in regs:
		okreg=preg.replace(' ','-')
		ld=d[preg]
		#print d[preg]
		vold=ld[:,:ty-ry]
		#print vold
		m=np.max(vold)
		for i in range(tm):
			ldi=ld[i,:]
			vmax=np.max(ldi[:ty-ry])
			am=start+np.argmax(ldi[:ty-ry])
			m=np.mean(ldi[:ty-ry])
			s=np.std(ldi[:ty-ry])
			delta=(ldi[-1]-m)
			dm=(ldi[-1]-vmax)
			zscore=(ldi[-1]-m)/s
			p=t.sf(ldi[-1],ty-1,m,s)
			print '%s\t%s\t%s\t%.0f\t%d\t%.0f\t%.3e\t%.3e' %(okreg,month[months[0]-1+i],'\t'.join(['%.0f' %l  for l in ldi]),delta,am,dm,p,100*delta/float(pop[preg]))
		v6m=np.zeros(ty+1)
		for i in range(ty+1):
			v6m[i]=np.sum(ld[0:tm,i])
		vmax=np.max(v6m[:ty-ry])
		m=np.mean(v6m[:ty-ry])
		am=start+np.argmax(v6m[:ty-ry])
		s=np.std(v6m[:ty-ry])
		delta=v6m[-1]-m
		dm=v6m[-1]-vmax
		zscore=(v6m[-1]-m)/s
		p=t.sf(v6m[-1],ty-1,m,s)
		print '%s\t%s\t%s\t%.0f\t%d\t%.0f\t%.3e\t%.3e' %(okreg,'SUM','\t'.join(['%.0f' %l for l in v6m]),delta,am,dm,p,100*delta/float(pop[preg]))



def get_options():
	parser = argparse.ArgumentParser(description='Parse istat data.')
	parser.add_argument('filename', type=str, help='file csv from istat')
	parser.add_argument('ypos', type=int ,help='Column Year')
	parser.add_argument('-r','--region', type=str, dest='region',help='Region name')
	parser.add_argument('--sm','--start-month', type=int, dest='smonth',help='Starting month')
	parser.add_argument('--em','--end-month', type=int, dest='emonth',help='Ending month')
	parser.add_argument('--sy','--start-year', type=int, dest='syear',help='Starting year column')
	parser.add_argument('--ey','--end-year', type=int, dest='eyear',help='Ending year column')
	parser.add_argument('--sa','--start-age', type=int, dest='sage',help='Starting age')
	parser.add_argument('--ea','--end-age', type=int, dest='eage',help='Ending age')
	args = parser.parse_args()
	region='Italy'
	months=[1,12]
	years=[31,40]
	ages=[0,22]
	filename=args.filename
	ypos=args.ypos-1
	if args.region: region=args.region
	if args.smonth: months[0]=args.smonth
	if args.emonth: months[1]=args.emonth
	if args.syear: years[0]=args.syear-1
	if args.eyear: years[1]=args.eyear
	if args.sage: ages[0]=args.sage/5
	if args.eage: ages[1]=args.eage/5-1
	return filename, ypos, region, months, years, ages




if __name__ == '__main__':
	filename, ypos, region, months, years, ages = get_options()
	#total year
	#ty=11
	#total months
	#tm=5
	pr=2
	pa=7
	pd=8
	#filename=sys.argv[1]
	if len(sys.argv) >3:
		ty=int(sys.argv[2])
		#tm=int(sys.argv[3])
	d=cound_istat(filename, ypos, region, months, years, ages, pr, pa, pd)
	print_stat(d,months,years[1]-years[0])



