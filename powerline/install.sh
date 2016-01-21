sudo cp segments/* /usr/lib/python2.7/site-packages/powerline/segments/common
sudo cp powerline.lua /usr/lib/python2.7/site-packages/powerline/bindings/awesome/powerline.lua

mkdir ~/.config/powerline
cp -r colors.json colorschemes config.json themes ~/.config/powerline
