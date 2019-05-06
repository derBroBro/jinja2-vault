import hvac
import os
import logging
from jinja2 import lexer, nodes
from jinja2.ext import Extension

debug_level = os.getenv("JINJA2_VAULT_DEBUG", "WARNING")
logging.basicConfig(level=debug_level)
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
            hostname = os.getenv("VAULT_ADDR", "http://localhost:8200")
            token = os.getenv("VAULT_TOKEN", "myroot")
            client = hvac.Client(hostname,token)
            # Verfiy authentication
            if not client.is_authenticated():
                logger.warning(
                    "Unable to authenticate")
                client.adapter.close()
                return "failed-to-auth"
        except:
            logger.warning(
                "Unable to connecto to {0}".format(hostname))
            client.adapter.close()
            return "failed-to-connect"
        


        # Load data
        try:
            secret = client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount)
            logger.debug(secret)
        except hvac.exceptions.InvalidPath:
            logger.warning(
                "Unable to find path {0}".format(path))
            client.adapter.close()
            return "failed-find-path"

        # return data
        if key in secret["data"]["data"]:
            client.adapter.close()
            return secret["data"]["data"][key]
        else:
            logger.warning("No key {0} found".format(path))
            client.adapter.close()
            return "failed-find-key"
        
 
        
