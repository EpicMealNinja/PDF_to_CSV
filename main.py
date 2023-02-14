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
    path += "/csvs"
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
            file = file[0:-4]
            print(file)
            #Create a csv file with the same name as the pdf
            csvFile = open("csvs/" + file + ".csv", 'w', encoding='utf-8-sig')
            #Write header for csv file
            csvFile.write("Text,Null copula,Person/num. agreement,Multiple negators,Existential it/dey,Perfect done,Remote past BIN,Habitual be")
            #Loop through all the pages in the pdf
            for page in pdfReader.pages:
                #Clean the text for Rezonator
                #Skip the first page
                if page == pdfReader.pages[0]:
                    continue
                
                #Store the text in a variable
                pageText = page.extract_text()

                #Change the text so that it is usable in Rezonator
                #replace all commas with semicolons
                pageText = pageText.replace(",", ";")
                #Delete all new lines
                pageText = pageText.replace("\n", "")
                #Replace all double spaces with single spaces
                pageText = pageText.replace("  ", " ")
                #For every capitial letter followed by a colon add a new line
                count = 0
                for i in range(len(pageText)):
                    i += count
                    if pageText[i].isupper() and pageText[i + 1] == ":":
                        pageText = pageText[:i - 1] + "\n" + pageText[i - 1:]
                        count += 1
                #If it is the first page delete all text before the first new line
                if page == pdfReader.pages[1]:
                    pageText = pageText[pageText.find("\n"):]

                #Remove all text after and including "[End of interview]"
                pageText = pageText[:pageText.find("[End of interview]")]
                #Remove all text before and including "Page" + the page number
                if pdfReader.get_page_number(page) != 1:
                    headerSpot = "Page " + str(pdfReader.get_page_number(page))
                    pageText = pageText[pageText.find(headerSpot) + len(headerSpot):]
                #Extract the text from the page and write it to the csv file
                csvFile.write(pageText)
            #Close the csv file
            csvFile.close()
        #Close the pdf file
        pdfFileObj.close()


if __name__ == "__main__":
    main()