VBoxManage controlvm Lubuntu6-big poweroff
VBoxManage controlvm Lubuntu7 poweroff
VBoxManage controlvm Lubuntu8 poweroff
echo "1"
VBoxManage snapshot Lubuntu6-big restore safe4-env
VBoxManage snapshot Lubuntu7 restore safe4-env
VBoxManage snapshot Lubuntu8 restore safe4-env
echo "2"