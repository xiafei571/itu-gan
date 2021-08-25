# network-device-bgpnw2
# physical-infrastructure-bgpnw2
# virtual-infrastructure-bgpnw2

mkdir "./type3"
mkdir "./type3/network-device-bgpnw2"
mkdir "./type3/physical-infrastructure-bgpnw2"
mkdir "./type3/virtual-infrastructure-bgpnw2"
count=0
for file_name in `cat type3time_processed.txt`
do
  echo "moving $c $file_name"
  cp ./network-device-bgpnw2/$file_name ./type3/network-device-bgpnw2/
  cp ./physical-infrastructure-bgpnw2/$file_name ./type3/physical-infrastructure-bgpnw2/
  cp ./virtual-infrastructure-bgpnw2/$file_name ./type3/virtual-infrastructure-bgpnw2/
  ((c++))
done