ln ~/dotfiles/aginoodle/secret.py $WORKSPACE/src/backlog/settings/secret.py
ln -s ~/dotfiles/aginoodle/exclude $WORKSPACE/.git/info/exclude
ln -s ~/dotfiles/aginoodle/snippets $WORKSPACE/snippets
ln -s ~/dotfiles/aginoodle/hooks/pre-push $WORKSPACE/.git/hooks

yaourt -S mysql gcc php56 pandoc
sudo systemctl enable mysqld.service

sudo pip2 install mycli django-extensions pdbpp

wget https://bitbucket.org/georgelewe/teamcal-pro/downloads/tcpro_36019.zip
mkdir ~/teamcal
unzip tcpro_36019.zip -d ~/teamcal
echo "create database teamcal" | /usr/bin/mysql -u root
echo "create database tcpro" | /usr/bin/mysql -u root
read -p "Uncomment mysql libraries in php.ini [Enter]"
php56 -t ~/teamcal -S 127.0.0.1:4000&
sleep 2
curl 'http://127.0.0.1:4000/installation.php' -H 'Host: 127.0.0.1:4000' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://127.0.0.1:4000/installation.php' -H 'Connection: keep-alive' --data 'txt_instAppRelDir=%2F&txt_instAppURL=http%3A%2F%2F127.0.0.1%3A4000%2F&txt_instDbServer=127.0.0.1&txt_instDbName=teamcal&txt_instDbUser=root&txt_instDbPassword=&txt_instDbPrefix=my_&opt_data=none&chkLicGpl=chkLicGpl&chkLicTcpro=chkLicTcpro&btn_install=Install'

# install arc
mkdir ~/bin
cd ~/bin
git clone https://github.com/phacility/libphutil.git
git clone https://github.com/phacility/arcanist.git
echo ‘export PATH="$PATH:~/bin/arcanist/bin"’ >> ~/.bashrc
cd ~/bin/libphutil
git apply ~/dotfiles/aginoodle/arc_fix_patch.diff
cd $WORKSPACE
~/bin/arcanist/bin/arc install_certificate

