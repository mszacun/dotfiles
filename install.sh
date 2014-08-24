#!/usr/bin/sh

# dotfile instalation script

# copy vim configuartion
ln ~/dotfiles/vim/vimrc ~/.vimrc 
ln -s ~/dotfiles/vim/vim ~/.vim

# install vundle
git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
echo "Dont forget to install plugins in vim!"

# copy conky configuration file
ln ~/dotfiles/conkyrc ~/.conkyrc

# copy scripts used in conky
ln -s ~/dotfiles/scripts ~/.scripts
