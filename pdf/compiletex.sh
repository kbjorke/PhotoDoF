#!/bin/bash

path="/home/kristian/Python/PhotoDoF/pdf/"
filename="dof"

pdflatex --output-directory=${path}/aux "${path}${filename}.tex"
pdflatex --output-directory=${path}/aux "${path}${filename}.tex"

mv "${path}/aux/${filename}.pdf" $path
cp ${path}${filename}.tex ${path}/bckp/
