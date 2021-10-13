# Azure-Purview-API-via-PowerShell

************
**Execute Azure Purview RESTful APIs via PowerShell**
*****************************************************
- Azure Purview REST APIs via Powershell. Based on Microsoft Official [Azure Purview REST API Documentation](https://docs.microsoft.com/en-us/rest/api/purview/)

## Download & Installation
- Download & Install The Script : https://aka.ms/Purview-API-PS
- Note: You need Powershell v7.x.x. Please [Download and upgrade your Powershell to v7](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-windows?view=powershell-7.1). 

## Usage Steps
- Open PowerShell on your Windows machine. Press "Windows" Key, type powershell, click "Run as administrator".
- On powershell prompt, enter "cd ~/Documents" to change to your User Home/Documents Folder. You may move to any other folder of your choice but make sure you have write permissions on whichever directory you choose.
- Then run the following command(s) to execute the Purview API Utility Script.
- There are two modes of operation: 
1. *Interactive Mode*
2. *Batch Mode*


## Interactive & UI Mode: Usage
- In the Interactive & UI Mode, lot of interactive inline help and prompts will be given to make your usage experience friendly and easy. In this mode, any of the APIs listed here : [Purview_API_Reference.csv](https://github.com/Azure/Azure-Purview-API-PowerShell/blob/main/Purview_API_Reference.csv) can be executed. However, when you need to write batch scripts or automation for Purview, or even scheduled cron jobs at regular intervals, you must use the Batch Mode (next section detailed below).
- Note: Interactive Mode restricts you to the APIs listed in the CSV only since it builds the menu items from the CSV. However, in the Batch Mode, any other APIs not listed in the CSV, or any other variations of the APIs or even extra additional parameters can be supplied. 
- For anyone who is running first time or getting familiarized with this tool may choose to use Interactive Mode
- For those who are using this utility tool regularly, Batch Mode described below is recommended.
```PowerShell
PS >>   Purview-API-PowerShell     -PurviewAccountName   {your_purview_account_name}
```

## Batch, Scripting & Automation Mode: Usage Examples 
- Run Azure Purview APIs directly without any interactivity help or prompts.
- Useful when building scripts or automation or scheduled cron jobs.
- There are a few sample APIs shown via the commands below but you may execute any other Purview API from the Microsoft Official [Azure Purview REST API Documentation](https://docs.microsoft.com/en-us/rest/api/purview/). All APIs given in Official Purview API Docs are supported by this script in Batch Mode.
```PowerShell
# Get All TypeDefs - Entity Relationships All Objects In Purview
PS >>   Purview-API-PowerShell     -APIDirect    -HTTPMethod GET    -PurviewAPIDirectURL "https://{your-purview-account-name}.purview.azure.com/catalog/api/atlas/v2/types/typedefs?api-version=2021-07-01"     -InputFile inputfile.json     -OutputFile outputfile.json
# Get AzureKeyVaults For Registering Scans
PS >>   Purview-API-PowerShell     -APIDirect    -HTTPMethod GET    -PurviewAPIDirectURL "https://{your-purview-account-name}.purview.azure.com/scan/azurekeyvaults?api-version=2021-07-01"
# Get All DataSources Known To Purview
PS >>   Purview-API-PowerShell     -APIDirect    -HTTPMethod GET    -PurviewAPIDirectURL "https://{your-purview-account-name}.purview.azure.com/scan/datasources?api-version=2021-07-01" 
# Get All Scan Rule Sets - User Defined Only
PS >>   Purview-API-PowerShell     -APIDirect    -HTTPMethod GET    -PurviewAPIDirectURL "https://{your-purview-account-name}.purview.azure.com/scan/scanrulesets?api-version=2021-07-01" 
```
- Note: InputFile and OutputFile Parameters: are not mandatory but recommended. 
- InputFile: For most PUT and POST APIs (-HTTPMethod PUT or -HTTPMethod POST) you will notice from the Purview API Documentation that JSON Body needs to be sent with the API Request. In these POST and PUT scenarios it is recommended you make one JSON file and supply the name of this file in InputFile parameter. It is the file name on your local drive that contains the JSON to be sent as request body with the API invokation. 
- OutputFile: Name of the file that contains the output of the API in JSON format. OutputFile parameter is not mandatory. If you do not supply OutputFile, do not worry, the script will automatically generate one file named "purview-api-output-{todays-date-and-time}.json" in your current directory.

## Samples & Usage Presentation 
[Purview-API-Powershell.pdf](https://github.com/Azure/Azure-Purview-API-PowerShell/blob/main/Purview-API-Powershell.pdf)

## Videos
### Installation Video [![Installation](https://www.powershellgallery.com/Content/Images/Branding/packageDefaultIcon.svg)](https://youtu.be/rrTYnEqPHgM)

### Interactive Mode: Video [![Interactive Mode](https://www.powershellgallery.com/Content/Images/Branding/packageDefaultIcon.svg)](https://youtu.be/0M6jRG77Wt8)

### Batch Script Automation Mode: Video [![Batch Mode](https://www.powershellgallery.com/Content/Images/Branding/packageDefaultIcon.svg)](https://youtu.be/VDkAFIG7Ii0)

************
**Benefits**
************
- While you can very well use cURL or Postman to Invoke Azure Purview APIs as well, it is generally cumbersome to extract the Azure OAuth2 *access_token* and use it appropriately in scripts or even during one-time API execution.
- Powershell has very strong and user friendly integration interfaces with Azure Cloud and hence it makes it really useful to have a way to execute Azure Purview service via its APIs on Windows PowerShell.


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
