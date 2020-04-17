#!/bin/bash

usage()
{
	echo "Incorrect args - must specify build or release"
	exit 1
}

[[ $# -ne 2 ]] || usage

# args: 
	# image tag
	# dockerfile name
build()
{
	docker build -t "$1" -f "$2" .
}

# args: 
	# image tag
release()
{
	docker image push "$1"
	datestamp_tag="$1"-$(date +"%Y_%m_%d-%H_%M_%S")
	docker tag "$1" "$datestamp_tag"
	docker image push "$datestamp_tag"
}

action=$1

username=$(jq -r '.docker_hub_username' manifest.json)
image_name=$(jq -r '.image_name' manifest.json)

for ((a=0; a < $(jq -r ".images | length" manifest.json); a++))
do
	name=$(jq -r '.images['$a'].name' manifest.json)
	dockerfile=$(jq -r '.images['$a'].dockerfile' manifest.json)
	if [[ "$action" == "build" ]]
	then
		build "$username/$image_name:$name" "$dockerfile"
	elif [[ "$action" == "release" ]]
	then
		release "$username/$image_name:$name"
	else
		usage
	fi
done
