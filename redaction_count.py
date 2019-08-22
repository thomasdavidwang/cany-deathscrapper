def redaction_count(pic):
  blblock = 0
  blockWidth = 5 # the width of the the measuring square
  imageWidth = 1220 #in pixels
  imageHeight = 1560 #in pixels
  #below is the number of characters on page divided by the average number of characters per line
  textLines = 3346/float(90)
   
  for xpos in range(0,imageWidth,blockWidth):
    for ypos in range(0,imageHeight,blockWidth):
      bl = 0
      for j in range(blockWidth):
        for i in range(blockWidth):
          pix = getPixel(pic,xpos+i, ypos+j)
          if getRed(pix) == 34 and getBlue(pix) == 32 and getGreen(pix) == 31:
            bl += 1
      
      if bl >= 20: #the number of pixels in the square that you demand to be that shade of black
        blblock +=1
  #the area of a redacted line in pixels, very sensitive so be exact if anything underestimate
  lineArea = 912*26
  blockArea = blockWidth**2  
  blblockPerLine = lineArea/float(blockArea)
  redactedLines = blblock/float(blblockPerLine)
  print "number of redacted lines", redactedLines
  print "percentage redacted on page", redactedLines/float(textLines+redactedLines)
#prompts you to pick a file that will be the input image
pic = makePicture(pickAFile())
redaction_count(pic) 