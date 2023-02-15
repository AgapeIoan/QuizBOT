# QuizBOT

QuizBOT is a Discord bot that allows you to create quizzes and practice them.

## Requirements
- The bot requires Python 3.10 or higher.
- Pip requirements can be installed by using `pip install -r requirements.txt` in the terminal.

## Setup
- The bot requires a Discord bot token to run. You can get one by creating a new application on the [Discord Developer Portal](https://discord.com/developers/applications). Once you have created the application, go to the bot tab. By pressing the Reset Token button, you can then copy the token and paste it into the `config.json` file or `deb_config.json` file, depending on the use case.
- For progression support, the bot needs a MySQL database. The credentials are saved in the `sql.json` file.
The progress SQL queries are thought to be used with the following table:
```sql
CREATE TABLE `quizbot` (
  `int_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `discord_uid` TEXT NOT NULL,
  `question_number` INT UNSIGNED NOT NULL,
  `answer_number` INT UNSIGNED NOT NULL,
  `total` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`int_id`)
) ENGINE = InnoDB;
```
- The quizes are saved in the `questions.json` file. More info and examples in the `storage/quiz` folder.
## Usage
- The bot can be started by using `python3 index.py` in the terminal. The invite link will be shown after the bot successfully logged in. [Example](https://files.agapeioan.ro/github/quizbot_startup.png)

