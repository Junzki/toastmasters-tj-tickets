# ETL Tools for Toastmasters TJ Conference

## Usage
1. Copy `etc/config.sample.yaml` to `etc/config.yaml` and add your database connection arguements to the field `DEFAULT.dsn`
2. Initiate `ipython` interactive shell (or other Python shell you like)
3. Call loaders in the `loaders` directory.   
   Basically, call `loader.run(path, sheet_name)` method will do the job, please turn out to the source code for detail
4. Join data as you wish with SQL and PostgreSQL


## Requirements
- Python 3.10 (or above)
- PostgreSQL 14
- Components listed in the `requirements.txt`

## Privacy and Security Notice
1. This project itself does not contain any privacy data.   
   Please make sure **NOT** to submit any privacy data before committing and opening any PRs.
2. If you use cloud databases, please ensure you have applied appropriate permissions and hardening strategies.
3. This project and its maintainers make no warranties about potential privacy non-compliance or data leakage; please follow your local security and privacy laws, rules, and policies.

## License
GPLv3
