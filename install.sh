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

# install oh-my-zsh
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
ln -s ~/dotfiles/zsh/zshrc ~/.zshrc
mkdir ~/.oh-my-zsh/custom/themes
ln -s ~/dotfiles/zsh/mytheme.zsh-theme ~/.oh-my-zsh/custom/themes

ln -s ~/dotfiles/tmux.conf ~/.tmux.conf
