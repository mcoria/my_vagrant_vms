# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions

EXPORT ASERVER=/u02/oracle/config/domains/edg_domain
EXPORT APPHOME=/u02/oracle/config/applications/edg_domain
EXPORT MSERVER=/u01/oracle/config/domains/edg_domain
EXPORT MW_HOME=/u01/oracle/product/fmw
alias wlst=$MW_HOME/oracle_common/common/bin/wlst.sh


