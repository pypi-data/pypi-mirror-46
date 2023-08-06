#!/usr/bin/env bash


package_file_name="<package_file_name>"
repo_owner="<repo_owner>"
repo_name="<repo_name>"
tag_name="<tag_name>"
access_token="<access_token>"
unique_str="<unique_str>"
package_folder="/tmp/$unique_str-package"
built_package_folder="/tmp/$unique_str"

#************************ Downloading package ************************

mkdir -p ${package_folder}
curl -s -H 'Authorization: token '"$access_token"'' -H 'Accept: application/vnd.github.v3.raw' -Lo  ${package_folder}/${package_file_name} https://github.com/$repo_owner/$repo_name/archive/${package_file_name}
cd ${package_folder} && tar -xf ${package_file_name}

#************************* Building package **************************

cd ${package_folder}/pos*/client/pos/
npm install > /dev/null 2>&1
npm run-script build > /dev/null 2>&1

#************************* Packing package **************************

cd ${package_folder} && rm -rf *.tar.gz
cd ${package_folder}/pos*
mkdir -p server/app/code/Magestore/Webpos/build/apps/pos
cp -r client/pos/build/* server/app/code/Magestore/Webpos/build/apps/pos/
built_file_name="${repo_name}-${tag_name}.tar.gz"
tar -cf ${built_file_name} server
mkdir -p ${built_package_folder}
mv ${built_file_name} ${built_package_folder}/${built_file_name}