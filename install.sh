#!/usr/bin/sh

# dotfile instalation script

sudo pacman-mirrors -f 5

sudo pacman -Sy

sudo pacman -S fakeroot base-devel

git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

yay -S zsh tmux tig python2-pip python-pip xbindkeys fasd dunst qtile ctags gvim xclip \
    geckodriver kitty docker docker-compose networkmanager-openconnect ttf-iosevka ttf-iosevka-term firefox chromium pass \
    python-beautifulsoup4 xorg-xhost npm pass-git-helper firefox-passff-git firefox-tridactyl firefox-tridactyl-native \
    task timew xlockmore ripgrep fzf-git khal vdirsyncer ruby ipython \
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
ln -s -f ~/dotfiles/zsh/zshrc ~/.zshrc
mkdir -p ~/.oh-my-zsh/custom/themes
ln -s -f ~/dotfiles/zsh/mytheme.zsh-theme ~/.oh-my-zsh/custom/themes

# tmux
ln -s -f ~/dotfiles/tmux.conf ~/.tmux.conf

# qtile
ln -s -f ~/dotfiles/qtile ~/.config/qtile

# kitty
mkdir -p ~/.config/kitty/
ln -s -f ~/dotfiles/kitty.conf ~/.config/kitty/kitty.conf

# ctags
ln -s -f ~/dotfiles/ctags ~/.ctags

# gitconfig
ln -s -f ~/dotfiles/git/gitconfig ~/.gitconfig

# git-pass-helper
mkdir -p ~/.config/pass-git-helper/
ln -s -f ~/dotfiles/git/git-pass-mapping.ini ~/.config/pass-git-helper/git-pass-mapping.ini

# tridactyl
ln -s -f ~/dotfiles/tridactylrc ~/.tridactylrc

# xbindkeys
ln -s -f ~/dotfiles/xbindkeysrc ~/.xbindkeysrc

# tig
ln -s -f ~/dotfiles/git/tigrc ~/.tigrc

# dunst
mkdir -p ~/.config/dunst
ln -s -f ~/dotfiles/dunst/dunstrc ~/.config/dunst/dunstrc

# khal
mkdir -p ~/.config/khal
ln -s -f ~/dotfiles/khal/config ~/.config/khal/config
