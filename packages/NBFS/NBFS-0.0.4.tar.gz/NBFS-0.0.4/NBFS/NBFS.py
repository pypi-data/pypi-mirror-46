from .lib.decoder import parse

class NBFS:
    def __init__(self):
        pass

    @classmethod
    def bin2xml(cls, data):
        '''
        .NET Binary to XML
        :param bytes:
        :return:
        '''
        assert isinstance(data, bytes), 'Input data should be byte type.'
        return parse.parse(data)

    @classmethod
    def xml2bin(cls, content):
        '''
        Same as xml2mcnbfs
        :param content:
        :return:
        '''
        return cls.xml2mcnbfs(content)

    @classmethod
    def xml2mcnbfs(cls, content):
        '''
        XML to .NET Binary in format [MC-NBFS] (standard)
        :param content:
        :return:
        '''
        return parse.xml_to_mcnbfs(content)

    @classmethod
    def xml2mcnbfse(cls, content,nosizeprefix=True):
        '''
        XML to .NET Binary in format [MC-NBFSE] with in-band dictionary
        :param content:
        :return:
        '''
        return parse.xml_to_mcnbfse(content,nosizeprefix)
