mkdir ../logsDT
mkdir ../errDT
mkdir ../logsDT/l
mkdir ../errDT/l
mkdir ../logsDT/l
mkdir ../errDT/l
cd ..
for file in `ls ./dataL/`
do
mkdir logsDT/l/$file
mkdir errDT/l/$file
cd ./dataL/$file
for line in `ls ./`
do
    cd ../..
    echo $file $line
    ls=`ls`
    echo $ls
    python apply_rule_larger.py $file $line 1> ./logsDT/l/$file/$line.log 2> ./errDT/l/$file/$line.err
done
cd ..
done