# Azure-Purview-API-via-PowerShell

************
**Execute Azure Purview RESTful APIs via PowerShell**
*****************************************************
- Azure Purview REST APIs via Powershell. Based on [Purview API Reference](https://docs.microsoft.com/en-us/rest/api/purview/)
- Note: You need Powershell v7.x.x to use this tool. Please [Download and upgrade your Powershell to v7](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-windows?view=powershell-7.1). 
- Extract [Purview-API-Powershell.zip](https://github.com/Azure/Azure-Purview-API-PowerShell/blob/main/Purview-API-Powershell.zip) to a folder of your choice.
- Right-Click on the folder and select "PowerShell > Open Here As Administrator" ![image](https://user-images.githubusercontent.com/13808986/131237833-6e9837c3-9e7f-4297-a800-2edf690fa9df.png)
- Run "Purview-API-PowerShell.exe"

*Note: The file "purview-api-body-payload.json" extracted in the same directory contains the API Body to be sent in case of PUT or POST APIs. Make sure to blank the file first, update your JSON into it and save the file before executing any "PUT" or "POST" APIs. If you need to back up your JSONs other than the one to be sent with the next request, you may do so in a different file name.

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
