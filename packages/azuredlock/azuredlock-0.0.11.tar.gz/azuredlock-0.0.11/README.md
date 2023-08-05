# azuredlock

azure + redlock onboarding script.

This is mainly just a wrapper around the az cli which is a dependency.

The quickest path is to do a `pip install azuredlock` and then
run `azuredlock onboard` from the Azure Cloud Shell which is in the 
Azure Portal since it already has the cli and uses a form of 
Managed Identities so you don't even have to login for it to work.
