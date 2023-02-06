#/usr/bin/bash

##
# git clone https://github.com/clhore/SecureBrowser.git /opt/SecureBrowser/
# python3 -m venv /opt/SecureBrowser/venv
# /opt/SecureBrowser/venv/bin/python3 -m pip install -r /opt/SecureBrowser/requirements.txt
# cp /opt/SecureBrowser/SecureBrowser.desktop /usr/share/applications/
##

#!/usr/bin/bash

# Author: Adrian Lujan Munoz ( aka: clhore)

# Colours
readonly green="\e[0;32m\033[1m"
readonly end="\033[0m\e[0m"
readonly red="\e[0;31m\033[1m"
readonly blue="\e[0;34m\033[1m"
readonly yellow="\e[0;33m\033[1m"
readonly purple="\e[0;35m\033[1m"
readonly turquoise="\e[0;36m\033[1m"
readonly gray="\e[0;37m\033[1m"

# Commands path
export GIT="/usr/bin/git"
export PYTHON3="/usr/bin/python3"
export ECHO="/usr/bin/echo"
export TPUT="/usr/bin/tput"
export CP="/usr/bin/cp"
export RM="/usr/bin/rm"

trap ctrl_c INT

# Exit function
function ctrl_c(){
  $ECHO -e "\n${yellow}[*]${end}${gray}Saliendo${end}"
  $TPUT cnorm; $RM crmk.log 2>/dev/null; exit 0
}

function error_log(){
  case $1 in
     22)
       $ECHO -e "${red}:: Error clonando el repositorio${end}"
     ;;

     44)
       $ECHO -e "${red}:: Error instalando las dependencias necesarias${end}"
     ;;
  esac
}

function read_msg(){
  local OPT=""; case $1 in
     00)
       until [[ $OPT =~ (y|Y) ]]; do
            $ECHO -ne "${yellow}[*]${end}${gray} Indica tu usuario personal: "; read PERSONAL_USERNAME
            $ECHO -ne "${yellow}[*]${end}${gray} Has indicado bien el usuario${end} ${purple}(y/n)${end}: "; read OPT
       done
     ;;  

     22)
       until [[ $OPT =~ (y|n|Y|N) ]]; do
            $ECHO -ne "${yellow}[*]${end}${gray} Desea crear un entorno virtual${end} ${purple}python${end} (y/n): "; read OPT
       done; if [[ $OPT =~ (n|N) ]]; then return 0; fi; return 1
     ;;
  esac
}

function clone_repository(){
    $ECHO -e "${gray}:: Clonando repositorio del proyecto${end} ${purple}[github.com/clhore/SecureBrowser]${end}"
    $GIT clone https://github.com/clhore/SecureBrowser.git /opt/SecureBrowser/ || {
        error_log 22; $ECHO -e "${green}:: Eliminando ficheros en conflicto${end}"
        $RM -rf /opt/SecureBrowser &>/dev/null
        $GIT clone https://github.com/clhore/SecureBrowser.git /opt/SecureBrowser/ || { error_msg 22; exit 1; } 
    }
}    
#
function install_python_dependencies(){ # path
    $1 -m pip install -r /opt/SecureBrowser/requirements.txt || {
        error_log 44; $1 -m pip install -r /opt/SecureBrowser/requirements.txt || { error_log 44; exit 1; }
    }
}

function create_desktop_aplication(){ # path
    {
        $ECHO -e "[Desktop Entry]"
        $ECHO -e "Name=SecureBrowser"
        $ECHO -e "Version=1.0"
        $ECHO -e "Terminal=false"
        $ECHO -e "Icon=/opt/SecureBrowser/data/img/icon.png"
        $ECHO -e "Exec=$1 /opt/SecureBrowser/SecureBrowser.py"
        $ECHO -e "Path=/opt/SecureBrowser/"
        $ECHO -e "Type=Application"
    } | tee /opt/SecureBrowser/SecureBrowser.desktop &>/dev/null
    $CP /opt/SecureBrowser/SecureBrowser.desktop /usr/share/applications/
}

function create_venv(){
    $ECHO -e "${gray}:: Creando entrono virtual${end} ${purple}python${end}"
    $PYTHON3 -m venv /opt/SecureBrowser/venv
    $ECHO -e "${gray}:: Intalando dependencias requirements.txt${end}"
    install_python_dependencies '/opt/SecureBrowser/venv/bin/python3'; create_desktop_aplication '/opt/SecureBrowser/venv/bin/python3'
}

if [ $UID -eq 0 ]; then
    read_msg 00; clone_repository; chown ${PERSONAL_USERNAME}:${PERSONAL_USERNAME} /opt/SecureBrowser/ -R
    read_msg 22; if [ "$(echo $?)" == "1" ]; then create_venv; exit 0; fi
    install_python_dependencies $PYTHON3; create_desktop_aplication $PYTHON3
else
    $ECHO -e "${red}Ejecute el script como root${end}"
fi
