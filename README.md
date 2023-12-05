#  Instructions / Setup 🚀
- Put json files in `/data` directory. Articles.db will be set up also there.
- Run pipeline with the following command while being in the root dir (i.e. where this file lies)
```shell
python main.py
```
- In the REPL system, type `help` for example queries
- You may have to install the dependencies in the requirements.txt first
- For the last command, i.e. `example [1...8]`, please use the seperator token, e.g. `example $1`
- Please refer to folder structure below to learn how the REPL system is organized.

# Folder Structure 🗂️
```
📦 REPL-EXERCISE-03
 ┣ 📂data                      <-- Put JSON files and/or articles.db here 
 ┣ 📂output                    <-- Figures will be saved here
 ┣ 📂queries                   <-- Saved queries from exercise 02
 ┃ ┗ 📜queries.py              <-- Contains the SQL queries from last exercise
 ┣ 📂src                       <-- Source code
 ┃ ┣ 📜constants.py            <-- Defines constants, e.g. valid commands
 ┃ ┣ 📜crud_interface.py       <-- Implements CRUD operations
 ┃ ┣ 📜data_classes.py         <-- Implements DAOs
 ┃ ┣ 📜evaluation.py           <-- Implements the valid REPL commands
 ┃ ┣ 📜guard.py                <-- Class to check for valid inputs
 ┃ ┣ 📜preprocess_input.py     <-- Class to preprocess user input
 ┃ ┗ 📜utils.py                <-- Defines utility / helper functions
 ┣ 🕹️main.py                   <-- Entry point of the REPL
 ┣ 📜README.md                 <-- Documentation
 ┗ 📜requirements.txt          <-- The requirenments file for reproducing the environment
```
