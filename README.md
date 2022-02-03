# Engineering project
> The program was prepared as a group engineering project

# Introduction 
This program allows performing detection and classification of LEGO bricks. It can work with videos in mp4 format, which contains the bricks moving from the right side to the left, or with any photos stored in any folder.
Object detection is using either YOLOv4-tiny neural network model or YOLOv5s model. Classification of detected bricks is done using classifier loaded by Keras library as the part of TensorFlow.

# Run and Test the main app
## Run
Run `program` configuration in PyCharm or `python ./program.py` command in `src` folder.

It is required to add `..` to PYTHONPATH environment variable before running the app.

## Tests
Launch `Unittests` configuration in PyCharm or run `python -m unittest discover -s ./test -t .` command in project folder.

## Running without GPU
Default configuration and list of dependencies (described in [Environment configuration](#environment-configuration) section) includes the configuration for GPU processing. Setting the app for only CPU, when GPU is not available for TensorFlow Python library (e.g. no GPU or no CUDA for it) two things must be adjusted:
- `tensorflow` library should be used instead of `tensorflow-gpu`
- in `video_remote.py` file inside `src/remotes` folder line `@ray.remote(num_cpus=1, num_gpus=0.5)` must be changed to `@ray.remote(num_cpus=1)`


## Detailed information about configuration of the server app
There is additional README file inside src file which describes the configuration of the app and some additional information about the implementation itself to allow easier further development.

# Environment configuration
It is possible to use any type of Python environment. It can work for at least Python versions 3.8 or 3.9 as long as it contains all required libraries which are listed inside `environment.yml`. Possible multiple of those dependencies can also work on different versions, e.g. TensorFlow was also tested for 2.4.2 version.

Below there is description of activation process specifically for Anaconda with 3.9.5 Python version.
## Anaconda environment

### Requirements
- conda Environment (e.g. Anaconda) compatible with Python 3.9.5

### Environment installation options
PyCharm should detect `enviroment.yml` on the first launch and ask to import the environment.

Alternatively, run the same command as for environment updates section. Then you need to switch to this environment `conda activate env_name_or_path` e.g. `conda activate ./env`. Such an environment can be also added in PyCharm in Settings->Project->Python Interpreter as an existing environment.
    
### Environment updates:
When there are changes to `environment.yml` file made by someone else, then you need to run the following command in project folder:
`conda env update --prefix conda_environment_path --file environment.yml  --prune`, for example, `conda env update --prefix ./env --file environment.yml --prune` to make it in the folder project.

If you need to include new libraries in the environment, then you need to update `environment.yml` and add dependencies there. Possibly, command from `conda env export --from-history` can be helpful to list all the required dependencies, but remember to keep channel as `conda-forge`.

# Scripts
There are also a few scripts in `scripts` folder, they are described in additional README files there.

# Contact and contributors
Contributors:
- Tomasz Piechocki - (https://github.com/TPiechocki))
- Rozalia Solecka
- Mateusz Nieścier

# References
- GitHub with conversion of darknet model to TensorFlow and yolo_v4 and yolo_v4 detection
(minor chunk of codes taken from there)
https://github.com/hunglc007/tensorflow-yolov4-tflite
