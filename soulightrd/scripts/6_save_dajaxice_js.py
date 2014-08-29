import urllib

DAJAXICE_LINK = "https://frittie.s3.amazonaws.com/dajaxice/dajaxice.core.js"
DAJAXICE_DOWNLOAD_PLACE = "frittie/assets/static/js/dajaxice.core.js"

def main():
	print "...DOWNLOADING DAJAIXCE SCRIPT..."
	try:
		urllib.urlretrieve (DAJAXICE_LINK, DAJAXICE_DOWNLOAD_PLACE)
	except:
		print "Download Dajaxice Script Failed"
		raise

if __name__ == "__main__":
    main() 