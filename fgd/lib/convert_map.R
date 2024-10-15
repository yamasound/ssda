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

# 「基盤地図情報ダウンロードデータファイル仕様書4.1」参照
tags <- c(
    'GCP',      # 測量の基準点
    'ElevPt',   # 標高点
    'Cntr',     # 等高線
    'AdmBdry',  # 行政区画界線
    'CommBdry', # 町字界線
    'AdmPt',    # 行政区画代表点
    'CommPt',   # 町字の代表点
    'AdmArea',  # 行政区画
    'Cstline',  # 海岸線
    'WL',       # 水涯線
    'WA',       # 水域
    'WStrL',    # 水部構造物線
    'WStrA',    # 水部構造物面
    'BldL',     # 建築物の外周線
    'BldA',     # 建築物
    'RdEdg',    # 道路縁
    'RdCompt',  # 道路構成線
    'RailCL'    # 軌道の中心線
)

for ( tag in tags ){ 
    print(tag)
    conv(tag)
}
