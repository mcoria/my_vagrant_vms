# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions

export ASERVER=/u02/oracle/config/domains/edg_domain
export APPHOME=/u02/oracle/config/applications/edg_domain
export MSERVER=/u01/oracle/config/domains/edg_domain
export MW_HOME=/u01/oracle/product/fmw
alias wlst=$MW_HOME/oracle_common/common/bin/wlst.sh


