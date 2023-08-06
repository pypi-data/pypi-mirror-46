# MySQLWrapperPackage

This is a  small MySQL database wrapper module that injects a mysql connection instance

## Getting Started
These instructions should help you run the code on your machine.

### Prerequisites
The code is written in Python3

### Installing the package 

Install the package 

```
pip install mysqlwrapperpackage
```

### Installing locally from github

start by cloning the repository from GitHub:

for https use
```
$ git clone https://github.com/Sharonsyra/MySQLWrapperPackage.git
```

for ssh use 
```
git clone git@github.com:Sharonsyra/MySQLWrapperPackage.git
```

Install the application's dependencies from `requirements.txt`
```
$ pip install -r requirements.txt
```

Start your MySQL server

```
mysqld
```

### Running the project

In you Working folder Test with this commands 

- Import WrapperPackage 

```
from MySQLWrapperPackage.wrapper import MySQLWrapper
```

- Make an instance of the start method. This creates an instance of the connection

```
variable_name = MySQLWrapper.start()
```

- View all from table

```
variable_name.fetch_all('table')
```

### Run your tests:
```
$ nose2 
```

## Resources Used
- Dependency Injection Python - [Python Dependency Injection](https://medium.com/@shivama205/dependency-injection-python-cb2b5f336dce)
