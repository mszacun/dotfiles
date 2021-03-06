#!/usr/bin/sh

# dotfile instalation script

sudo pacman-mirrors -f 5

sudo pacman -Sy

sudo pacman -S fakeroot base-devel

git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

yay -S zsh tmux tig python2-pip python-pip the_silver_searcher meld xbindkeys fasd dunst qtile ctags \
    geckodriver kitty docker docker-compose networkmanager-openconnect ttf-iosevka ttf-iosevka-term firefox chromium pass \
    python-beautifulsoup4 xorg-xhost npm pass-git-helper firefox-passff-git firefox-tridactyl firefox-tridactyl-native \
    task xlockmore ripgrep fzf-git khal vdirsyncer ruby ipython \
    --noconfirm

sudo pip install selenium webium
sudo pip install git+https://github.com/mszacun/pypass@master

# copy vim configuartion
ln -s ~/dotfiles/vim/vimrc ~/.vimrc 
ln -s ~/dotfiles/vim/vim ~/.vim

# install vundle
git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim -c "PluginInstall" -c "qa"

# install oh-my-zsh
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
ln -s ~/dotfiles/zsh/zshrc ~/.zshrc
mkdir ~/.oh-my-zsh/custom/themes
ln -s ~/dotfiles/zsh/mytheme.zsh-theme ~/.oh-my-zsh/custom/themes

# tmux
ln -s ~/dotfiles/tmux.conf ~/.tmux.conf

# qtile
ln -s ~/dotfiles/qtile ~/.config/qtile

# kitty
mkdir -p ~/.config/kitty/
ln -s ~/dotfiles/kitty.conf ~/.config/kitty/kitty.conf

# ctags
ln -s ~/dotfiles/ctags ~/.ctags

# gitconfig
ln -s ~/dotfiles/git/gitconfig ~/.gitconfig

# git-pass-helper
mkdir -p ~/.config/pass-git-helper/
ln -s ~/dotfiles/git/git-pass-mapping.ini ~/.config/pass-git-helper/git-pass-mapping.ini

# tridactyl
ln -s ~/dotfiles/tridactylrc ~/.tridactylrc

# xbindkeys
ln -s ~/dotfiles/xbindkeysrc ~/.xbindkeysrc

# tig
ln -s ~/dotfiles/git/tigrc ~/.tigrc

# dunst
mkdir -p ~/.config/dunst
ln -s ~/dotfiles/dunst/dunstrc ~/.config/dunst/dunstrc

# khal
mkdir -p ~/.config/khal
ln -s ~/dotfiles/khal/config ~/.config/khal/config
