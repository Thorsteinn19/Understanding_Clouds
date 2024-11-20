# Understanding_Clouds
Group 4 - solution to the kaggle competition understanding clouds
```
Preprocessing
	- Download all data from Kaggle, Understanding Clouds from Satellite Images
	- Run boundingbox.py in the same directory as the train.csv to convert runlength encoding to bounding boxes
	- Run bb2roboflow.mlx to convert the bounding box output csv file to annotation format for roboflow.com
	- Move all txt files generated in previous step into the training image folder. 
	- Upload the trainingfolder to roboflow with txt files for annotation.
	- Export dataset with downscaling to 640x640 with padding
	- Find the preprocessed dataset in the Roboflow_dataset folder
Training
	- Install yolov5, https://github.com/ultralytics/yolov5  (if using GPU make sure torch version is compatable with CUDA drivers)
	- python3 train.py --img 640 --epochs 100 --data Roboflow_dataset/data.yaml --weights Roboflow_dataset/yolov5l.pt --device 0
		-Remove --device 0 to run on cpu when gpu is not available, if gpu has another device id make sure the number matches
	- After training is complete, the weights will be found under runs/training/exp/weights, pick best.pt
 	- The trained model can be found in the exp folder
Testing
	- After training the model, run the model on the test images from Kaggle by using the following command
		python detect.py --weights best.pt --source D:\...\yolov5\data\images\test_images\ --conf-thres 0.30 --iou-thres 0.4 --save-		txt --save-format 1 --imgsz (350,525) --device 0
	- Make sure the path to the images is the same as on the computer using the model and same goes for the weights
	- Modify the weights to find the best combination, the values above were found to offer the highest score when uploaded to Kaggle
Post processing
	- With the lables generated from yolov5l model, they need to be reinterpreted to run length encoding
	- Run bb2rle.py in the directory of the lables to generate the result.csv file
	- Run the kagglesubmission.py file, make sure that submission=pd.read_csv('results.csv') points to the file generated above.
	- Then upload the now generated submission.csv file to kaggle

```