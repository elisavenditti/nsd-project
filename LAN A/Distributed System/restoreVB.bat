VBoxManage controlvm Lubuntu-av-4 poweroff
echo "1"
VBoxManage snapshot Lubuntu-av-4 restore safe-env
echo "2"
VBoxManage startvm Lubuntu-av-4 --type emergencystop
echo "3"