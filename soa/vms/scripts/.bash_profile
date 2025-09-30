# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

JAVA_HOME=/opt/jdk_latest
export JAVA_HOME


PATH=$PATH:$HOME/.local/bin:$HOME/bin:$JAVA_HOME/bin
export PATH
