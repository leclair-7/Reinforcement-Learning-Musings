
from Layers import  *
from Render2D import Render

if __name__=='__main__':
	Q_init = np.zeros((4,3))
	layer = Layer(Q_init, "Mister Spider")
	
	layers = [layer]	

	display = Render(layer = layer)

	while display.getRunning():
		display.HandleEvent()