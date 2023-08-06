

all: classes.png packages.png

classes.png: classes_lbinstall.dot
	dot -Tpng -o classes.png ../classes_lbinstall.dot

packages.png: packages_lbinstall.dot
	dot -Tpng -o packages.png  ../packages_lbinstall.dot

packages_lbinstall.dot: classes_lbinstall.dot
	
classes_lbinstall.dot:  packages_lbinstall.dot
	cd .. && pyreverse -p lbinstall --ignore=test,rpmfile  lbinstall tools


