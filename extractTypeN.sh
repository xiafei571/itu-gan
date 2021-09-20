# network-device-bgpnw2
# physical-infrastructure-bgpnw2
# virtual-infrastructure-bgpnw2
typeN="type9"
file_list="type9time_processed.txt"
data_from="/home/itu/datadisk/dataset/data-for-learning"
data_to="/home/itu/datadisk/gan/data"

mkdir "$data_to/$typeN"
mkdir "$data_to/$typeN/network"
mkdir "$data_to/$typeN/physical"
mkdir "$data_to/$typeN/virtual"
c=1
for file_name in `cat $file_list`
do
  echo "moving $c $file_name"
  cp $data_from/network-device-bgpnw2/$file_name $data_to/$typeN/network/
  cp $data_from/physical-infrastructure-bgpnw2/$file_name $data_to/$typeN/physical/
  cp $data_from/virtual-infrastructure-bgpnw2/$file_name $data_to/$typeN/virtual/
  ((c++))
done