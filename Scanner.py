#for read text from pdfs (ie SCOC)
def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    from google.cloud import vision
    from google.cloud import storage
    from google.protobuf import json_format
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.

    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=280)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()
    import re
    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.


    output = blob_list[2]

    json_string = output.download_as_string()
    response = json_format.Parse(json_string, vision.types.AnnotateFileResponse())


    #CHANGE EACH TIME

    page_response = response.responses[0]
    annotation = page_response.full_text_annotation


    # Here we print the full text from from each page to the text document.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    file_output = open("FOIL2_2text.txt", "a")
    file_output.write(annotation.text)
    file_output.close()

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
#simple chracter Counting function
def characterCounter(file_name):
    infile = open(file_name, 'r')
    lines = 0
    words = 0
    characters = 0
    for line in infile:
        wordslist = line.split()
        lines = lines + 1
        words = words + len(wordslist)
        characters = characters + len(line)
    print("Number of lines:", lines)
    print("Number of words:", words)
    print("Number of characters:", characters)

#this is the handwriting documentation program
def detect_document(path):
    from google.protobuf import json_format
    from google.cloud import storage
    """Detects document features in an image."""
    from google.cloud import vision
    #from json import load
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    #print(response)
    #son_string = response
    #print(json_format.Parse(json_string,vision.types.AnnotateFileResponse())) #vision.types.AnnotateFileResponse())
    file_output = open("2letter.txt", "a+")

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
    #            print('Paragraph confidence: {}'.format(
    #                paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print(format(word_text))
                    file_output.write(format(word_text+' '))
                    #for symbol in word.symbols:
                    #    print('\tSymbol: {} (confidence: {})'.format(
                    #    symbol.text, symbol.confidence))
    file_output.close()
    #this is for recognization text in images, I dont know how useful
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    file_output = open("FOIL2_2text.txt", "a")
    file_output.write(annotation.text)
    file_output.close()
    for text in texts:
        print('\n"{}"'.format(text.description))
        #specify the txt file you want it to write
        file_output = open("FOIL2_2text.txt", "a")
        file_output.write('\n"{}"'.format(text.description))
        #vertices = (['({},{})'.format(vertex.x, vertex.y)
        #            for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))
#obviously modify the below to the desired input and output URI
#CHANGE EACH TIME
detect_document("2letter_Page_1.jpg")
detect_document("2letter_Page_2.jpg")
#async_detect_document("gs://cany_project/FOIL2_2.pdf", "gs://cany_project/outputs/FOIL2_2scanned.pdf")
