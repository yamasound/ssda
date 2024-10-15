#!/usr/bin/env Rscript

# パッケージ読み込み
library(tidyverse) # r-cran-tidyverse
library(sf) # r-cran-sf
library(raster) # r-cran-raster
library(fgdr) # install_fgdr.R

conv <- function(tag){
     map_dir <- paste(work_dir, '/', 'PackDLMap/', sep='')
     gpkg_file <- paste(work_dir, '/', tag, '_WGS84.gpkg', sep='')
     list.files(path=map_dir, pattern=tag, full.names=T) %>%
         map(read_fgd) %>%  # xmlファイルにread_fgdを適用
         bind_rows() %>%  # xmlファイルを結合
         st_transform(4326) %>%  # WGS84に変換
         st_write(driver='GPKG', append=FALSE, gpkg_file)
}

work_dir = '~/Downloads'

tags <- c(
     'WA',      # 水域
     'WL',      # 河川
     'BldA',    # 建物 
     'RailCL',  # 鉄道
     'AdmArea', # 市区町村のポリゴン
     'AdmBdry'  # 市区町村のライン
)

for ( tag in tags ){ 
    print(tag)
    conv(tag)
}
