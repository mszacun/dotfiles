ln ~/dotfiles/aginoodle/secret.py $WORKSPACE/src/backlog/settings/secret.py
ln -s ~/dotfiles/aginoodle/exclude $WORKSPACE/.git/info/exclude
ln -s ~/dotfiles/aginoodle/snippets $WORKSPACE/snippets

sudo pacman -S mariadb gcc
sudo systemctl enable mysqld.service

sudo pip2 install mycli django-extensions

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

