@echo off & python -x "%~f0" %* & goto :eof
from s3sh.repl import S3Shell

if __name__ == '__main__':
    prompt = S3Shell()
    prompt.cmdloop('Starting prompt...')
