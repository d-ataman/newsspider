set +x
dir=/home/ataman/PycharmProjects/paralleldata/crawledsites
outdir=/home/ataman/PycharmProjects/paralleldata/crawledsites/aligned-entr-2
hunalign=/home/ataman/Documents/software/hunalign-1.2/src/hunalign/hunalign

outputfile=$outdir/bianet-entr.txt
scp null.dict $outputfile
for file in $dir/*en.txt;
do
id=`echo $file |  cut -c 56-61`
echo "$id -> $file"
$hunalign -text null.dict $dir/$id-en.txt $dir/$id-tr.txt > $outdir/$id-alignment.txt
if [ -s $outdir/$id-alignment.txt ]
then
    cut -f1,2 $outdir/$id-alignment.txt > $outdir/$id-entr.txt
    # Remove Empty Lines
    sed -i '/^$/d' $file | sed -i '/^ *$/d' | sed -i '/^\t*$/d'  $outdir/$id-entr.txt
    cat $outdir/$id-entr.txt >> $outputfile
fi
rm $outdir/$id-alignment.txt
done
