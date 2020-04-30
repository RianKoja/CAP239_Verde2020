FROM continuumio/anaconda3:2020.02

ARG target_dir=./src

RUN apt-get update && apt-get install -y -qq graphviz

WORKDIR /project

# Set entrypoint to execute python:
ENTRYPOINT [ "python3" ]

# Copy project dependencies of the project first, as it should change less often:
COPY ${target_dir}/requirements.txt /project/

# Install project dependencies:
RUN conda install --yes --file requirements.txt

# Copy project files only at the end of image, to improve reusage of intermediate images:
COPY ${target_dir} /project/

# By default, call Entry.py when running the container.
CMD ["Entry.py"]