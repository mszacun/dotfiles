#!/usr/bin/sh

# dotfile instalation script

pacman-mirrors -G

yaourt -S zsh tmux tig spotify python2-pip python-pip the_silver_searcher meld xbindkeys fzf-git fasd dunst qtile ctags \
    geckodriver kitty

sudo pip install selenium webium

# copy vim configuartion
ln ~/dotfiles/vim/vimrc ~/.vimrc 
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
ln -s ~/dotfiles/gitconfig ~/.gitconfig

# vimperator
ln -s ~/dotfiles/vimperatorrc ~/.vimperatorrc

# xbindkeys
ln -s ~/dotfiles/xbindkeysrc ~/.xbindkeysrc

