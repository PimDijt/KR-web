for line in `cat ./md5hashes.txt`
do
echo $line
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line
mv $line ../data/$line.nt
done
