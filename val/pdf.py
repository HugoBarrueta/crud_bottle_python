from xhtml2pdf import pisa             # import python module

# Define your data
#sourceHtml = "<html><body><p>To PDF or not to PDF</p></body></html>"
#outputFilename = "test.pdf"
"""
# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file
    
    print("pdf Generado")
    # return True on success and False on errors
    return pisaStatus.err

# Main program
#if __name__ == "__main__":
 #   pisa.showLogging()
    #convertHtmlToPdf(sourceHtml, outputFilename)"""
from io import BytesIO
from reportlab.pdfgen import canvas
from bottle import response
def convertHtmlToPdf(pdf):
    response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'
    response.headers['Content-Disposition'] = 'attachment; filename="test.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100,100, pdf)
    p.showPage()
    p.save()

    return buffer.getvalue()