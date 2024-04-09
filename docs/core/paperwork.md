# Paperwork Automation
We will use PyMuPDF to work with pdfs in python. Every piece of paperwork has "forms" to be filled. Each of these forms are uniquely named. Forms that represent the same information should have the same name.

## Pipeline
### Preprocessing
The pipeline starts with a blank paperwork file.
1. Convert to pdf if it isn't
2. Add all fields using sedja
3. Rename and add new fields to the PFD (Paperwork Field Dictionary)
4. Provide default values for fields
5. Mark required fields as such
### Usage
1. Identify the paperwork template you want to fill out.
2. Fill out fields given context.

## Paperwork Pipeline Tools
Get the pdf, add all forms to it. Now the pdf might have already came with some forms. In this case we want to standardize it - match it with out Paperwork Field Dictionary.
Standardize Fields Bulk Manual Tool: CLI. Loop through each field. Show the existing field name, whether it exists in the PFD and definition if it does. User can manually decide to accept or create a new field name and definition, which automatically gets added to PFD and updates the paperwork template object. In addition at each step here we get to set default or required. Display PDF page with field name at the form of interest.
Edit individual field in paperwork: CLI. Provide paperwork id and field name and edit the 