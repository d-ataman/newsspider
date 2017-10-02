dir=/home/ataman/PycharmProjects/paralleldata/crawledsites

for file in $dir/*.html;
do
echo "Preprocessing..."
echo "$file"

# Remove Empty Lines
sed '/^$/d' $file | sed '/^ *$/d' > $file.1
# Remove the 1st line
sed '1d' $file.1 > $file.2
# Separate all sentences to different lines
#sed 's/[a-zA-Z]\. /\.\n/g' $file.2 > $file.3
rm $file $file.1
id=`echo $file.2 |  cut -c 56-64`
#echo $id
mv $file.2 $dir/$id.txt
done
