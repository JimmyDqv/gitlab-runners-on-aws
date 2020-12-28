
set -e

function handler () {
    echo "Starting Up......"

    REGISTRATION_TOKEN=abcdefgh123456
    URL=https://gitlab.com/

    curl --request POST "https://gitlab.com/api/v4/runners" --form "token=$REGISTRATION_TOKEN" --form "description=aws-lambda-shell" --form "tag_list=aws,lamba,shell" > /tmp/registration.json

    id=$(jq -r ".id" /tmp/registration.json)
    runner_token=$(jq -r ".token" /tmp/registration.json)

    gitlab-runner run-single -u $URL -t $runner_token --description "aws-lambda-shell" --executor shell --docker-image alpine:3.7 --builds-dir "/tmp/" --max-builds 1
    
    curl --request DELETE "https://gitlab.com/api/v4/runners" --form "token=$token"

    echo "Lambda Runner Completed!"
}