#!/bin/bash -ex

# usage
if [[ $# -lt 1 ]] ; then
    echo "Usage: $0 {version}"
    echo ""
    echo "Example: $0 2.4.0"
    exit 1
fi

zone_version=$1
base_url="https://solutions-reference.s3.amazonaws.com/aws-landing-zone/v${zone_version}"

# Cleanup
rm -fr ./tmp
mkdir ./tmp

# Fetch stuff
# Got this list from here: https://github.com/devk-insurance/landing-zone/blob/master/downloadLandingZones.sh
pushd ./tmp
curl --fail -LO "${base_url}/aws-landing-zone-initiation.template"
curl --fail -LO "${base_url}/aws-landing-zone-addon-publisher.zip"
curl --fail -LO "${base_url}/aws-landing-zone-add-on-config-deployer.zip"
curl --fail -LO "${base_url}/aws-landing-zone-avm-cr.zip"
curl --fail -LO "${base_url}/aws-landing-zone-config-deployer.zip"
curl --fail -LO "${base_url}/aws-landing-zone-handshake-state-machine.zip"
curl --fail -LO "${base_url}/aws-landing-zone-launch-avm.zip"
curl --fail -LO "${base_url}/aws-landing-zone-state-machine-trigger.zip"
curl --fail -LO "${base_url}/aws-landing-zone-state-machine.zip"
curl --fail -LO "${base_url}/aws-landing-zone-configuration.zip"
curl --fail -LO "${base_url}/aws-landing-zone-validation.zip"

# Unzip, cleanup
for zip_file in *.zip
do
    directory="${zip_file%.*}"
    mkdir "${directory}"
    unzip "${zip_file}" -d "${directory}"
done
rm *.zip

# Add-ons
mkdir ./add-on
pushd ./add-on
curl --fail -LO "${base_url}/add-on/aws-centralized-logging-solution.zip"
curl --fail -LO "${base_url}/add-on/aws-centralized-logging-solution.template"

# Unzip, cleanup
for zip_file in *.zip
do
    directory="${zip_file%.*}"
    mkdir "${directory}"
    unzip "${zip_file}" -d "${directory}"
done
rm *.zip

# root dir
popd
popd

# Swap LZ content with new version
rm -fr landing-zone
mv ./tmp ./landing-zone
