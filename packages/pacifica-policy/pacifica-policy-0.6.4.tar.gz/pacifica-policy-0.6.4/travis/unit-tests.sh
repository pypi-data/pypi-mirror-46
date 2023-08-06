#!/bin/bash -xe
export POSTGRES_ENV_POSTGRES_USER=postgres
export POSTGRES_ENV_POSTGRES_PASSWORD=
export ADMIN_USER_ID=10
pushd travis
MetadataServer.py &
popd
MAX_TRIES=60
HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
while [[ $HTTP_CODE != 200 && $MAX_TRIES > 0 ]] ; do
  sleep 1
  HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
  MAX_TRIES=$(( MAX_TRIES - 1 ))
done
TOP_DIR=$PWD
MD_TEMP=$(mktemp -d)
git clone https://github.com/pacifica/pacifica-metadata.git ${MD_TEMP}
pushd ${MD_TEMP}
python test_files/loadit.py
popd
PYTHONPATH=${MD_TEMP} python test_files/loadit.py

export PYTHONPATH=$PWD
coverage run --include='pacifica/*' -m pytest -v
coverage run --include='pacifica/*' -a -m pacifica.policy --stop-after-a-moment
coverage report -m --fail-under=100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
