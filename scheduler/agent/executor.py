from subprocess import Popen
from tempfile import TemporaryFile
from utils import getlogger

logger = getlogger(__name__,'./output.log')
class Executor:

    def run(self,script, timeout=None):
        with TemporaryFile('w+') as f:
            p = Popen(script, shell=True,stdout=f)
            code = p.wait()
            f.seek(0)
            text = f.read()
        logger.info('{} {}'.format(code, text))
        return code,text







