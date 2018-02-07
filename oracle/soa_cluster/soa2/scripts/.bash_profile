# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

JAVA_HOME=/opt/jdk1.8.0_152
export JAVA_HOME

#ORACLE_HOME=/home/vagrant/Oracle/Middleware/Oracle_Home
#export ORACLE_HOME

PATH=$PATH:$HOME/.local/bin:$HOME/bin:$JAVA_HOME/bin
export PATH
