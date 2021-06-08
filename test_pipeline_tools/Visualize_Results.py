from IPython.display import display, Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Visualize_Results():

	def __init__(self, images_path):
		self.images_path = images_path
		
	def overall_accuracies(self,database):
		overall_kind_acc = database +'_kind_accuracy.png'
		overall_pcs_acc = database + '_pcs_accuracy.png'
		
		fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 30), dpi=90, facecolor='w', edgecolor='k')
		for a in ax:
		    a.axis('off')
		    
		#ax[0].set_title('OVERALL ACCURACIES')

		img = mpimg.imread(self.images_path + overall_kind_acc)
		ax[0].imshow(img)
		img = mpimg.imread(self.images_path + overall_pcs_acc)
		ax[1].imshow(img)
		fig.tight_layout()
	def result(self,database,split):
	
		kind_performance = database +'_TestSet_'+split+ '_kind_performance.png'
		kind_cm = database +'_TestSet_'+split + '_kind_cm.png'
		pcs_performance = database +'_TestSet_'+ split+ '_pcs_performance.png'
		pcs_cm =database +'_TestSet_'+split+ '_pcs_cm.png'

	
		
		fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(50, 50), dpi=90, facecolor='w', edgecolor='k')
		for a in ax:
		    a.axis('off')
		    

		img = mpimg.imread(self.images_path + kind_performance)
		ax[0].set_title('PER KIND PERFORMANCE')
		ax[0].imshow(img)

		img = mpimg.imread(self.images_path + kind_cm)
		ax[1].set_title('PER KIND CONFUSION MATRIX')
		ax[1].imshow(img)

		img = mpimg.imread(self.images_path + pcs_performance)
		ax[2].set_title('PITCH CLASS SET PERFROMANCE')
		ax[2].imshow(img)

		img = mpimg.imread(self.images_path + pcs_cm)
		ax[3].set_title('PITCH CLASS SET CONFUSION MATRIX')
		ax[3].imshow(img, interpolation='nearest')
		
		fig.tight_layout()
	def filtered_stats(self,database, kind, split):
		models = database +'_'+split+'_' + kind + '_models.png'
		distribution= database+'_TestSet_'+split+'_'+kind+'_distribution.png'
		ratio= database+'_TestSet_'+split+'_'+kind+'_ratio.png'
		hexagram= database+'_TestSet_'+split+'_'+kind+'_hexagram.png'
		
		fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(20, 20), dpi=90, facecolor='w', edgecolor='k')
		for a in ax:
	   		a.axis('off')

		img = mpimg.imread(self.images_path + models)
		ax[0].set_title('MODELS')
		ax[0].imshow(img)

		img = mpimg.imread(self.images_path + distribution)
		ax[1].set_title('DISTRIBUTIONS')
		ax[1].imshow(img)

		img = mpimg.imread(self.images_path + ratio)
		ax[2].set_title('STRONG DEGREE RATIO')
		ax[2].imshow(img)

		img = mpimg.imread(self.images_path + hexagram)
		ax[3].set_title('BALANCE')
		ax[3].imshow(img, interpolation='nearest')
		fig.tight_layout()

