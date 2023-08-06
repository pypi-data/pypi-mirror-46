from cmd import Cmd

from boto3 import client


class S3Shell(Cmd):

    def __init__(self):
        super().__init__()
        self.conn = client('s3')
        self._wd = ''
        self.prompt = '> '

    @property
    def wd(self):
        return self._wd

    @wd.setter
    def wd(self, d):
        self.prompt = d + '> '
        self._wd = d

    def do_ls(self, args):

        if not self.wd and not args:
            [print(b.get('Name')) for b in self.conn.list_buckets().get('Buckets')]
        else:
            if args:
                bucket, *prefix = args.split('/')
            else:
                bucket, *prefix = self.wd.split('/')
            prefix = '/'.join(prefix)
            result = self.conn.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
            for o in result.get('CommonPrefixes'):
                print(o.get('Prefix').replace(prefix, ''))

    def do_cd(self, args):
        if args == '..':
            self.wd = '/'.join(self.wd.split('/')[:-2])
        else:
            self.wd += args + '/'


if __name__ == '__main__':
    prompt = S3Shell()
    prompt.cmdloop('Starting prompt...')
