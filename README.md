# Amazon Sponsored Products Campaign Builder

> **Just fill in the Excel file and run the script—no coding changes needed!**

This script reads your Excel (Input_Campaigns.xlsx) and generates a bulk upload file for Amazon. Follow the simple steps below.

---

## 1. How to Install (What You Need)

1. **Install Python**
   - Go to https://www.python.org/downloads/ and click **Download**.
   - Run the downloaded file. During setup, **check** the box that says **Add Python to PATH**. Then click **Install**.
2. **Install Visual Studio Code (VSCode)**
   - Go to https://code.visualstudio.com/ and download the installer.
   - Run it and click **Next** on all default prompts.
3. **Install Python Packages**
   - Open VSCode. In the top menu, click **View > Terminal**.
   - In the terminal window that appears, type these two lines and press Enter after each:
     ```bash
     pip install pandas
     pip install openpyxl
     ```
   - These add two helpers: **pandas** (for working with tables) and **openpyxl** (for reading/saving Excel files).

---

## 2. How to Set Up Your Project Folder

1. Create a **new folder** anywhere you like (Desktop or Documents) and name it `AmazonCampaignBuilder`.
2. Copy the Python script file (`amazon_campaign_builder.py`) into this folder.
3. Keep your input Excel file (next section) ready in this same folder.
4. In VSCode, click **File > Open Folder** and select your `AmazonCampaignBuilder` folder.

---

## 3. Fill in Your Provided Input Excel

Open the provided Excel template (Input_Campaigns.xlsx). You don’t need to add or remove columns—just enter your campaign details under each column heading.

| Column                   | Required? | Notes / Example                          |
|--------------------------|:---------:|------------------------------------------|
| **campaign_name**        | Yes       | Unique ID, e.g. `BrandX_Shoes_01`         |
| **portfolio_id**         | Optional        | (Optional) portfolio identifier           |
| **budget**               | Yes       | Daily budget, e.g. `25.00`               |
| **sku**                  | Yes       | Comma-separated SKUs, e.g. `SKU1,SKU2`   |
| **ad_group_default_bid** | Yes       | Default bid, e.g. `0.75`                 |
| **bid**                  | Yes       | Keyword bid, e.g. `0.50`                 |
| **keyword_text**         | Yes       | Comma-separated keywords, e.g. `red shoes,blue hat` |
| **keyword_match_type**   | Yes       | `exact`, `phrase`, or `broad`            |
| **bidding_strategy**     | Yes       | e.g. `fixed bids`                  |
| **placement**            | Optional        | Optional—e.g. `placement-top`            |
| **percentage**           | Optional        | Optional adjustment %, e.g. `15`         |
| **negative_keyword_text**| Optional        | Optional CSV of negatives, e.g. `cheap,used` |
| **negative_match_type**  | Optional        | Optional—`negativeExact` or `negativePhrase` |

After entering all your data (starting on row 2), save and close the file.

---

---

## 4. How to Run the Script

1. Make sure both your script `amazon_campaign_builder.py` and your Excel `Input_Campaigns.xlsx` are in the same folder.
2. In VSCode, open the file `amazon_campaign_builder.py`.
3. Near the bottom of the file, find the line that sets the input path, and change it to your file name:
   ```python
   input_file_path = r"./Input_Campaigns.xlsx"
   ```
4. Save the script (Ctrl+S).
5. In VSCode, click **View > Terminal** if it isn’t already open.
6. In the terminal, type:
   ```bash
   python amazon_campaign_builder.py
   ```
7. Press Enter. The script will read your Excel and create a new folder called `amazon_campaign_output_Manual` inside your project folder.
8. Inside that new folder, you’ll find your output Excel file (it will include a date/time in its name).

---

## 5. Troubleshooting (If Something Goes Wrong)

- **Python not found**: Did you check “Add Python to PATH” when installing? You may need to restart your computer.
- **ModuleNotFoundError**: In the terminal, run `pip install pandas` and `pip install openpyxl` again.
- **File not found**: Make sure your Excel file name exactly matches what you set in `input_file_path` and that it’s in the same folder.
- **PermissionError**: Close the Excel file in Excel before running the script; Excel locks the file when it’s open.
- **Wrong columns**: Double-check your Excel headers for typos and exact spelling.

---

## 6. Maintenance & Updates

- **Update software**: From time to time, run:
  ```bash
  pip install --upgrade pandas openpyxl
  ```
- **Update your Excel data** as your campaigns change; then run the script again.
- **Customize**: If you want to include more columns (like negative keywords), you can edit the Python script—just follow the same pattern used for the existing columns.


Congratulations! You’ve set up a basic, no-code workflow to build Amazon Sponsored Products bulk files from Excel. 🎉

