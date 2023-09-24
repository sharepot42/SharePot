#!/bin/sh

project_files=$(ls SharePot)

if [ $project_files -eq 0 ]; then
	expo start --template blank SharePot
fi
