#!/usr/bin/python

#print "hello"
import cv2
import numpy as np



class hog:
	def __init__(self,cellsize=3,blockheight=3,blockwidth=3):
		self.cellsize=cellsize
		self.blockheight=blockheight
		self.blockwidth=blockwidth
		self.derivate=np.array([-1,0,1])
		self.gammar_en=False
		self.gammar=0.5
		self.nbins=9
		self.min_ang=np.pi/self.nbins
		self.eps=1e-10
		self.border_width=1

	def calc_hog(self,img):
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		#if self.gammar_en:
			#do nothing

		#height_ratio=self.cellsize*self.blockheight
		#width_ratio=self.cellsize*self.blockwidth

		ratio=self.cellsize
		cell_area=float(self.cellsize*self.cellsize)
		#9 direction from 0~180
		hog_hist=np.zeros([gray_img.shape[0]/ratio,gray_img.shape[1]/ratio,self.nbins+1],dtype=float)
		#hog_hist=np.zeros([gray_img.shape[0]/ratio,gray_img.shape[1]/ratio,self.nbins+1],dtype=np.uint8)
		width=self.border_width
		expand_img=cv2.copyMakeBorder(gray_img,width,width,width,width,cv2.BORDER_REPLICATE)

		"""
		for i in range(hog_hist.shape[0]):
			for j in range(hog_hist.shape[1]):
				pic_roi=gray_img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio]
				hog_hist[i,j,0]=np.uint8(np.sum(gray_img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio])/cell_area)

		return hog_hist
		"""
		dx_img=np.zeros(gray_img.shape)
		dy_img=np.zeros(gray_img.shape)
		for i in range(gray_img.shape[0]):
			dx_tmp=np.convolve(expand_img[i+width,:],self.derivate,'same')
			dx_img[i,:]=dx_tmp[width:-width]
		for i in range(gray_img.shape[1]):
			dy_tmp=np.convolve(expand_img[:,i+width],self.derivate,'same')
			dy_img[:,i]=dy_tmp[width:-width]

		cv2.namedWindow('test1',cv2.WINDOW_NORMAL)
		cv2.namedWindow('test2',cv2.WINDOW_NORMAL)
		cv2.imshow('test1',np.uint8(dx_img))
		cv2.imshow('test2',np.uint8(dy_img))
			

		print hog_hist.shape
		for i in range(hog_hist.shape[0]):
			for j in range(hog_hist.shape[1]):
				dx_roi=dx_img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio]
				dy_roi=dy_img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio]
				#mag_roi=np.sqrt(dx_roi**2+dy_roi**2)*np.sign(dy_roi)
				mag_roi=np.sqrt(dx_roi**2+dy_roi**2)
				ang_roi=np.arctan(dy_roi/(dx_roi+self.eps))
				np.putmask(ang_roi,ang_roi<0,ang_roi+np.pi)
				ang_remap1=np.floor(ang_roi/self.min_ang)
				ang_remap2=ang_remap1+1
				np.putmask(ang_remap1,ang_remap1<0,ang_remap1+9)
				np.putmask(ang_remap2,ang_remap2<0,ang_remap2+9)
				ang_o=np.pi-self.min_ang
				ang_proj_1=ang_roi-ang_remap1*self.min_ang
				ang_proj_2=ang_remap2*self.min_ang-ang_roi
				mag_project_ang1=mag_roi/np.sin(ang_o)*np.sin(ang_proj_2)
				mag_project_ang2=mag_roi/np.sin(ang_o)*np.sin(ang_proj_1)
				[wait_hist1,r]=np.histogram(ang_remap1,bins=self.nbins,range=(0,8),weights=mag_project_ang1)
				[wait_hist2,r]=np.histogram(ang_remap2,bins=self.nbins,range=(0,8),weights=mag_project_ang2)
				hog_hist[i,j,-1]=np.uint8(np.sum(gray_img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio])/cell_area)
				hog_hist[i,j,0:9]=wait_hist1+wait_hist2
				'''
				if i==2 and j==3:
				#if j==3 :
					print "==="
					print dx_roi 
					print "==="
					print dy_roi 
					print "==="
					print mag_roi
					print "---"
					print ang_roi
					print "~~~"
					print ang_remap1
					print "~~~"
					print ang_remap2
					print "~~~"
					print ang_o
					print "---"
					print ang_proj_1
					print "---"
					print ang_proj_2
					print "---"
					print mag_project_ang1
					print "---"
					print mag_project_ang2
					print "~~~"
					print wait_hist1
					print wait_hist2
					print hog_hist[i,j,0:9]
					print '++++'
					'''
				'''
				'''


		print hog_hist.shape
		return hog_hist

	def HogGray(self,hog_hist):
		ratio=self.cellsize
		img=np.zeros((hog_hist.shape[0]*ratio,hog_hist.shape[1]*ratio),dtype=np.uint8)
		for i in range(hog_hist.shape[0]):
			for j in range(hog_hist.shape[1]):
				img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio]=np.uint8(hog_hist[i,j,-1])
				
		#print img.shape
		#print img
		return img

	def Hogpicture(self,hog_hist):
		hog_pic=hog_hist[:,:,0:9]
		hog_pic_bf=hog_pic
		'''
		print "***"
		print hog_pic
		print "***"
		'''
		hog_pic=hog_pic/np.max(hog_pic)
		ratio=20
		img=np.zeros((hog_pic.shape[0]*ratio,hog_pic.shape[1]*ratio),dtype=np.uint8)
		for i in range(hog_pic.shape[0]):
			for j in range(hog_pic.shape[1]):
				buf=self.Cell2Img(hog_pic[i,j],ratio)
				img[i*ratio:(i+1)*ratio,j*ratio:(j+1)*ratio]=np.uint8(buf*255)
				#cv2.namedWindow('test21',cv2.WINDOW_NORMAL)
				#cv2.imshow('test21',np.uint8(buf*255))


		#cv2.namedWindow('test11',cv2.WINDOW_NORMAL)
		#cv2.imshow('test11',img)
		return img 

	def Cell2Img(self,cell_hist,width):
		#print width
		tmp=np.zeros((width,width),dtype=np.float)
		buf=np.zeros((width,width),dtype=np.float)
		tmp[np.round(width/2):np.round(width/2)+1,:]=1
		for idx in range(cell_hist.size):
			if idx==self.nbins:
				break
			angle=idx*self.min_ang/np.pi*180;
			M=cv2.getRotationMatrix2D((buf.shape[1]/2,buf.shape[0]/2),angle+90,1)
			rot=cv2.warpAffine(tmp,M,(tmp.shape[1],tmp.shape[0]))
			buf=buf+rot*cell_hist[idx]

		return buf





