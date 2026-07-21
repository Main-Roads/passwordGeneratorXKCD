
from flask import Flask, render_template, request
from configFileHelper import Config
from flask_htmlmin import HTMLMIN

from pathlib import Path
from datetime import datetime
from os import getenv

try:
    from icecream import ic

    def ic_set(debug):
        if debug:
            ic.enable()
        else:
            ic.disable()


except ImportError:  # Graceful fallback if IceCream isn't installed.
    doDebug: bool = False

    def ic(thing):  # just print to STDOUT
        if doDebug:
            print(thing)

    def ic_set(debug):
        global doDebug
        doDebug = debug
        ic("* icecream module not imported successfully, using STDOUT")


def nowString():
    return f"{datetime.now().strftime('%Y.%m.%d %T')} |> "

try:
    ic.configureOutput(prefix=nowString)
except AttributeError:
    pass


_default_env_location = '/home/app/web/project/config.yaml'

def getConfig(configFile: str):
    global __version__
    # Looks in current folder (i.e. the "app" folder), then if it doesn't find it there looks at the project folder
    
    thisPath = Path(configFile).resolve()

    if not thisPath.is_file():
        raise FileNotFoundError(str(thisPath))
    config = Config(file_path=thisPath)
    ic_set(config.get_bool("APP/DEBUG"))
    try:
        __version__ = thisPath.parent.joinpath('VERSION').read_text().rstrip()
    except FileNotFoundError:
        __version__ = "NFI"

    return config

CONFIG = getConfig(getenv('APP_CONFIG',_default_env_location))

app = Flask(__name__)
app.config['MINIFY_HTML'] = CONFIG.get_bool('APP/MINIFY_HTML')

htmlmin = HTMLMIN(app)


@app.route("/version")
def getVersion():
    return __version__


def _getPasswordsDict():
    theConfig = CONFIG.get('XKCDPASS')
    theOutput = {}
    if CONFIG.get_bool("APP/DEBUG"):
        theOutput['config'] = theConfig
    passwords = generateIt(theConfig)
    pad = len(str(len(passwords)))
    theOutput["passwords"] = []
    theOutput["maxLength"] = (len(max(passwords, key=len)) - 1)
    for ix, p in enumerate(passwords):
        this = {"varname": "p", "varvalue": p, "varlen": len(p)}
        this["varname"] += f"{('0'*pad)}{(ix+1)}"[(-1 * pad):]
        theOutput["passwords"].append(this)
    return theOutput


@app.route("/json")
def getJSON():
    theDict = _getPasswordsDict()

    if (request.args.get('includeConfig', default=0, type=int) == 1):
        ...
    else:
        theDict.pop('config', None)
        theDict.pop('maxLength', None)

    theList = []
    for p in theDict["passwords"]:
        theList.append(p["varvalue"])
    theDict["passwords"] = theList
    return theDict


@app.route("/")
def index():
    passwordDict = _getPasswordsDict()
    return render_template('index.html', passwords=passwordDict["passwords"], debugMode=1 if app.debug else None, maxLength=passwordDict["maxLength"], version=getVersion())


def generateIt(params):

    def _fix_up_params(params):

        defaults = [("wordfile", None), ("valid_chars", "."), ("valid_delimiters", " ,"), ("random_delimiters", False),
                    ("delimiter", " "), ("numwords", 4), ("acrostic", None), ("count", 1), ("case_methods", "lower"), ("count", 1)]
        for d in defaults:
            params[d[0]] = params.get(d[0], d[1])
        for k in params.keys():
            if isinstance(params[k], str) and params[k] == "None":
                params[k] = None

        params["delimiter"] = None if params["random_delimiters"] else params.get(
            "delimiter", " ")

        return params

    import xkcdpass.xkcd_password as xp

    params = _fix_up_params(params)
    wordfile = xp.locate_wordfile(wordfile=params["wordfile"])

    mywords = xp.generate_wordlist(
        wordfile=wordfile, min_length=params['min_length'], max_length=params['max_length'], valid_chars=params['valid_chars'])

    # XKCD - make sure we have the chance of "Correct Horse Battery Staple"
    for w in ["correct", "horse", "battery", "staple"]:
        if w not in mywords and len(w) >= params["min_length"] and len(w) <= params["max_length"]:
            mywords.append(w)

    passwords = []
    for _ in range(params["count"]):
        password = xp.generate_xkcdpassword(mywords,
                                            numwords=params["numwords"], interactive=False,
                                            acrostic=params["acrostic"],
                                            delimiter=params["delimiter"],
                                            random_delimiters=params["random_delimiters"],
                                            valid_delimiters=params["valid_delimiters"],
                                            case=params["case_methods"]
                                            )

        if password[0] in params["valid_delimiters"]:
            password = password[1:]
        if password[-1] in params["valid_delimiters"] and password[-1] not in ['.', '!', ';']:
            password = password[:-1]
        passwords.append(password)

    return passwords


if __name__ == '__main__':
    app.run(host=CONFIG.get("APP/HOST"), port=5000,
            debug=CONFIG.get_bool("APP/DEBUG"))
