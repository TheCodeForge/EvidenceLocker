import hmac

def generate_hash(string):

    msg = bytes(string, "utf-16")

    return hmac.new(key=bytes(environ.get("MASTER_KEY"), "utf-16"),
                    msg=msg,
                    digestmod='md5'
                    ).hexdigest()


def validate_hash(string, hashstr):

    return hmac.compare_digest(hashstr, generate_hash(string))