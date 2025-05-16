---
lab:
    title: 'Develop a content understanding client application'
    description: 'Use Azure AI Content Understanding REST API to develop a client app for an analyzer.'
---

# Develop a content understanding client application

In this exercise, you use Azure AI Content Understanding to create an analyzer that extracts information from business cards. You'll then develop a client application that uses the analyzer to extract contact details from scanned business cards.

This exercise takes approximately **30** minutes.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](./media/ai-foundry-portal.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a valid name for your project, and if an existing hub is suggested, choose the option to create a new one. Then review the Azure resources that will be automatically created to support your hub and project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A valid name for your hub*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: Choose one of the following regions\*
        - West US
        - Sweden Central
        - Australia East
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource*
    - **Connect Azure AI Search**: *Create a new Azure AI Search resource with a unique name*

    > \*At the time of writing, Azure AI Content understanding is only avilable in these regions.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](./media/ai-foundry-project.png)

## Create a Content Understanding analyzer

In your AI Foundry project, you're going to build an analyzer that can extract information from images of business cards. You'll start by defining a schema based on a sample image.

1. In a new browser tab, download the [biz-card-1.png](https://github.com/microsoftlearning/mslearn-ai-information-extraction/raw/main/Labfiles/content-app/biz-card-1.png) sample business card from `https://github.com/microsoftlearning/mslearn-ai-information-extraction/raw/main/Labfiles/content-app/biz-card-1.png` and save it in a local folder.

    The buisness card in the image looks like this:

    ![A business card for Roberto Tamburello, an Adventure Works Cycles employee.](./media/biz-card-1.png)

1. Return to the tab containing the home page for your Azure AI Foundry project; and in the navigation pane on the left, select **Content Understanding**.
1. On the **Content Understanding** page, select the **Custom analyzer** tab at the top.
1. On the Content Understanding custom analyzer page, select **+ Create**, and create a task with the following settings:
    - **Task name**: `Business card analysis`
    - **Description**: `Extract data from a business card`
    - **Azure AI services connection**: *the Azure AI Services resource in your Azure AI Foundry hub*
    - **Azure Blob Storage account**: *The default storage account in your Azure AI Foundry hub*
1. Wait for the task to be created.

    > **Tip**: If an error accessing storage occurs, wait a minute and try again.

1. On the **Define schema** page, upload **biz-card-1.png** and select the **Document analysis** template. Then select **Create**.

    The *Document analysis* template doesn't include any predefined fields. You must define fields to describe the information you want to extract.

1. Use **+ Add new field** button to add the following fields, selecting **Save changes** (**&#10003;**) for each new field:

    | Field name | Field description | Value type | Method |
    |--|--|--|--|
    | `Company` | `Company or organization` | String | Extract |
    | `Name` | `Contact's name` | String | Extract |
    | `Title` | `Contact's job title` | String | Extract |
    | `Email` | `Contact's email address` | String | Extract |
    | `Phone` | `Contact's phone number` | String | Extract |

1. Verify that your completed schema includes the fields above, and select **Save**.
1. On the **Test Analyzer** page, if analysis does not begin automatically, select **Run analysis**. Then wait for analysis to complete and review the values extracted from the business card based on the fields in the schema. The fields should have been correctly identified.

    > **Note**: For more complex document layouts, you can explicitly *label* the fields in an example document to improve the accuracy of the analyzer. For this simple senario, the fields should be detected automatically.

1. Select the **Build analyzer** page, and then select **+ Build analyzer** and build a new analyzer with the following properties (typed exactly as shown here):
    - **Name**: `business-card-analyzer`
    - **Description**: `Business card analyzer`
1. Wait for the new analyzer to be ready (use the **Refresh** button to check).

## Use the Content Understanding REST API

Now that you've created an analyzer, you can consume it from a client application through the Content Understanding REST API.

1. Return to the **Overview** page for your AI Foundry project, and in the **Project details** area, note the **Project connection string**. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.

    Close any welcome notifications to see the Azure portal home page.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.

    The cloud shell provides a command-line interface in a pane at the bottom of the Azure portal. You can resize or maximize this pane to make it easier to work in.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    **<font color="red">Ensure you've switched to the classic version of the cloud shell before continuing.</font>**

1. In the cloud shell pane, enter the following commands to clone the GitHub repo containing the code files for this exercise (type the command, or copy it to the clipboard and then right-click in the command line and paste as plain text):

    ```
   rm -r mslearn-ai-info -f
   git clone https://github.com/microsoftlearning/mslearn-ai-information-extraction mslearn-ai-info
    ```

    > **Tip**: As you enter commands into the cloudshell, the output may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, navigate to the folder containing the code files for your app:

    ```
   cd mslearn-ai-info/Labfiles/content-app
   ls -a -l
    ```

    The folder contains two scanned business card images as well as the Python code files you need to build your app.

1. In the cloud shell command-line pane, enter the following command to install the libraries you'll use:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt
    ```

1. Enter the following command to edit the configuration file that has been provided:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **YOUR_PROJECT_CONNECTION_STRING** placeholder with the connection string for your project (copied from the project **Overview** page in the Azure AI Foundry portal), and ensure that **ANALYZER** is set to the name you assigned to your analyzer (which should be *business-card-analyzer*)
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

1. In the cloud shell command line, enter the following command to edit the **card-app.py** Python code file that has been provided:

    ```
   code card-app.py
    ```

    The Python code file is opened in a code editor:

1. Review the code, which:
    - Identifies the image file to be analyzed, with a default of **biz-card-1.png**.
    - Retrieves the endpoint and key for your Azure AI Services resource from the project (using the Azure credentials from the current cloud shell session to authenticate).
    - Calls a function named **analyze_card**, which is currently not implemented

1. In the **analyze_card** function, find the comment **Use Content Understanding to analyze the image** and add the following code (being careful to maintain the correct indentation):

    ```python
   # Use Content Understanding to analyze the image
   print (f"Analyzing {image_file}")

   # Set the API version
   CU_VERSION = "2024-12-01-preview";

   # Read the image data
   with open(image_file, "rb") as file:
        image_data = file.read()
    
   ## Use a POST request to submit the image data to the analyzer
   print("Submitting request...")
   headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"}
   url = endpoint + f'/contentunderstanding/analyzers/{analyzer}:analyze?api-version={CU_VERSION}'
   response = requests.post(url, headers=headers, data=image_data)

   # Get the response and extract the ID assigned to the analysis operation
   print(response.status_code)
   response_json = response.json()
   id_value = response_json.get("id")

   # Use a GET request to check the status of the analysis operation
   print ('Getting results...')
   result_url = f'{endpoint}/contentunderstanding/analyzers/{analyzer}/results/{id_value}?api-version={CU_VERSION}'
   result_response = requests.get(result_url, headers=headers)
   print(result_response.status_code)

   # Keep polling until the analysis is complete
   status = result_response.json().get("status")
   while status == "Running":
        result_response = requests.get(result_url, headers=headers)
        status = result_response.json().get("status")

   # Process the analysis results
   if status == "Succeeded":
        print("Analysis succeeded:\n")
        result_json = result_response.json()
        output_file = "results.json"
        with open(output_file, "w") as json_file:
            json.dump(result_json, json_file, indent=4)
            print(f"Response saved in {output_file}")

        # Iterate through the fields and extract the names and type-specific values
        contents = result_json["result"]["contents"]
        for content in contents:
            if "fields" in content:
                fields = content["fields"]
                for field_name, field_data in fields.items():
                    if field_data['type'] == "string":
                        print(f"{field_name}: {field_data['valueString']}")
                    elif field_data['type'] == "number":
                        print(f"{field_name}: {field_data['valueNumber']}")
                    elif field_data['type'] == "integer":
                        print(f"{field_name}: {field_data['valueInteger']}")
                    elif field_data['type'] == "date":
                        print(f"{field_name}: {field_data['valueDate']}")
                    elif field_data['type'] == "time":
                        print(f"{field_name}: {field_data['valueTime']}")
                    elif field_data['type'] == "array":
                        print(f"{field_name}: {field_data['valueArray']}")
    ```

1. Review the code you added, which:
    - Reads the contents of the image file
    - Sets the version of the Content Understanding REST API to be used
    - Submits an HTTP POST request to your Content Understanding endpoint, instructing the to analyze the image.
    - Checks the response from the POST operation to retrieve an ID for the analysis operation.
    - Repeatedly submits an HTTP GET request to your Content Understanding endpoint to check the operation status until it is no longer running.
    - If the operation has succeeded, saves the JSON response, and then parses the JSON and displays the values retrieved for each type-specific field.

    > **Note**: In our simple business card schema, all of the fields are strings. The code here illustrates the need to check the type of each field so that you can extract values of different types from a more complex schema.

1. Use the **CTRL+S** command to save the code changes, but keep the code editor pane open in case you need to correct any errors in the code. Resize the panes s you can clearly see the command line pane.
1. In the cloud shell command line pane, enter the following command to run the Python code:

    ```
   python card-app.py biz-card-1.png
    ```

1. Review the output from the program, which should show the values for the fields in the business card with which you trained the analyzer
1. Use the following command to run the program with a different business card:

    ```
   python card-app.py biz-card-2.png
    ```

1. Review the results, which should reflect the values in this business card:

    ![A business card for Mary Duartes, an Contoso employee.](./media/biz-card-2.png)

1. In the cloud shell command line pane, use the **more** command to view the full JSON response that was returned:

    ```
   more results.json
    ```

    Use **Enter** or the down arrow to scroll through the JSON.

## Clean up

If you've finished working with the Content Understanding service, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. In the Azure AI Foundry portal, navigate to your project and delete it.
1. In the Azure portal, delete the resource group you created in this exercise.
