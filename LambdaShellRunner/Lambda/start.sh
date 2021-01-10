
set -e

function handler () {
    EVENT_DATA=$1
    echo "$EVENT_DATA" 1>&2;
    echo "Starting Up Runner......" 1>&2;

    aws ssm get-parameter --with-decryption --name /GitLabRunners/RegistrationToken > /tmp/ssm-registration-token.json
    registration_token=$(jq -r ".Parameter.Value" /tmp/ssm-registration-token.json)
    aws ssm get-parameter --with-decryption --name /GitLabRunners/Url > /tmp/ssm-url.json
    url=$(jq -r ".Parameter.Value" /tmp/ssm-url.json)

    curl --request POST "$url/api/v4/runners" --form "token=$registration_token" --form "description=my-lambda-test" --form "tag_list=aws,lambda,shell" > /tmp/registration.json
    id=$(jq -r ".id" /tmp/registration.json)
    runner_token=$(jq -r ".token" /tmp/registration.json)

    gitlab-runner run-single -u $url -t $runner_token --description "my-lambda-test" --executor shell --docker-image alpine:3.7 --builds-dir "/tmp/" --max-builds 1
    
    curl --request DELETE "$url/api/v4/runners" --form "token=$runner_token"

    echo "All done, removed runner" 1>&2;
}