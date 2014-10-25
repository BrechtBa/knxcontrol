# Raspbery Pi preparation for KNXControl

## Start fresh
Write a fresh raspbian image to a 8GB SD card using win32diskimager
A high end SD card is preferable as we will write to it a lot
Plug in the raspberry pi and connect to your network

### Configuration
Find the ip adress of the raspberry.pi using Advanced IP Scanner
Use PuTTy to connect to your raspberry over ssh with any computer in your network
Use the above found ip adress, port 22
login as: pi

password: raspberry
Run configuration
sudo raspi-config

Choose
Enlarge the root partition

Under the internationalisation options choose Change Timezone and set it to your time zone
I'm not changing the password yet to make a general image of this pi with the default password.

When asked choose Reboot now


## Networking

After the reboot find the ip adress again and connect using PuTTy

### Static ip
Setup a static ip adress open the network interfaces file
�sudo nano /etc/network/interfaces�

Change file contents to:
���
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.1.2
gateway 192.168.1.1
netmask 255.255.255.0
���
Save the file and Exit using �Ctrl+O� and �Ctrl+X�

restart networking
�sudo /etc/init.d/networking restart�
you can safely ignore error messages

Now close your current putty session and start a new one using the static ip adress 192.168.1.2 in this example.
A reboot might also be required for the static ip to come to effect:
�sudo reboot�

From now on you can allways acces your pi through that ip adress.
It must be noted that it is best to choose an ip adress outside of your routers DHCP range, so set the DHCP range accordingly.


## EIBD


#################################################################
# change eibd settings
#################################################################
sudo vim /etc/default/eibd
# uncomment lines and set the following values: 
EIB_ARGS="..."
EIB_ADDR="0.0.255"
EIB_IF="ipt:192.168.1.3"  # ip router adress

# restart eibd
/etc/init.d/eibd restart

# test eibd groupswrite

groupswrite ip:localhost 1/1/5 1
groupswrite ip:localhost 1/1/5 0

#################################################################
# change the network settings to a static ip adress 192.168.1.2
#################################################################

sudo nano /etc/network/interfaces

# overwrite with:
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.1.2
gateway 192.168.1.1
netmask 255.255.255.0

# restart networking
sudo /etc/init.d/networking restart

# ignore error messages

#################################################################
# add a user
#################################################################
sudo adduser admin
sudo passwd admin

sudo userdel pi
#################################################################
# install packages:
#################################################################
sudo apt-get update
sudo apt-get install vsftpd
#sudo apt-get install mc

#################################################################
# configure ftp server
#################################################################
sudo vim /etc/vsftpd.conf
# Edit or uncomment the following lines to secure VSFTPD
anonymous_enable=NO
local_enable=YES
write_enable=YES
ascii_upload_enable=YES
ascii_download_enable=YES

sudo /etc/init.d/vsftpd restart

# log on using an ftp client 
# user: admin
# pswd: admin
# upload items to /usr/smarthome/items/
# upload the page files to /var/www/homecontrol/
# restart smarthome.py
/etc/init.d/smarthome.py restart


#################################################################
# mysql
#################################################################
sudo apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql
# set password as admin

sudo mysql_install_db

sudo /usr/bin/mysql_secure_installation
#Answer Y to all questions


# there were some issues with apache and php, reinstalling apache with:
sudo apt-get install apache2
# and php with:
sudo apt-get install php5 libapache2-mod-php5 php5-mcrypt
# and setting the privileges of the folder knxcontrol and subfolders
chmod -R a+x knxcontrol 
chmod -G o+r knxcontrol
# solved every thing

#################################################################
# phpmyadmin
#################################################################
sudo apt-get install phpmyadmin

# select apache2 for server
# Choose YES when asked about whether to Configure the database for phpmyadmin with dbconfig-common
# enter mysql password
# set phpmyadmin password to admin

# add phpmyadmin to apache
sudo nano /etc/apache2/apache2.conf
# at the bottom add
Include /etc/phpmyadmin/apache.conf


# restart apache 
sudo /etc/init.d/apache2 restart

# login to phpmyadmin using roor - admin

# security
sudo nano /etc/phpmyadmin/apache.conf 

#make the directorry section look like this:
<Directory /usr/share/phpmyadmin>
        Options FollowSymLinks
        DirectoryIndex index.php
        AllowOverride All
        [...]
		
		
sudo nano /usr/share/phpmyadmin/.htaccess

# this is an empty file, add:
AuthType Basic
AuthName "Restricted Files"
AuthUserFile /usr/smarthome/.htpasswd
Require valid-user

# add user to password file
sudo htpasswd -c /usr/smarthome/.htpasswd root
# will ask for your password, enter
admin

# restart apache
sudo /etc/init.d/apache2 restart


#################################################################
# squeezelite
#################################################################
#sound card driver
sudo apt-get install alsa

# libraries
sudo apt-get install libfaad2 libmad0 libmpg123-0 libasound2

wget https://squeezelite.googlecode.com/files/squeezelite-armv6hf
chmod +x squeezelite-armv6hf
sudo mv squeezelite-armv6hf /usr/bin/
sudo adduser admin audio

# show audio devices
/usr/bin/squeezelite-armv6hf -l

# test squeezelite
/usr/bin/squeezelite-armv6hf -s 192.168.1.2 -n pi1 -z

# download autostart script
wget http://www.gerrelt.nl/RaspberryPi/squeezelitehf.sh
# edit script, only the squeezelite name needs to be changed to pi1 or something
nano squeezelitehf.sh
SL_NAME = "pi1" # needs to be uncommented

chmod u+x squeezelitehf.sh
sudo mv squeezelitehf.sh /etc/init.d/squeezelite
sudo update-rc.d squeezelite defaults

sudo /etc/init.d/squeezelite start

#################################################################
# python and mysql
#################################################################
sudo apt-get install python-mysqldb

# add
[Backup]
	comment = Backup Folder
	path = /media/hdd
	force user = admin
	force group = admin
	create mask = 0775
	directory mask = 0775
	read only = no
	
sudo /etc/init.d/samba restart

#################################################################
# network storage
#################################################################

sudo apt-get install samba samba-common-bin

sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.old
sudo nano /etc/samba/smb.conf



#################################################################
# ipopt and pyipopt
#################################################################
# http://www.coin-or.org/Ipopt/documentation/

sudo apt-get install gcc g++ gfortran subversion patch wget

cd /etc
sudo svn co https://projects.coin-or.org/svn/Ipopt/stable/3.11 CoinIpopt 
cd CoinIpopt

# getting 3rd party libraries
cd ThirdParty/Blas 
sudo ./get.Blas 
cd ../Lapack 
sudo ./get.Lapack 
cd ../ASL 
sudo ./get.ASL
cd ../Mumps
sudo ./get.Mumps
cd ../Metis
sudo ./get.Metis

cd ..
cd ..


# compiling IPOPT
sudo mkdir build
cd build

sudo /etc/CoinIpopt/configure -C ADD_CFLAGS="-DNO_fpu_control"
sudo make
sudo make test
sudo make install

#test the example
cd /etc/CoinIpopt/build/Ipopt/examples/hs071_cpp
sudo ./hs071_cpp



# getting python.h
sudo apt-get install python3.2-dev


# pyipopt
cd /etc
sudo git clone https://github.com/facat/py3ipopt.git
cd py3ipopt

# edit setup.py
sudo nano setup.py 
#change directory line to "/etc/CoinIpopt/build/"
#change "blas" to "coinblas" and "lapack" to "coinlapack" in libraries 

#sudo ldconfig
sudo python3 setup.py build
sudo python3 setup.py install

cd examples
# change print command in hs071.py, add ()
sudo nano hs071.py
python3 hs071.py