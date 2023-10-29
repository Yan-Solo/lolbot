from enums import Enums

# Source: https://gist.github.com/kkrypt0nn/a02506f3712ff2d1c8ca7c9e0aed7c06
# other: https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51#masked-links
class DiscordStyle:
    def __init__(self) -> None:
        pass
    def orangeColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Yellow.value,message)
    def greenColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Green.value,message)
    def blueColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Blue.value,message)
    def lightBlueColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Cyan.value,message)
    def redColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Red.value,message)
    def pinkColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Pink.value,message)
    def grayColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.Gray.value,message)
    def whiteColor(self,message):
        return self.__codeToANSIColor(Enums.ANSITextColorCode.White.value,message)
    
    def __codeToANSIColor(self,code, message):
        return f"\u001b[1;{code}m{message}\u001b[0m"

