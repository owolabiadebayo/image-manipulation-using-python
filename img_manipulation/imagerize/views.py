from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from .cartoonizer import cartoonize
import cv2
import os
import time
import numpy as np
from .image_to_sketch import *
from PIL import Image, ImageFilter, ImageEnhance




# Create your views here.

def index(request):
	if request.method == "POST":
		option = request.POST.get("choose_option")
		file_selected = request.FILES.get("choose_file")
        
		if file_selected == None:
			return redirect("index")
		
		elif option == "Image To Cartoon":
			nparr = np.fromstring(file_selected.read(), np.uint8)
			img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			output = cartoonize(img)
			cv2.imwrite("sample.jpg", output)
			
			return redirect("send_img")
			
		elif option == "Image To Sketch":
			s=imageio.imread(file_selected)
			g=grayscale(s)
			i=255-g
			b=scipy.ndimage.filters.gaussian_filter(i,sigma=10)
			r=dodge(b,g)
			cv2.imwrite('sample.jpg', r)
			
			return redirect("send_img")
			
		elif option == "Image To GrayScale":
			nparr = np.fromstring(file_selected.read(), np.uint8)
			img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cv2.imwrite("sample.jpg", gray)
			
			return redirect("send_img")
			
		elif option == "Image To Contour":
			nparr = np.fromstring(file_selected.read(), np.uint8)
			img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			edged = cv2.Canny(gray, 30, 200)
			
			contours, hierarchy = cv2.findContours(edged,  
				cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
				
			contour = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
			#gray = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)
			gray = cv2.bitwise_not(contour)
			cv2.imwrite("sample.jpg", gray)
			
			return redirect("send_img")
			
			
		elif option == "Image To Enhanced Image":
			im = Image.open( file_selected)
			enh = ImageEnhance.Contrast(im)
			enh.enhance(1.8).save("sample.jpg")
			
			return redirect("send_img")
			
		elif option == "Image To Edges":
			nparr = np.fromstring(file_selected.read(), np.uint8)
			img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			edges = cv2.Canny(img,100,200) 
			cv2.imwrite("sample.jpg", edges)
			
			return redirect("send_img")
			
			
		else:
			return redirect("index")
			
			
		
	return render(request, "imagerize/index.html")
	
	
	
def send_image(request):
	f = open("sample.jpg", "rb")
	#response = FileResponse(f)
	response = HttpResponse(f.read(), content_type="image/jpeg")
	response['Content-Disposition'] = 'inline; filename=sample.jpg'
	
		
	return response
	
	
	
	

