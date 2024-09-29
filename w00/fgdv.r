#!/usr/bin/Rscript

install.packages('fgdr')

library(tidyverse)
library(sf)
library(raster)
library(fgdr)

# 水域
list.files(path = "map/PackDLMap/",  
           pattern = "WA",
           full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  st_write(driver = "GPKG" ,
           append = FALSE , "map/WA_JGD2000_12k.gpkg")  # ファイルを書き出し

# 河川
list.files(path = "map/PackDLMap/",  
           pattern = "WL",
           full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  st_write(driver = "GPKG" ,
           append = FALSE , "map/WL_JGD2000_12k.gpkg")  # ファイルを書き出し


# 等高線
list.files(path = "map/PackDLMap/",  
           pattern = "Contr",
           full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  st_write(driver = "GPKG" ,
           append = FALSE , "map/Contr_JGD2000_12k.gpkg") 

#建物
list.files(path = "map/PackDLMap/",  
                  pattern = "BldA",
                  full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  st_write(driver = "GPKG" ,
           append = FALSE , "map/BldA_JGD2000_12k.gpkg") 

# 鉄道
list.files(path = "map/PackDLMap/",  
           pattern = "RailCL",
           full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  st_write(driver = "GPKG" ,
           append = FALSE , "map/RailCL_JGD2000_12k.gpkg") 

# 市町村域_polygon
list.files(path = "map/PackDLMap/",  
                  pattern = "AdmArea",
                  full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  group_by(name) %>%  # 市町村名でグループ化
  summarize() %>%  # 市町村名で結合
  st_write(driver = "GPKG" ,
           append = FALSE , "map/AdmArea_JGD2000_12k.gpkg") 

# 市町村域_Line
list.files(path = "map/PackDLMap/",  
           pattern = "AdmBdry",
           full.names = T) %>%  # 基盤地図情報のxmlファイルをリスト化
  map(read_fgd) %>%  # xmlファイルにread_fgdを適用
  bind_rows() %>%  # xmlファイルを結合
  st_transform(2454) %>%  # JGD2000平面直角座標系12系に変換
  st_write(driver = "GPKG" ,
           append = FALSE , "map/AdmBdry_JGD2000_12k.gpkg") 
