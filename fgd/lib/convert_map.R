#!/usr/bin/env Rscript

read_packages <- function(){
    library(tidyverse) # r-cran-tidyverse
    library(sf) # r-cran-sf
    library(raster) # r-cran-raster
    library(fgdr) # install_fgdr.R
}

convert_map <- function(work_dir, input_dir, output_dir, name, symbol){
     map_dir <- paste(work_dir, '/', input_dir, '/', sep='');
     output_file <- paste(work_dir, '/', output_dir, '/', name, '_WGS84.gpkg', sep='');
     list.files(path=map_dir, pattern=symbol, full.names=T) %>%
         map(read_fgd) %>%  # xmlファイルにread_fgdを適用
         bind_rows() %>%  # xmlファイルを結合
         st_transform(4326) %>%  # WGS84に変換
         st_write(driver='GPKG', append=FALSE, output_file)
}

clear_output_dir <- function(work_dir, output_dir){
    path <- paste(work_dir, '/', output_dir, sep='')
    if ( dir.exists(path) ){
       unlink(path, recursive=TRUE)
    }
    dir.create(path)
}

main <- function(work_dir, input_dir, output_dir, l_name_symbol){
    clear_output_dir(work_dir, output_dir)
    for ( i in seq(1, length(l_name_symbol)) ){
        name = l_name_symbol[[i]][1]
        symbol = l_name_symbol[[i]][2]
        cat(i, ': ', name, ', ', symbol, '\n', sep='')
        convert_map(work_dir, input_dir, output_dir, name, symbol)
   }
}

work_dir='~/Downloads'
input_dir='PackDLMap'
output_dir='kiban_toyohashi_20190701'
l_name_symbol <- list(
  #「基盤地図情報ダウンロードデータファイル仕様書4.1」参照
  c('測量の基準点', 'GCP'),
  c('標高点', 'ElevPt'),
  c('等高線', 'Cntr'),
  c('行政区画界線', 'AdmBdry'),
  c('町字界線', 'CommBdry'),
  c('行政区画代表点', 'AdmPt'),
  c('町字の代表点', 'CommPt'),
  c('行政区画', 'AdmArea'),
  c('海岸線', 'Cstline'),
  c('水涯線', 'WL'),
  c('水域', 'WA'),
  c('水部構造物線', 'WStrL'),
  c('水部構造物面', 'WStrA'),
  c('建築物の外周線', 'BldL'),
  c('建築物', 'BldA'),
  c('道路縁', 'RdEdg'),
  c('道路構成線', 'RdCompt'),
  c('軌道の中心線', 'RailCL')
)
read_packages()
main(work_dir, input_dir, output_dir, l_name_symbol)
