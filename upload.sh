#!/bin/bash

PROFILE="skyline"
NAME="chestday-lambda"

aws --profile $PROFILE lambda update-function-code --function-name $NAME --zip-file fileb://output/lambda_code.zip