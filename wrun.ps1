###########################################################################################################
# Prepares environment, builds docker image to run a Python project and executes it.
#
# Written by Rian Koja to publish in a GitHub repository with specified licence.
###########################################################################################################

# Prepare environment:
$ScriptName = $MyInvocation.MyCommand.Name
Write-Output "Running $ScriptName script..."

$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
cd $ScriptDir

# Set up monitor, XLaunch is required. See https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde
# If not working, try restarting XLaunch.
$my_ip = Test-Connection -ComputerName (hostname) -Count 1  | Select-Object IPV4Address

# Check if target project is specified at the input:
if ($args[0] -eq $null) {
  Write-Output "Call this script with the folder name of the required project."
  exit 1
}
$ProjectName = $args[0]

# Build docker image:
try {
    docker build --build-arg target_dir="./$ProjectName" -t "runner_$ProjectName" -f ./DockerFiles/Dockerfile .
}
catch {
    Write-Output "Building image with $ProjectName failed, exiting $ScriptName"
    exit 2
 }

# Run docker image:
try {
    docker run -it --rm -e DISPLAY="$($my_ip.IPV4Address)":0.0 "runner_$ProjectName" 
}
catch {
    Write-Output "Running container for $ProjectName failed, exiting $ScriptName" 
    exit 3
}

echo "Finished $ScriptName script."