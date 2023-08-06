# TakeMessageCleaner

TakeMessageCleaner is a tool for pre processing messages. 
It can be used to convert messages to lower case, correct spelling, remove elements like punctuation, emoji, whatapp's emoji, accentuation, number, cpf, url, e-mail, money, code, time, date and small talks.
Also, it can pre process data from a dataframe, series, list or csv file.

#### MessageCleaner.from_dataframe: creates a constructor from a dataframe

<ul>
<li>config_file_path: str</li>
config_file_path is the path of the json file with the configuration

<li>dataframe: pd.core.frame.DataFrame</li>
dataframe is the pandas dataframe that needs to be processed.

<li>content_column : str</li>
content_column is the column name of the dataframe that has the information to be processed.
</ul>

#### MessageCleaner.from_series: creates a constructor from a series

<ul>
<li>config_file_path: str</li>
config_file_path is the path of the json file with the pre processing

<li>series: pd.core.frame.Series</li>
series is the pandas series that needs to be processed.

#### MessageCleaner.from_list: creates a constructor from a list

<ul>
<li>config_file_path: str</li>
config_file_path is the path of the json file with the configuration

<li>lst: list</li>
lst is the list of string that need to be processed.
</ul>

#### MessageCleaner.from_file: creates a constructor from a csv file
file_path : str, content_column : str = 'Content', encoding: str = 'utf-8', sep: str = ';'

<ul>
<li>config_file_path: str</li>
config_file_path is the path of the json file with the configuration

<li>file_path : strt</li>
file_path is the path of the csv file that needs to be processed.

<li>content_column: str</li>
content_column is the column name of the dataframe that has the information to be processed. If the file separator is not set, the value 'Content' will be used.

<li>sep: str</li>
sep is the csv file separator. If the file separator is not set, the value ';' will be used.

<li>encoding: str</li>
encoding is the encoding of the csv file. If the file encoding is not set, the value 'utf-8' will be used.
</ul>

#### MessageCleaner.pre_process: pre-process messages using a json file with the configuration.
The pre processing step is able to convert sentences to lower case, correct spelling and remove elements like punctuation, emoji, whatapp emoji, accentuation, number, cpf, url, e-mail, money, code, time, date and small talks.
Optionally, you can activate use_placeholder to insert a placeholder where the element was removed. For example: "I want 2 apples" would be converted in "I want NUMBER apples".

## config.json
```
{
	"use_placeholder": true,
	"verbose": true, 
	"processing": {
		"lower": true,
		"punctuation": true,
		"emoji": true,
		"wa_emoji": true,
		"accentuation": true,
		"number": true,
		"cpf": true,
		"url": true,
		"email": true,
		"money": true,
		"code": true,
		"time": true,
		"date": true,
		"spelling": true
	},
	"output": {
		"file_name": "output_file.csv",
		"file_encoding" : "utf-8",
		"file_sep": ";",
		"remove_duplicates": true,
		"remove_empty": true,
		"sort_by_length": true
	}
}
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TakeMessageCleaner

```bash
pip install TakeMessageCleaner
```

## Usage

```python
import MessageCleaner as mc

cleaner = mc.MessageCleaner.from_file(config_file_path = 'C:/Documents/config.json', file_path = 'C:/Users/mydata.csv', sep = ';', encoding = 'latin-1')
result = cleaner.clean()
print(result)
```

## Author
Karina Tiemi Kato

## License
[MIT](https://choosealicense.com/licenses/mit/)