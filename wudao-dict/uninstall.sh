#!/bin/bash

wd -k

sysOS=`uname -s`
if [ $sysOS == "Darwin" ];then
    # 删除系统命令wd
    sudo rm -f /usr/local/bin/wd
    sudo rm -f /usr/local/bin/voc
    # 删除自动补全
    sudo rm -f /usr/local/etc/bash_completion.d/wd
else
    # 删除系统命令wd
    sudo rm -f /usr/bin/wd
    sudo rm -f /usr/bin/voc
    # 删除自动补全
    sudo rm -f /etc/bash_completion.d/wd
fi

echo 'Uninstall Finished! '

