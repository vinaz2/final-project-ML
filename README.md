My project is called ***Kitty Puppy Snakelet***. It is an interative program to play with that user could pet any virtual cats, dogs or snakes from any pictures they find online, for those children are having allergies/cannot be allowed to pet to pets but still wish to pet a cat, snake or dog. The pygame is interactive as it will have the sounds varying (except the snake! Because snake does not have many feelings to their human owners, sadly) and also the message line changing when the user did any actions with the pet. 


Depending on the category of the animal in the picture the user inputs, with the concept of multiclass classification in machine learning, the program will recognize between dogs, snakes, and cats and continue to each category's contextual functions that user could call to the dog, the snake or cat. 


E.g. If the user inputs a cat image, the functions that user will end up playing with are collecting the dropped furs, cleaning the cat litters, and feeding kitty treats; if the user inputs a dog, the functions that user could play with would be feed the bones, hug the dog and walk the dog; if the user inputs a snake image, the fucntions that user could play with would be feed rats, clean ecdysis, and curl up gently. 

***Three main original functions*** are def run_game(img_path, pet_type), def classify_pet, and def choose_image_file().


***Flow (Steps to run my program)***:

1. install all the dependencies on your terminal (see requirements_dependencies.txt);

2. git clone this repo (typing command "git clone https://github.com/vinaz2/final-project-ml");

(There is a big file, the model file, so then you should only get the files by git clone. Downloading the files directly from github website will cause the model file to be html format, not the Hierarchical Data Format that the my model file is actually of.)

3. run the main_try5.py (this is the main file);

(Running it might take a bit of time for the drop-drag pops up, thanks for the patience~~~)

4. find a picture of single cat/dog/snake you like from internet to input;

5. pygame got started.



***The things I did for pursuing extra credit up to 5%***:

1. This project blends a significant concept in machine learning since the program categorize the specie of animal in the input image without the user explicitly telling the program. I self-studied the Andrew Ng's online Stanford series of courses on Coursera to go through the concepts in supervised learning and convolutional layers. 

2. To have more original efforts, based on the existing training code of cats. vs dogs categorization, I changed this training code to make it capable do categorization on three classes instead of two.

3. To improve my model's efficiency for those pictures that are vague or too bright, I not only prepare the dataset from kaggle but also did changes to the dataset I used to train the neural network (manully add some extremely blurry pictures to each class using my original bulk_download.py to change the unsplash. com API after learning python knowledge in changing website's API to download bulk of considerably blurry cats, dogs and snakes pictures systematically.). 

4. I changed the pretrained CNN been used in the training script (from resnet to EfficientNetB0), the number of freezing layers in the convolutional neural network and also the parameters to augument the images. I did many times of adjusting to make it right now could differ cats, dogs and snakes images even they are pretty vague.














