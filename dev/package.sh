#!/bin/bash
WORKSPACE_ROOT=$(pwd)

cd $WORKSPACE_ROOT/..

rm -rf md_exporter.difypk

dify plugin package md_exporter