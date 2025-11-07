Test 1: 
	100 hidden layer neurons with relu function
	250/250 - 2s - 8ms/step - accuracy: 0.8685 - loss: 0.7337
Test 2:
	4 x 100 hidden layer neurons with relu function
	250/250 - 5s - 22ms/step - accuracy: 0.8629 - loss: 0.7310
	
Test 3:
	48 layer
	64 2 x convolution layers
	pooling layer (2x2)
	dropout 0.25
	Flatten
	96 layer
	48 Outputlayer
	Training: accuracy: 0.9856 - loss: 0.0583
	Test:	  accuracy: 0.9740 - loss: 0.1165
	
Test 4:
	All test 3, but pooling layer (3x3)
	Training: accuracy: 0.9828 - loss: 0.0674 - precision: 0.9856 - recall: 0.9796
	Test:	  accuracy: 0.9879 - loss: 0.0608 - precision: 0.9899 - recall: 0.9856