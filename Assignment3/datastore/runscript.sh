for line in `cat ./md5hashes.txt`
do
echo $line
if [ ! -f ../data/$line.nt ]; then
wget http://download.lodlaundromat.org/$line
mv $line $line.gz
gunzip $line.gz
mv $line ../data/$line.nt
<<<<<<< HEAD
#cd ..
#python parse_data.py
#cd datastore
fi
=======
cd ..
python parse_data.py $line
cd datastore
>>>>>>> d6fda174fd7c966c9e7e0282abacbf5cbb3a76c2
done
