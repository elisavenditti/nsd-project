VBoxManage controlvm Lubuntu-av-6 poweroff
echo "1"
VBoxManage snapshot Lubuntu-av-6 restore safe3-env
echo "2"