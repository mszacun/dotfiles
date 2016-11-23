#!/usr/bin/sh

# dotfile instalation script

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

# awesome
ln -s ~/dotfiles/awesome ~/.config/awesome

# ctags
ln -s ~/dotfiles/ctags ~/.ctags

# gitconfig
ln -s ~/dotfiles/gitconfig ~/.gitconfig

# vimperator
ln -s ~/dotfiles/vimperatorrc ~/.vimperatorrc

# xbindkeys
ln -s ~/dotfiles/xbindkeysrc ~/.xbindkeysrc

yaourt -S fasd
