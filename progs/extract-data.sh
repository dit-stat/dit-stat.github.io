#!/bin/bash

for i in `seq 5 5 110`; 
do 
   b=`echo $i-5|bc`; 
   python ./d-istat.py $1 41  -r Italy  --sa $b  --ea $i |tail -n +2 |awk -v OFS=","  -v a=$i '{for (i=3;i<=12;i++) {print $1,$2,$i,2011+i-3,a}}' |grep -v SUM ; 
done

for i in `seq 5 5 110`;
do
   b=`echo $i-5|bc`;
   python ./d-istat.py $1 42  -r Italy  --em 5 --sa $b  --ea $i |tail -n +2 |awk -v OFS=","  -v a=$i '{for (i=3;i<=12;i++) {print $1,$2,$i,2011+i-2,a}}' |grep -v SUM;
done
