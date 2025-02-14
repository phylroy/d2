from bs4 import BeautifulSoup
import requests
import pandas as pd
# Get list of all tiers for all weapons
urls = [
        # Primary
        "https://www.blueberries.gg/weapons/best-destiny-2-auto-rifles/",
        "https://www.blueberries.gg/weapons/destiny-2-best-bows/",
        "https://www.blueberries.gg/weapons/destiny-2-hand-cannons/",
        "https://www.blueberries.gg/weapons/destiny-best-2-pulse-rifles/",
        "https://www.blueberries.gg/weapons/destiny-2-scout-rifles/",
        "https://www.blueberries.gg/weapons/destiny-2-best-sidearms/",
        "https://www.blueberries.gg/weapons/destiny-2-smg/",
        # Special
        "https://www.blueberries.gg/weapons/breech-grenade-launchers/",
        "https://www.blueberries.gg/weapons/destiny-2-fusion-rifles/",
        "https://www.blueberries.gg/weapons/destiny-2-snipers/",
        "https://www.blueberries.gg/weapons/best-glaives-destiny-2/",
        "https://www.blueberries.gg/weapons/destiny-2-best-shotguns/",
        "https://www.blueberries.gg/weapons/best-trace-rifles/",
        # Heavy
        "https://www.blueberries.gg/weapons/destiny-2-grenade-launchers/",
        "https://www.blueberries.gg/weapons/destiny-2-machine-guns/",
        "https://www.blueberries.gg/weapons/best-destiny-2-swords/", 
        "https://www.blueberries.gg/weapons/linear-fusion-rifles/",   
        "https://www.blueberries.gg/weapons/destiny-2-rocket-launchers/"
        ]

# Create an empty DataFrame
complete_weapon_df = pd.DataFrame()

# Iterate over all URLs
for url in urls:
    print("Processing URL:", url)
    # Get the HTML content from the URL
    html = requests.get(url).text
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    # Find the table of data contained in id="tablepress-4" in the HTML
    weapon_table = soup.find(id="tablepress-4")
    # Get the number of rows in the table
    rows = weapon_table.find_all("tr")
    # Get the header row
    header_row = rows[0]
    # Get the header columns
    header_cols = header_row.find_all("th")
    # Get the header text
    header = [col.text for col in header_cols]
    # Get the data rows
    data_rows = rows[1:]
    # Get the data columns
    data = []
    for row in data_rows:
        cols = row.find_all("td")
        cols = [col.text for col in cols]
        data.append(cols)
    # Create a DataFrame from the header and data
    weapon_df = pd.DataFrame(data, columns=header)
    # Remove any \n characters from the DataFrame
    weapon_df = weapon_df.replace(r'\n', '', regex=True)
    
    # Add the DataFrame to the complete DataFrame
    complete_weapon_df = pd.concat([complete_weapon_df, weapon_df], ignore_index=True)
 
# Clean up special charecters in the DataFrame
# replace charecter '›' with '>' in the Tier column
complete_weapon_df['Tier'] = complete_weapon_df['Tier'].str.replace('›', '>', regex=True)
# Replace the "’" with "'" in the Name column
complete_weapon_df['Name'] = complete_weapon_df['Name'].str.replace('’', "'", regex=True)

# Save dataframes to csv
# Sort the weapons by name
csv_output = complete_weapon_df.sort_values(by='Name')
csv_output.to_csv('complete_weapon_df.csv', index=False)

# list all unique tier names
print(complete_weapon_df['Tier'].unique())  

# List all columns in the DataFrame
print(complete_weapon_df.columns)

# Remove Exotics from the DataFrame we don't want to consider these. 
no_exotics_df = complete_weapon_df[complete_weapon_df['Archetype'] != 'Exotic']



# Tier names we consider, note this is with > charecters cleaned up. 
tier_names = [
                  'S+ > Meta', 
                  'S > Best',
                  'A > Strong', 
                  'B > Average', 
                  'C > Weak', 
                  'D > Worst']
# Open file Readme.md in write mode ensure encoding is utf-8
with open("README.md", "w") as file:
    # Write the header
    file.write("# Legendary Destiny 2 Weapon Tier List\n\n")
    # Iterate over the tier names
    for tier in tier_names:
        # Write the tier header
        file.write(f"### Tier: {tier}\n")
        # Get the weapons for the current tier
        tier_weapons = no_exotics_df[no_exotics_df['Tier'] == tier]
        # Sort the weapons by name
        tier_weapons = tier_weapons.sort_values(by='Name')
        # remove duplicates
        tier_weapons = tier_weapons.drop_duplicates(subset=['Name'])
        # Get the weapon names as a string
        tier_weapons_str = " OR ".join(tier_weapons['Name'].tolist())
        # Write the weapon names to the file
        file.write("```\n")
        file.write(tier_weapons_str)
        # Write a new line
        file.write("\n")
        file.write("```\n")






