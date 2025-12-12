#!/bin/bash

# Load .env variables
set -a
source .env
set +a

# Backup the original pytest.ini
cp pytest.ini pytest.ini.bak

# Append credentials to pytest.ini
echo "rp_api_key = $RP_API_KEY" >> pytest.ini
echo "rp_endpoint = $RP_ENDPOINT" >> pytest.ini
echo "rp_project = $RP_PROJECT" >> pytest.ini
echo "rp_launch = $RP_LAUNCH" >> pytest.ini

# Run tests
pytest --reportportal -v

# Restore the original pytest.ini
mv pytest.ini.bak pytest.ini