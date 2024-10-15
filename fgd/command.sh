#!/bin/bash

f_install_fgdr() {
    sudo Rscript lib/install_fgdr.R
}

f_set_data() {
    cd ~/Downloads
    rm -rf PackDLMap
    unar PackDLMap.zip
    cd PackDLMap
    unzip -o '*.zip'
}

f_convert_map() {
    Rscript lib/convert_map.R
}

#f_install_fgdr
#f_set_data
f_convert_map
