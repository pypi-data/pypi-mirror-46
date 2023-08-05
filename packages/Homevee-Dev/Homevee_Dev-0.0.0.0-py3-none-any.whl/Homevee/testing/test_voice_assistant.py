import traceback

from Homevee.Helper import translations, Logger
from Homevee.Utils.Database import Database
from Homevee.VoiceAssistant import VoiceAssistant


def run_voice_tests():
    print("running voice tests...")

    commands = [
        "hallo",
        "mach das licht im garten an",
        "was steht an",
        "wie wird das wetter morgen",
        "was steht auf der einkaufsliste",
        "wie viel kalorien hat ein apfel",
        "was kommt im fernsehen",
        "was sind die tv tipps",
        "wer war paul walker",
        "wie lange brauche ich von velden nach münchen",
        "wie warm ist es in der küche",
        "was kann ich morgen mit freunden kostenlos machen",
        "erzähl mir einen witz",
        "was ist 5 mal 5",
        "wie ist der film titanic",
        "was ist der 24. dezember 2019 für ein tag",
        "was ist der 24. dezember für ein tag",
        "wie viel fett habe ich noch offen",
        "ksdjflksdfl",
    ]

    username = "sascha"
    db = Database.get_database_con()

    for command in commands:
        try:
            output = VoiceAssistant().do_voice_command(username, command, None, None, db, translations.LANGUAGE)

            output_text = output['msg_text']

            print("===> "+command+": "+output_text)
        except:
            print("error at command: "+command)
            if(Logger.IS_DEBUG):
                traceback.print_exc()