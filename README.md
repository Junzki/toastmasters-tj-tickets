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

## License
GPLv3
