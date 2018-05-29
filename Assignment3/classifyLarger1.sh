mkdir logsDT2
mkdir errDT2
mkdir logsDT2/l
mkdir errDT2/l
mkdir logsDT2/l
mkdir errDT2/l
while true
do
for file in `ls ./dataL2/`
do
mkdir logsDT2/l/$file
mkdir errDT2/l/$file
if [ -d ./dataL2/$file ]; then
cd ./dataL2/$file
for line in `ls ./ | cut -d'.' -f1`
do
    cd ../..
    echo $file $line
    python apply_rule_larger1.py $file $line 1> ./logsDT2/l/$file/$line.log 2> ./errDT2/l/$file/$line.err
    cd dataL2/$file
done
cd ../..
fi
done
done