import PyPDF2
import os
import PySimpleGUI as sg

def main(): 
    #Create a window
    layout = [[sg.Text("Select folder of pdfs (Will work with all the pdfs in the folder)")],
                [sg.Input(), sg.FolderBrowse()],
                [sg.Button("Ok")]]
    window = sg.Window("Folder Browser", layout)
    event, values = window.read()
    window.close()
    #Get the path of the selected folder
    path = values[0]
    #Get a list of all the files in the directory
    list_of_files = os.listdir(path)

    #Create a folder to store the csv files
    path = os.getcwd()
    path += "\csvs"
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(path)
    
    #Loop through the list of files
    for file in list_of_files:
        #Check if the file is a pdf and starts with "AAHP"
        if file.endswith(".pdf") and file.startswith("AAHP"):
            #Open the pdf file
            pdfFileObj = open("pdfs/" + file, 'rb')
            #Create a pdf reader object
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            #Remove the .pdf from the file name
            file = file[1:-4]
            print(file)
            #Create a csv file with the same name as the pdf
            csvFile = open("csvs/" + file + ".csv", 'w')
            #Loop through all the pages in the pdf
            for page in pdfReader.pages:
                #Clean the text for Rezonator
                #Skip the first page
                if page == pdfReader.pages[0]:
                    continue

                #Change the text so that it is usable in Rezonator
                #Replave two new lines with one new line
                page.extract_text().replace("\n\n", "\n")

                #Extract the text from the page and write it to the csv file
                csvFile.write(page.extract_text())
            #Close the csv file
            csvFile.close()
        #Close the pdf file
        pdfFileObj.close()
        break


if __name__ == "__main__":
    main()