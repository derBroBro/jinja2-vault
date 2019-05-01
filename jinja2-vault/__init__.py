import hvac
import os
import logging
from jinja2 import lexer, nodes
from jinja2.ext import Extension

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VaultExtension(Extension):
    tags = set(['secret'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # parase key, path and mount
        key = parser.parse_expression()
        parser.stream.skip_if('comma')
        if parser.stream.skip_if('name:path'):
            parser.stream.skip(1)
            path = parser.parse_expression()
        else:
            path = ""
        parser.stream.skip_if('comma')
        if parser.stream.skip_if('name:mount'):
            parser.stream.skip(1)
            mount = parser.parse_expression()
        else:
            mount = "secret"

        args = [path,key,mount]
        return nodes.Output([
            nodes.MarkSafeIfAutoescape(self.call_method('get_secret', args))
        ]).set_lineno(lineno)


    def get_secret(self, path, key, mount):
        # Try to connect
        try:
            hostname = os.getenv("VAULT_ADDR", "localhost")
            token = os.getenv("VAULT_TOKEN", "myroot")
            client = hvac.Client(hostname,token)
        except:
            logger.error(
                "Unable to connecto to {0}".format(hostname))
            return "failed-to-connect"
        
        # Verfiy authentication
        if not client.is_authenticated():
            logger.error(
                "Unable to authenticate")
            return "failed-to-auth"

        # Load data
        try:
            secret = client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount)
            logger.debug(secret)
        except hvac.exceptions.InvalidPath:
            logger.error(
                "Unable to find path {0}".format(path))
            return "failed-find-path"

        # return data
        if key in secret["data"]["data"]:
            return secret["data"]["data"][key]
        else:
            logger.error("No key {0} found".format(path))
            return "failed-find-key"
        
 
        
