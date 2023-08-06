# XRDownloader
XploitsR | XRDownloader is a module for faster downloading of files.

# Usage
    # import the xrdownloader module
      import xrdownloader
    
    # XRDownloader returns the response from ongoing downloads
      xr = xrdownloader.XRDownloader()
     
    # To download single file, just put in the url
      download_Files("your-file-url")

    # To download multiple files, add [] and seperate the links with ,
      download_Files(["link-1","link-2","link-3","and so on.."])

    # You can also specify a file that contains your links
      download_Files("your-file") # example: download_Files("myLinks.txt")

    Examples:

        #######################
        #  single file link   #
        #######################
        import xrdownloader
        xr = xrdownloader.XRDownloader()
        response = xr.download_Files("https://xploitsr.tk/assets/csxp_img/logo/icon.png")
        print(response)

        
        #######################
        #  multiple file link #
        #######################
        import xrdownloader
        xr = xrdownloader.XRDownloader()
        response = xr.download_Files(["https://www.somesite.co/file-1.pdf","https://www.somesite.co/file-2.pdf"])
        print(response)


        ##############################################
        #  file contains links of files to download  #
        ##############################################
        import xrdownloader
        xr = xrdownloader.XRDownloader()
        response = xr.download_Files("xploitsr-links.txt")
        print(response)
